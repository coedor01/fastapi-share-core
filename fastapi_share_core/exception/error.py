from enum import Enum


class BaseEC(Enum):
    def __init__(self, code: int, msg: str):
        self._code = code
        self._msg = msg

    def get_code(self) -> int:
        return self._code

    def get_msg(self):
        return self._msg
