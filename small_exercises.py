
class ChecksumCalculator:
    class FormatException(Exception):
        pass

    @staticmethod
    def prepare_code_string(code_string: str) -> str:
        retval = code_string.replace("-", "")
        retval = retval.replace(" ", "")
        return retval

    @staticmethod
    def calc_weighted_sum_check_digit(code_string: str, weight_array: [int], modulus: int = 10) -> int:
        """
        Returns the proper check digit for a codestring, calculated using a weighted sum mechanism

        Parameters:
            code_string: a string of integer digits for which a check digit is desired
            weight_array: an array of integers containing the "weight" by which each digit should be multiplied.
                          This array is used in a circular manner, so for the array [1, 3], the weights applied would
                          be 1, 3, 1, 3, 1, 3... until there are no more numbers in the code_string.
            modulus: the modulus to use in the calculation.  0 <= value_returned < modulus

        Returns:
            An integer between 0 and modulus, representing the "checkdigit."  Note: If the modulus is > 10, this
            checkdigit could actually consist of two or more integer digits -- with modulus = 11, 10 is a valid
            "checkdigit"
        """
        num_weights = len(weight_array)
        checksum = 0
        for (count, digit) in enumerate(code_string):
            weight = weight_array[count % num_weights]
            checksum += (int(digit) * weight)
        check_digit = (modulus - (checksum % modulus)) % modulus
        return check_digit

    @staticmethod
    def validate_isbn10(code_string: str) -> bool:
        # Remove dashes from the string
        isbn_string = ChecksumCalculator.prepare_code_string(code_string)
        # Reject if string is wrong length, or is not numeric (including special case for digit 10)
        if len(isbn_string) != 10 or \
                not isbn_string[0:9].isnumeric() or \
                not (isbn_string[9].isnumeric() or isbn_string[9].lower() == "x"):
            return False
        check_digit = ChecksumCalculator.calc_weighted_sum_check_digit(code_string=isbn_string[0:9],
                                                                       weight_array=[10, 9, 8, 7, 6, 5, 4, 3, 2],
                                                                       modulus=11)
        check_digit = str(check_digit) if check_digit < 10 else "x"
        return isbn_string[9].lower() == check_digit

    @staticmethod
    def validate_isbn13(code_string: str) -> bool:
        isbn_string = ChecksumCalculator.prepare_code_string(code_string)
        if len(isbn_string) != 13 or not isbn_string.isnumeric():
            return False
        check_digit = ChecksumCalculator.calculate_isbn_13_checkdigit(isbn_string[:12])
        return str(check_digit) == isbn_string[12]

    @staticmethod
    def validate_isbn(code_string: str) -> bool:
        # Validate an ISBN of unknown format.
        isbn_string = ChecksumCalculator.prepare_code_string(code_string)
        if len(isbn_string) == 10:
            return ChecksumCalculator.validate_isbn10(isbn_string)
        elif len(isbn_string) == 13:
            return ChecksumCalculator.validate_isbn13(isbn_string)
        else:
            return False

    @staticmethod
    def calculate_isbn_13_checkdigit(isbn13_first12_numbers: str) -> str:
        if len(isbn13_first12_numbers) != 12 or not isbn13_first12_numbers.isnumeric():
            raise ChecksumCalculator.FormatException("Improper format in first 12 numbers of ISBN13")
        check_digit = ChecksumCalculator.calc_weighted_sum_check_digit(code_string=isbn13_first12_numbers,
                                                                       weight_array=[1, 3],
                                                                       modulus=10)
        return str(check_digit)

    @staticmethod
    def convert_isbn_10_to_13(isbn10_code_string: str) -> str:
        if not ChecksumCalculator.validate_isbn10(isbn10_code_string):
            raise ChecksumCalculator.FormatException(f"{isbn10_code_string} is not a valid ISBN-10 code string.")

        # Remove the dashes and spaces from the code string and drop the check digit
        new_isbn = ChecksumCalculator.prepare_code_string(isbn10_code_string)[0:9]
        new_isbn = "978" + new_isbn
        check_digit = ChecksumCalculator.calculate_isbn_13_checkdigit(new_isbn)
        new_isbn += check_digit
        return new_isbn

    @staticmethod
    def calculate_upc_checkdigit(first_11_numbers: str) -> str:
        if len(first_11_numbers) != 11 or not first_11_numbers.isnumeric():
            raise ChecksumCalculator.FormatException("Improper format in first 11 numbers of UPC")
        check_digit = ChecksumCalculator.calc_weighted_sum_check_digit(code_string=first_11_numbers,
                                                                       weight_array=[3, 1],
                                                                       modulus=10)
        return str(check_digit)

    @staticmethod
    def validate_upc(code_string: str) -> bool:
        upc_string = ChecksumCalculator.prepare_code_string(code_string)
        if len(upc_string) != 12:
            return False
        retval = ChecksumCalculator.calculate_upc_checkdigit(upc_string[:-1]) == upc_string[-1:]
        return retval


if __name__ == '__main__':
    pass
