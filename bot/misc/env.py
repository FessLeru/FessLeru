import os
from abc import ABC
from typing import Final


class EnvKeys(ABC):
    TOKEN: Final = '7208443080:AAEh7p5pDxaGeW78k3wY3Wt85PfbIBNmlhY'
    OWNER: Final = ('1899077005', '6517930437', '935351006')
    CLIENT_TOKEN: Final = 'AgAAAAA2zr9wAAaV0UJ0eOq4r9W0f5aDcQ'
    RECEIVER_TOKEN: Final = 'AgAAAAA2zr9wAAaV0UJ0eOq4r9W0f5aDcQ'
    DB_USERNAME: Final = 'postgres'
    DB_PASSWORD: Final = '1234'
    DB_HOST: Final = 'localhost'
    DB_NAME: Final = 'cryptomus'
