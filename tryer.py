class TryExecutor:
    def __init__(self, try_func):
        self.try_func = try_func
        self.exception_handler = None
        self.else_action = None
        self.final_action = None
        self.result = None
        self.exception = None

    def except_(self, exception_handler):
        self.exception_handler = exception_handler
        return self

    def else_(self, else_action):
        self.else_action = else_action
        return self

    def finally_(self, final_action):
        self.final_action = final_action
        return self

    def execute(self):
        try:
            self.result = self.try_func()
        except Exception as e:
            self.exception = e
            if self.exception_handler:
                self.exception_handler(e)
        else:
            if self.else_action:
                self.else_action()
        finally:
            if self.final_action:
                self.final_action()

        return self.result

# Пример использования
# try_executor = TryExecutor(lambda: get_attribute_x_of(clss_x))
# result = (try_executor
#             .except_(lambda err: logger.exception(err))
#             .else_(lambda: setattr(clss_x, 'good', True))
#             .finally_(lambda: clear_resources(clss_x))
#             .execute())
