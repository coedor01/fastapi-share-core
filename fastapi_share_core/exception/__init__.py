from fastapi_share_core.exception.error import BaseEC


class ConfigException(Exception): ...


class BusinessException(Exception):
    def __init__(self, ec: BaseEC):
        self.code = ec.get_code()
        self.msg = ec.get_msg()


class ServerException(Exception): ...
