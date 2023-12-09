class ConditionalExecutor:
    def __init__(self):
        self.conditions = []
        self.actions = []
        self.final_action = None
        self.exception_action = None
        self.continue_after_error = False
        self.log_exceptions = False

    def if_(self, condition):
        self.conditions.append(condition)
        return self

    def then(self, action):
        self.actions.append((self.conditions[-1], action))
        return self

    def elif_(self, condition):
        self.conditions.append(condition)
        return self

    def else_(self, action):
        self.else_action = action
        return self

    def finally_(self, action):
        self.final_action = action
        return self

    def on_except(self, exception_type, log=False, continue_after_error=False):
        self.exception_action = (exception_type, log, continue_after_error)
        return self

    def execute(self):
        try:
            for condition, action in self.actions:
                if condition():
                    action()
                    break
            else:
                if self.else_action:
                    self.else_action()
        except Exception as e:
            if self.exception_action:
                exception_type, log, continue_after_error = self.exception_action
                if isinstance(e, exception_type):
                    if log:
                        print(f"Error: {e}")
                    if not continue_after_error:
                        return
        finally:
            if self.final_action:
                self.final_action()

# Пример использования
# executor = ConditionalExecutor()
# (executor
#     .if_(lambda: customa > b and b > 5)
#     .then(lambda: func_a())
#     .elif_(lambda: funcb_condition)
#     .else_(func)
#     .finally_(clear_f)
#     .on_except(Exception, log=True, continue_after_error=True)
#     .execute())
