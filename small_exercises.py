class ISBNValidator:

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


if __name__ == '__main__':
    pass
