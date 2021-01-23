from unittest import TestCase
from small_exercises import ChecksumCalculator


class TestChecksumCalculator(TestCase):
    test_data_isbn10 = {
        "123": False,
        "0136091814": True,
        "1616550416": False,
        "0553418025": True,
        "3859574859": False,
        "155404295X": True,
        "1-55404-295-X": True,
        "1-55404-294-X": False
    }
    test_data_isbn13 = {
        "123": False,
        # A valid isbn10 should not work
        "0136091814": False,
        "978-1-86197-876-9": True,
        "978-1-56619-909-4": True,
        "9781566199094": True,
        "9781566199092": False,
        "978156619909X": False,
        # Leading or trailing spaces should work
        " 9781566199094": True,
        " 9781566199094 ": True
    }

    test_data_convert_10_to_13 = {
        "0201882957": "9780201882957",
        "1420951300": "9781420951301",
        "0452284236": "9780452284234",
        "1292101768": "9781292101767",
        "0345391802": "9780345391803",
        "0-34539-180-2": "9780345391803"
    }

    test_data_isbn_13_checkdigit = {
        "978186197876": "9",
        "978156619909": "4",
        "978129210176": "7"
    }

    test_data_upc_checkdigit = {
        "79603011497": "7",
        "08716214312": "7",
    }

    test_data_upc = {
        "087162143127": True,
        "087162143128": False,
        "796030114977": True,
        "0 36000 29145 2": True,
        "123": False,

    }

    def test_validate_isbn10(self):
        for (code_string, valid) in TestChecksumCalculator.test_data_isbn10.items():
            result = ChecksumCalculator.validate_isbn10(code_string=code_string)
            self.assertEqual(valid, result)

    def test_validate_isbn13(self):
        for (code_string, valid) in TestChecksumCalculator.test_data_isbn13.items():
            result = ChecksumCalculator.validate_isbn13(code_string=code_string)
            self.assertEqual(valid, result)

    def test_validate_isbn(self):
        # The last literal in this dictionary resets the valid ISBN-10 to true (which is a false case in test_data_isbn13)
        items_to_test = {**TestChecksumCalculator.test_data_isbn10,
                         **TestChecksumCalculator.test_data_isbn13,
                         "0136091814": True}
        for (code_string, valid) in items_to_test.items():
            result = ChecksumCalculator.validate_isbn(code_string=code_string)
            self.assertEqual(valid, result)

    def test_convert_isbn_10_to_13(self):
        for (isbn_10, isbn_13) in TestChecksumCalculator.test_data_convert_10_to_13.items():
            result = ChecksumCalculator.convert_isbn_10_to_13(isbn_10)
            self.assertEqual(isbn_13, result)
        # Test invalid input
        invalid_isbn_10 = "1-55404-294-X"
        with self.assertRaises(ChecksumCalculator.FormatException):
            ChecksumCalculator.convert_isbn_10_to_13(invalid_isbn_10)

    def test_calculate_isbn_13_checkdigit(self):
        # Check valid conversions
        for (first_12_digits, checkdigit) in TestChecksumCalculator.test_data_isbn_13_checkdigit.items():
            result = ChecksumCalculator.calculate_isbn_13_checkdigit(first_12_digits)
            self.assertEqual(checkdigit, result)
        # Test invalid input - Improper length
        with self.assertRaises(ChecksumCalculator.FormatException):
            ChecksumCalculator.calculate_isbn_13_checkdigit("123")
        # Test invalid input - Code with dashes
        with self.assertRaises(ChecksumCalculator.FormatException):
            ChecksumCalculator.calculate_isbn_13_checkdigit("978-1-86197-")

    def test_calculate_upc_checkdigit(self):
        for (first_11_digits, checkdigit) in TestChecksumCalculator.test_data_upc_checkdigit.items():
            result = ChecksumCalculator.calculate_upc_checkdigit(first_11_digits)
            self.assertEqual(checkdigit, result)
        with self.assertRaises(ChecksumCalculator.FormatException):
            ChecksumCalculator.calculate_upc_checkdigit("0871X2143127")

    def test_validate_upc(self):
        for (code_string, valid) in TestChecksumCalculator.test_data_upc.items():
            result = ChecksumCalculator.validate_upc(code_string)
            self.assertEqual(valid, result)

