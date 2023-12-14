import asyncio
import inspect

class AsyncChain:
    def __init__(self):
        self.tasks = []
        self.on_complete_handler = None
        self.error_handler = None

    async def run(self):
        result = None
        for task in self.tasks:
            try:
                if inspect.iscoroutinefunction(task):
                    if inspect.signature(task).parameters:
                        result = await task(result)
                    else:
                        result = await task()
                else:
                    if inspect.signature(task).parameters:
                        result = task(result)
                    else:
                        result = task()
            except Exception as e:
                if self.error_handler:
                    await self.error_handler(e)
                else:
                    raise e

        if self.on_complete_handler:
            if inspect.iscoroutinefunction(self.on_complete_handler):
                if inspect.signature(self.on_complete_handler).parameters:
                    result = await self.on_complete_handler(result)
                else:
                    result = await self.on_complete_handler()
            else:
                if inspect.signature(self.on_complete_handler).parameters:
                    result = self.on_complete_handler(result)
                else:
                    result = self.on_complete_handler()

        return result

    def add(self, func):
        self.tasks.append(func)
        return self

    def on_complete(self, func):
        self.on_complete_handler = func
        return self

    def on_error(self, func):
        self.error_handler = func
        return self

    def add_delay(self, seconds):
        async def delay(_):
            await asyncio.sleep(seconds)
        self.tasks.append(delay)
        return self

    def add_condition_wait(self, condition_func, timeout=None):
        async def wait_condition(_):
            start_time = asyncio.get_event_loop().time()
            while not condition_func():
                if timeout and (asyncio.get_event_loop().time() - start_time) > timeout:
                    raise TimeoutError("Condition wait timed out")
                await asyncio.sleep(0.1)
        self.tasks.append(wait_condition)
        return self

# Пример использования

async def first_task(_):
    return 5

def second_task(x):
    return x * 2

async def final_handler(result):
    return result + 1

def condition_func():
    # Пример условия, которое должно быть выполнено
    return True

async def main():
    chain = AsyncChain()
    result = await (chain.add(first_task)
                       .add_delay(1)  # задержка 1 секунда
                       .add(second_task)
                       .add_condition_wait(condition_func, timeout=5)  # ждать выполнения условия
                       .on_complete(final_handler)
                       .run())
    print(f"Result: {result}")
if __name__ == '__main__':

    asyncio.run(main())
