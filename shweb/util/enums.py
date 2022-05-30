"""Енумы необходимые для разных частей системы"""
import enum
from enum import Enum


class AuthStatus(Enum):
    VALID = 'valid'  # все хорошо
    INVALID = 'invalid'  # токен некорректный
    EXPIRED = 'expired'  # токен истек
    INVALID_AUD = 'invalid_aud'  # нет доступа
    EMPTY = 'empty'  # переданы пустые креды
    LIMIT = 'limit'  # количество попыток исчерпано
    CHANGE_PASSWORD = 'force_change_password'  # необходимо сменить пароль


class ReleaseType(enum.Enum):
    SINGLE = "Single"
    ALBUM = "Album"
    EP = "EP"
