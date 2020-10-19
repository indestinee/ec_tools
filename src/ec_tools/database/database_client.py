class DatabaseClient:
    def __init__(self):
        pass

    def execute(self, *args, **kwargs):
        raise NotImplementedError

    def commit(self):
        raise NotImplementedError
