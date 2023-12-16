import os
import sqlite3

import pygame

from constants import MEDIA_URL, DB_URL


def load_image(image_name):
    return pygame.image.load(os.path.join(MEDIA_URL, image_name)).convert_alpha()


class DataBase:

    def __init__(self):
        self._cursor = self._get_cursor()

    @staticmethod
    def _get_cursor():
        with sqlite3.connect(DB_URL) as connection:
            return connection.cursor()

    def _commit(self):
        self._cursor.connection.commit()
