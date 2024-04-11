from cryptography.fernet import Fernet
from src.config import ENCRYPTION_KEY


class BaseCrypto:
    __function: Fernet

    def __init__(self, key: bytes):
        self.__function = Fernet(key)

    def encrypt(self, data: bytes):
        token = self.__function.encrypt(data)
        return token.decode("utf-8")

    def decrypt(self, token: str):
        data = self.__function.decrypt(token.encode("utf-8"))
        return data.decode()


client = BaseCrypto(ENCRYPTION_KEY.encode("utf-8"))
