import unittest

from constants import Action, WrongInputException, WrongInputText
from custom_database import CustomDataBase
from input_filter import InputFilter


class InputFilterCase(unittest.TestCase):

    def test_filter_wrong_lines(self):
        filter = InputFilter('')
        self.assertFalse(filter.is_valid())
        self.assertIsInstance(filter.error, WrongInputException)
        self.assertEqual(filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

        filter = InputFilter('This makes no sense')
        self.assertFalse(filter.is_valid())
        self.assertIsInstance(filter.error, WrongInputException)
        self.assertEqual(filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

        filter = InputFilter('This "makes no" "sense" too')
        self.assertFalse(filter.is_valid())
        self.assertIsInstance(filter.error, WrongInputException)
        self.assertEqual(filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

        filter = InputFilter('GET "this will not work"')
        self.assertFalse(filter.is_valid())
        self.assertIsInstance(filter.error, WrongInputException)
        self.assertEqual(filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

        filter = InputFilter('SET "I told" "you +5"')
        self.assertFalse(filter.is_valid())
        self.assertIsInstance(filter.error, WrongInputException)
        self.assertEqual(filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

    def test_filter_get(self):
        test_filter = InputFilter('GET A')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.GET,
             'key'    : 'A',
             'value'  : None, })

        test_filter = InputFilter('GET A 5')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

        test_filter = InputFilter('GET')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.NO_ARGUMENT_NAME.value)


    def test_filter_set(self):
        test_filter = InputFilter('SET A 5')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.SET,
             'key'    : 'A',
             'value'  : '5', })

        test_filter = InputFilter('SET')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.NO_ARGUMENT_NAME.value)

        test_filter = InputFilter('SET A')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.NO_ARGUMENT_VALUE.value)

    def test_filter_unset(self):
        test_filter = InputFilter('unset A')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.UNSET,
             'key'    : 'A',
             'value'  : None, })

        test_filter = InputFilter('unset')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.NO_ARGUMENT_NAME.value)

        test_filter = InputFilter('unset A 5')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

    def test_filter_counts(self):
        test_filter = InputFilter('counts 5')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.COUNTS,
             'key'    : None,
             'value'  : '5', })

        test_filter = InputFilter('COUNTS')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.NO_ARGUMENT_NAME.value)

        test_filter = InputFilter('COUNTS A 5')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

    def test_filter_find(self):
        test_filter = InputFilter('FIND 5')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.FIND,
             'key'    : None,
             'value'  : '5', })

        test_filter = InputFilter('FIND')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.NO_ARGUMENT_NAME.value)

        test_filter = InputFilter('FIND A 5')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

    def test_filter_help_end_begin_rollback_commit(self):
        """
        Тестируемые команды в целом не отличаются по суть друг от друга с точки зрения фильтрации
        входной строки. Нет аргументов и параметров.
        :return:
        """
        test_filter = InputFilter('HELP')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.HELP,
             'key'    : None,
             'value'  : None, })

        test_filter = InputFilter('END')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.END,
             'key'    : None,
             'value'  : None, })

        test_filter = InputFilter('BEGIN')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.BEGIN,
             'key'    : None,
             'value'  : None, })

        test_filter = InputFilter('ROLLBACK')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.ROLLBACK,
             'key'    : None,
             'value'  : None, })

        test_filter = InputFilter('COMMIT')
        self.assertTrue(test_filter.is_valid())
        self.assertDictEqual(
            test_filter.cleaned_data,
            {'command': Action.COMMIT,
             'key'    : None,
             'value'  : None, })


        test_filter = InputFilter('HELP A')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

        test_filter = InputFilter('HELP A 5')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)

        test_filter = InputFilter('HELP A 5 asd ')
        self.assertFalse(test_filter.is_valid())
        self.assertIsInstance(test_filter.error, WrongInputException)
        self.assertEqual(test_filter.error.message, WrongInputText.WRONG_INPUT_FORMAT.value)


class CustomDataBaseCase(unittest.TestCase):

    def setUp(self):
        self.test_database = CustomDataBase()


    def test_set(self):
        self.test_database.set('A', '5')
        self.assertDictEqual(self.test_database.database, {'A': '5'})

    def test_get(self):
        self.test_database.database = {'A': '5'}
        self.assertEqual(self.test_database.get('A'), '5')
        self.assertRaises(WrongInputException, self.test_database.get, 'B')

    def test_unset(self):
        self.test_database.database = {'A': '5', 'B': '4'}
        self.test_database.unset('B')
        self.assertDictEqual(self.test_database.database, {'A': '5'})
        self.assertRaises(WrongInputException, self.test_database.unset, 'B')

    def test_counts(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}
        self.assertEqual(self.test_database.counts('4'), 2)
        self.assertEqual(self.test_database.counts('0'), 0)

    def test_find(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}
        self.assertListEqual(self.test_database.find('4'), ['B', 'C'])
        self.assertListEqual(self.test_database.find('0'), [])

    def test_begin_transaction(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}
        self.test_database.begin_transaction()
        self.test_database.set('I_AM_ONLY_IN_TRANSACTION', '55')
        self.assertDictEqual(self.test_database.transaction_stack[0], {'A': '5', 'B': '4', 'C': '4'})
        self.assertDictEqual(self.test_database.database, {'A'                       : '5',
                                                           'B'                       : '4',
                                                           'C'                       : '4',
                                                           'I_AM_ONLY_IN_TRANSACTION': '55'})

    def test_rollback_transaction(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}
        self.test_database.begin_transaction()
        self.test_database.set('I_AM_ONLY_IN_TRANSACTION', '55')
        self.assertDictEqual(self.test_database.transaction_stack[0], {'A': '5', 'B': '4', 'C': '4'})
        self.assertDictEqual(self.test_database.database, {'A'                       : '5',
                                                           'B'                       : '4',
                                                           'C'                       : '4',
                                                           'I_AM_ONLY_IN_TRANSACTION': '55'})
        self.test_database.rollback_transaction()
        self.assertDictEqual(self.test_database.database, {'A': '5',
                                                           'B': '4',
                                                           'C': '4'})

        self.assertListEqual(self.test_database.transaction_stack, [])

    def test_commit_transaction(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}
        self.test_database.begin_transaction()
        self.test_database.set('I_AM_ONLY_IN_TRANSACTION', '55')
        self.assertDictEqual(self.test_database.database, {'A'                       : '5',
                                                           'B'                       : '4',
                                                           'C'                       : '4',
                                                           'I_AM_ONLY_IN_TRANSACTION': '55'})
        self.test_database.commit_transaction()
        self.assertDictEqual(self.test_database.database, {'A'                       : '5',
                                                           'B'                       : '4',
                                                           'C'                       : '4',
                                                           'I_AM_ONLY_IN_TRANSACTION': '55'})

        self.assertListEqual(self.test_database.transaction_stack, [])

    def test_multiple_transactions(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}
        self.test_database.begin_transaction()
        self.test_database.set('TR1', '11')
        self.test_database.begin_transaction()
        self.test_database.set('TR2', '22')
        self.test_database.begin_transaction()
        self.test_database.set('TR3', '33')

        self.assertEqual(len(self.test_database.transaction_stack), 3)

        self.test_database.commit_transaction()
        self.assertDictEqual(self.test_database.database,
                             {'A': '5', 'B': '4', 'C': '4', 'TR1': '11', 'TR2': '22', 'TR3': '33'})

        self.test_database.rollback_transaction()
        self.assertDictEqual(self.test_database.database,
                             {'A': '5', 'B': '4', 'C': '4', 'TR1': '11'})

        self.test_database.commit_transaction()
        self.assertDictEqual(self.test_database.database,
                             {'A': '5', 'B': '4', 'C': '4', 'TR1': '11'})
        self.assertListEqual(self.test_database.transaction_stack, [])

    def test_execute_command_set_get_unset(self):
        self.assertRaises(WrongInputException, self.test_database.execute_command, 'very', 'strange', 'arguments')


        self.assertDictEqual(self.test_database.database, {})
        self.test_database.execute_command(Action.SET, key='A', value='5')
        self.assertDictEqual(self.test_database.database, {'A': '5'})

        self.assertEqual(self.test_database.execute_command(Action.GET, key='A'), '5')

        self.test_database.execute_command(Action.UNSET, key='A')
        self.assertDictEqual(self.test_database.database, {})

    def test_execute_command_find_counts(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}

        self.assertEqual(self.test_database.execute_command(Action.COUNTS, value='4'),
                         self.test_database.counts('4'))

        self.assertEqual(self.test_database.execute_command(Action.FIND, value='4'),
                         " ".join(key for key in self.test_database.find('4')))

    def test_execute_command_begin_rollback_commit_transaction(self):
        self.test_database.database = {'A': '5', 'B': '4', 'C': '4'}

        self.assertEqual(len(self.test_database.transaction_stack), 0)
        self.test_database.execute_command(Action.BEGIN)
        self.assertEqual(len(self.test_database.transaction_stack), 1)
        self.test_database.set('TR1', '11')
        self.assertDictEqual(self.test_database.database, {'A': '5', 'B': '4', 'C': '4', 'TR1': '11'})
        self.test_database.execute_command(Action.ROLLBACK)
        self.assertEqual(len(self.test_database.transaction_stack), 0)
        self.assertDictEqual(self.test_database.database, {'A': '5', 'B': '4', 'C': '4'})

        self.assertEqual(len(self.test_database.transaction_stack), 0)
        self.test_database.execute_command(Action.BEGIN)
        self.assertEqual(len(self.test_database.transaction_stack), 1)
        self.test_database.set('TR2', '22')
        self.assertDictEqual(self.test_database.database, {'A': '5', 'B': '4', 'C': '4', 'TR2': '22'})
        self.test_database.execute_command(Action.COMMIT)
        self.assertEqual(len(self.test_database.transaction_stack), 0)
        self.assertDictEqual(self.test_database.database, {'A': '5', 'B': '4', 'C': '4', 'TR2': '22'})


if __name__ == '__main__':
    unittest.main()
