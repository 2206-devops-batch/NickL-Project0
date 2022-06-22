import unittest

from account_functions import deposit
from project_0 import Account

class AccountFunctionalityTest(unittest.TestCase):
    
    def test_deposit(self):
        initial = 0
        account = Account("TestAccount", initial)
        deposit = 100
        account.make_deposit(deposit)
        expected = initial + deposit
        actual = account.get_value()
        self.assertEqual(actual, expected)

    def test_withdrawl(self):
        initial = 100
        account = Account("TestAccount", initial)
        withdrawal = 47
        account.make_withdrawal(withdrawal)
        expected = initial - withdrawal
        actual = account.get_value()
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()