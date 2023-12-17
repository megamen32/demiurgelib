class TryExecutor:
    def __init__(self, try_func):
        self.try_func = try_func
        self.exception_handler = None
        self.else_action = None
        self.final_action = None
        self.result = None
        self.exception = None
        self._repeat=None
        self.repeat_err=None
        self._repeat_step=0

    def repeat(self,times,err=Exception):
        self._repeat=times
        self.repeat_err=err
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
        res,final,else_,exc=None,None,None,None
        while True:
            try:
                res=self.result = self.try_func()

            except Exception as e:
                self.exception = e
                if self.exception_handler:
                    exc=self.exception_handler(e)
                if self._repeat:
                    self._repeat_step+=1
                    if self._repeat_step>self._repeat:
                        break
                    continue
                else:
                    break
            else:
                if self.else_action:
                    else_=self.else_action()
            finally:
                if self.final_action:
                    final=self.final_action()
        return res



# Пример использования
# try_executor = TryExecutor(lambda: get_attribute_x_of(clss_x))
# result = (try_executor
#             .except_(lambda err: logger.exception(err))
#             .else_(lambda: setattr(clss_x, 'good', True))
#             .finally_(lambda: clear_resources(clss_x))
#             .execute())
