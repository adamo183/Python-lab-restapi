import sympy

class Number:
    def checkIsNumberPrime(self, number) -> bool:
        return sympy.isprime(number)

    def checkIsNumberValid(self, number) -> bool:
        if number > 9223372036854775807 or number < 0:
            return False
        else:
            return True