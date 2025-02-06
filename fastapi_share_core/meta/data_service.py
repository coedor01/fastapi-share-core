from fastapi_share_core.meta.singleton import ThreadUnsafeSingletonMeta


class DataServiceMeta(ThreadUnsafeSingletonMeta):

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        # 从 kwargs 中获取 model 参数并设置为类属性
        if 'model' in kwargs:
            cls.model = kwargs['model']

        return cls
