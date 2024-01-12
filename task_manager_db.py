import asyncio
import functools
import time
from typing import Any, Callable

import cloudpickle
from peewee import BlobField
from playhouse.sqlite_ext import SqliteExtDatabase



db=SqliteExtDatabase('tasks_db.sqlite',pragmas={'foreign_keys':1})



class CloudPickleField(BlobField):
    def python_value(self, value):
        if value is not None:
            return cloudpickle.loads(value)

    def db_value(self, value):
        if value is not None:
            return cloudpickle.dumps(value)
from peewee import Model, CharField, ForeignKeyField, DateTimeField
from datetime import datetime
class TaskManager(Model):

    created_at = DateTimeField(default=datetime.now)
    first_run=False
    name=CharField(primary_key=True)
    task_callbacks=[]


    async def start_tasks(self):
        callbacks=self.task_callbacks
        while True:
            # Логика запуска задач
            if self.first_run:
                self.tasks.update(status='pending').where(BaseTask.status=='in_progress').execute()
            task_to_run=self.tasks.where(BaseTask.status=='pending')[:]
            tasks=[]
            for t in task_to_run:
                t.status='pending'
                t.save()
                task=asyncio.create_task( self.run_task(callbacks, t))
                tasks.append(task)
            st_time=time.time()
            await asyncio.gather(*tasks)
            await asyncio.sleep(10-(time.time()-st_time))

    async def run_task(self, callbacks, t):
        res = await t.run()
        if callbacks:
            for callback in callbacks:
                t = callback(res)
                if asyncio.iscoroutine(t):
                    t = await t

    def to_task(self, func: Any, *args, **kwargs):
        self.add_task(args, func, kwargs)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    def add_task(self, args, func, kwargs):
        task = BaseTask.create(parent=self, run_function=functools.partial(func, *args, **kwargs))


    def task(manager,func: Callable):
        @functools.wraps(func)
        def wrapper( *args, **kwargs):

            task = BaseTask.create(parent=manager, run_function=functools.partial(func, *args, **kwargs))
            return task

        return wrapper

    @classmethod
    def instance(cls,name,callback=None)->'TaskManager':

        callbacks = [callback] if callback else None

        t,_=cls.get_or_create(name=name)
        t.task_callbacks=callbacks
        return t
    class Meta:

        database=db


class BaseTask(Model):
    parent = ForeignKeyField(TaskManager,backref='tasks')
    status = CharField(default='pending')
    result = CloudPickleField(null=True)
    run_function=CloudPickleField(null=True)
    async def run(self):
        if self.run_function:
            run=self.run_function
        else:
            run=self.start

        if asyncio.iscoroutinefunction(run):
            r=await run()
        else:
            r=await asyncio.get_running_loop().run_in_executor(None, run)
            if asyncio.iscoroutine(r):
                r=await r
            elif asyncio.iscoroutinefunction(r):
                r=await r()
        self.result=r
        self.status='completed'
        self.save()
        return r
    async def start(self):
        raise NotImplemented
    def __str__(self):
        f= self.result
        if f:
            res = [str(item) for sublist in f for item in (sublist if isinstance(sublist, list) else [sublist])]
            return '\n'.join(res)
        return ''
    class Meta:
        database = db


def async_callback_wrapper(async_func, *args, **kwargs):
    @functools.wraps(async_func)
    async def wrapped():
        return await async_func(*args, **kwargs)
    return wrapped