import datetime
from model import *
from google.cloud import datastore

class DatastoreModel(Model):
    task_list_kind = 'task_list'
    task_kind = 'task'

    def __init__(self):
        self.client = datastore.Client()

    def new_task_list(self):
        '''
        Returns task list id.
        '''
        with self.client.transaction():
            key = self.client.key(self.task_list_kind)
            task_list = datastore.Entity(key=key)
            self.client.put(task_list)
        return task_list.key.id

    def get_task_list(self, task_list_id):
        key = self.client.key(self.task_list_kind, task_list_id)
        task_list = self.client.get(key)
        if task_list is None:
            raise UnknownTaskListError
        return task_list

    def add_task(self, task_list_id, name, start_year, start_month, start_day, interval):
        '''
        Returns task id.
        '''
        with self.client.transaction():
            task_list = self.get_task_list(task_list_id)
            start_date = datetime.datetime(
                 year=start_year,
                 month=start_month,
                 day=start_day,
            )
            key = self.client.key(self.task_kind, parent=task_list.key)
            task = datastore.Entity(key=key)
            task.update({
                'name': name,
                'next_date': start_date,
                'interval': interval,
            })
            self.client.put(task)
        return task.key.id

    def get_task(self, task_list_id, task_id):
        task_list = self.get_task_list(task_list_id)
        key = self.client.key(self.task_kind, task_id, parent=task_list.key)
        return self.client.get(key)

    def update_task(self, task_list_id, task_id):
        with self.client.transaction():
            task = self.get_task(task_list_id, task_id)
            task['next_date'] = datetime.datetime.now()  \
                + datetime.timedelta(days=task['interval'])
            self.client.put(task)

    def remove_task(self, task_list_id, task_id):
        with self.client.transaction():
            task_list = self.get_task_list(task_list_id)
            key = self.client.key(self.task_kind, task_id,
                parent=task_list.key)
            self.client.delete(key)

    def get_tasks(self, task_list_id):
        task_list_key = self.client.key(self.task_list_kind, task_list_id)
        query = self.client.query(kind=self.task_kind,
            ancestor=task_list_key)
        return sorted(query.fetch(), key=lambda e: e['next_date'])

