class BaseModel:
    @classmethod
    def before_create(cls, *args, **kwargs):
        pass

    @classmethod
    def after_create(cls, *args, **kwargs):
        pass

    @classmethod
    def before_update(cls, *args, **kwargs):
        pass

    @classmethod
    def after_update(cls, *args, **kwargs):
        pass
