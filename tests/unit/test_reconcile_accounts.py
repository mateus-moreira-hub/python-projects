import datetime as dt
import unittest
from scripts.reconcile_accounts import (
    Account, 
    AccountsReadingConfig, 
    AccountsMatchingConfig, 
    reconcile_accounts, 
    ReconcileAccountsConfig
)

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.base_list_data = [
            "2020-12-04",
            "Tecnologia",
            "16.00",
            "Bitbucket"
        ]
        self.base_account_object = Account(
            date=dt.date(2020, 12, 4),
            department="Tecnologia",
            value=16.00,
            beneficiary="Bitbucket",
            value_decimal_places=2
        )

    def test_from_list(self):
        config = AccountsReadingConfig()
        config.columns_order = ["date", "department", "value", "beneficiary"]
        config.date_format = "%Y-%m-%d"
        self.assertEqual(Account().from_list(self.base_list_data, config), self.base_account_object)

    def test_to_list(self):
        self.assertEqual(self.base_account_object.to_list(), self.base_list_data + ["MISSING"])

    def test_match_1(self):
        config = AccountsMatchingConfig()
        config.float_decimal_places = 10
        config.is_case_sensitive = True
        config.plus_or_minus_days_tolerance = 1
        other_account = Account(
            date=dt.date(2020, 12, 5),
            department="Tecnologia",
            value=16.00,
            beneficiary="Bitbucket"
        )
        self.assertEqual(self.base_account_object.match(other_account, config), True)

    def test_match_2(self):
        config = AccountsMatchingConfig()
        config.float_decimal_places = 10
        config.is_case_sensitive = True
        config.plus_or_minus_days_tolerance = 1
        other_account = Account(
            date=dt.date(2020, 12, 3),
            department="Tecnologia",
            value=16.00,
            beneficiary="Bitbucket"
        )
        self.assertEqual(self.base_account_object.match(other_account, config), True)

    def test_match_3(self):
        config = AccountsMatchingConfig()
        config.float_decimal_places = 10
        config.is_case_sensitive = True
        config.plus_or_minus_days_tolerance = 1
        other_account = Account(
            date=dt.date(2020, 12, 4),
            department="TECNOLOGIA",
            value=16.00,
            beneficiary="Bitbucket"
        )
        self.assertEqual(self.base_account_object.match(other_account, config), False)

    def test_main_func(self):
        rconfig = AccountsReadingConfig()
        rconfig.columns_order = ["date", "department", "value", "beneficiary"]
        rconfig.date_format = "%Y-%m-%d"

        mconfig = AccountsMatchingConfig()
        mconfig.float_decimal_places = 10
        mconfig.is_case_sensitive = True
        mconfig.plus_or_minus_days_tolerance = 1

        config = ReconcileAccountsConfig()
        config.accounts_reading_config = rconfig
        config.accounts_matching_config = mconfig

        transactions1 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket"],
            ["2020-12-04","Jurídico","60.00","LinkSquares"],
            ["2020-12-05","Tecnologia","50.00","AWS"]
        ]
        transactions2 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket"],
            ["2020-12-05","Tecnologia","49.99","AWS"],
            ["2020-12-04","Jurídico","60.00","LinkSquares"]
        ]
        expected_out1 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket", "FOUND"],
            ["2020-12-04","Jurídico","60.00","LinkSquares", "FOUND"],
            ["2020-12-05","Tecnologia","50.00","AWS", "MISSING"]
        ]
        expected_out2 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket", "FOUND"],
            ["2020-12-05","Tecnologia","49.99","AWS", "MISSING"],
            ["2020-12-04","Jurídico","60.00","LinkSquares", "FOUND"]
        ]
        self.assertEqual(reconcile_accounts(transactions1, transactions2), (expected_out1, expected_out2))

    def test_main_func_duplicates(self):
        rconfig = AccountsReadingConfig()
        rconfig.columns_order = ["date", "department", "value", "beneficiary"]
        rconfig.date_format = "%Y-%m-%d"

        mconfig = AccountsMatchingConfig()
        mconfig.float_decimal_places = 10
        mconfig.is_case_sensitive = True
        mconfig.plus_or_minus_days_tolerance = 1

        config = ReconcileAccountsConfig()
        config.accounts_reading_config = rconfig
        config.accounts_matching_config = mconfig

        transactions1 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket"],
            ["2020-12-05","Tecnologia","16.00","Bitbucket"],
            ["2020-12-05","Tecnologia","50.00","AWS"]
        ]
        transactions2 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket"],
            ["2020-12-05","Tecnologia","49.99","AWS"],
            ["2020-12-04","Jurídico","60.00","LinkSquares"]
        ]
        expected_out1 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket", "FOUND"],
            ["2020-12-05","Tecnologia","16.00","Bitbucket", "MISSING"],
            ["2020-12-05","Tecnologia","50.00","AWS", "MISSING"]
        ]
        expected_out2 = [
            ["2020-12-04","Tecnologia","16.00","Bitbucket", "FOUND"],
            ["2020-12-05","Tecnologia","49.99","AWS", "MISSING"],
            ["2020-12-04","Jurídico","60.00","LinkSquares", "MISSING"]
        ]
        self.assertEqual(reconcile_accounts(transactions1, transactions2), (expected_out1, expected_out2))

if __name__=="__main__":
    unittest.main()