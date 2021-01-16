from unittest import TestCase
from small_exercises import ISBNValidator


class TestISBNValidator(TestCase):
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

    def test_validate_isbn10(self):
        for (code_string, valid) in TestISBNValidator.test_data_isbn10.items():
            result = ISBNValidator.validate_isbn10(code_string=code_string)
            self.assertEqual(result, valid)

    def test_validate_isbn13(self):
        for (code_string, valid) in TestISBNValidator.test_data_isbn13.items():
            result = ISBNValidator.validate_isbn13(code_string=code_string)
            self.assertEqual(result, valid)
