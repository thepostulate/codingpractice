
class ISBNValidator:
    class FormatException(Exception):
        pass

    @staticmethod
    def prepare_code_string(code_string: str) -> str:
        retval = code_string.strip()
        retval = retval.replace("-", "")
        return retval

    @staticmethod
    def validate_isbn10(code_string: str) -> bool:
        # Remove dashes from the string
        isbn_string = ISBNValidator.prepare_code_string(code_string)

        # Reject if string is wrong length, or is not numeric (including special case for digit 10)
        if len(isbn_string) != 10 or \
                not isbn_string[0:9].isnumeric() or \
                not (isbn_string[9].isnumeric() or isbn_string[9].lower() == "x"):
            return False
        checksum = 0
        for i in range(0, 10):
            if i == 9 and isbn_string[i].lower() == "x":
                digit = 10
            else:
                digit = int(isbn_string[i])
            checksum += digit * (10 - i)
        return (checksum % 11) == 0

    @staticmethod
    def validate_isbn13(code_string: str) -> bool:
        isbn_string = ISBNValidator.prepare_code_string(code_string)
        if len(isbn_string) != 13 or not isbn_string.isnumeric():
            return False
        checksum = 0
        for (count, digit) in enumerate(isbn_string):
            # Weight of 1 for even and 3 for odd digits
            weight = 1 + ((count % 2) * 2)
            checksum += (int(digit) * weight)
        return (checksum % 10) == 0

    @staticmethod
    def validate_isbn(code_string: str) -> bool:
        # Validate an ISBN of unknown format.
        isbn_string = ISBNValidator.prepare_code_string(code_string)
        if len(isbn_string) == 10:
            return ISBNValidator.validate_isbn10(isbn_string)
        elif len(isbn_string) == 13:
            return ISBNValidator.validate_isbn13(isbn_string)
        else:
            return False

    @staticmethod
    def calculate_isbn_13_checkdigit(isbn13_first12_numbers: str) -> str:
        if len(isbn13_first12_numbers) != 12 or not isbn13_first12_numbers.isnumeric():
            raise ISBNValidator.FormatException("Improper format in first 12 numbers of ISBN13")
        checksum = 0
        for (count, digit) in enumerate(isbn13_first12_numbers):
            weight = 1 + ((count % 2) * 2)
            checksum += (int(digit) * weight)
        checkdigit = (10 - (checksum % 10)) % 10
        return str(checkdigit)

    @staticmethod
    def convert_isbn_10_to_13(isbn10_code_string: str) -> str:
        if not ISBNValidator.validate_isbn10(isbn10_code_string):
            raise ISBNValidator.FormatException(f"{isbn10_code_string} is not a valid ISBN-10 code string.")

        # Remove the dashes and spaces from the code string and drop the check digit
        new_isbn = ISBNValidator.prepare_code_string(isbn10_code_string)[0:9]
        new_isbn = "978" + new_isbn
        check_digit = ISBNValidator.calculate_isbn_13_checkdigit(new_isbn)
        new_isbn += check_digit
        return new_isbn


if __name__ == '__main__':
    pass
