import asyncio
import time
import traceback

from config.config import bot
from demiurgelib.task_manager_db import  TaskManager, BaseTask

##EXAMPLE USAGE
TaskManager.create_table(True)
BaseTask.create_table(True)

async def send_message(x):
    await bot.send_message(chat_id=5170895847, text=x)
async def test_result(x):
    assert x==4

manager=TaskManager.instance(name='example', callback=send_message)
manager.task_callbacks+= [test_result]
@manager.task
def long_function(x):
    time.sleep(4)
    return x*x


def long_function2(x):
    time.sleep(4)
    return x+x


@manager.task
async def long_function3(x):
    await asyncio.sleep(4)
    return x*x


async def long_function4(x):
    await asyncio.sleep(4)
    return x+x


async def test_main():
    try:
        t=long_function(2)
        t2=manager.to_task(lambda :long_function2(2))
        t = long_function3(2)
        t2 = manager.to_task(lambda: long_function4(2))
        await manager.start_tasks()
    except:
        traceback.print_exc()


if __name__ == '__main__':

    asyncio.run(test_main())