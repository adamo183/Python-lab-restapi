from fastapi import APIRouter
from Functions.number import Number

controlerName = "prime"
numberController = APIRouter()

numberFunc = Number()


@numberController.get(f'/{controlerName}/{{number}}')
def isPrimeNumber(number: int):
    if not numberFunc.checkIsNumberValid(number):
        return "Bad request", 400
    if numberFunc.checkIsNumberPrime(number):
        primeRespone = f"{number} is prime number"
    else:
        primeRespone = f"{number} is not a prime number"
    return primeRespone, 200
