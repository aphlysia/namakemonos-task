from datetime import datetime, timezone, timedelta
from model import *
from google.cloud import datastore

class DatastoreModel(Model):
    task_list_kind = 'task_list'
    task_kind = 'task'
    history_kind = 'history'

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
            start_date = datetime(
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
                'status': 'running',
            })
            self.client.put(task)
        return task.key.id

    def get_task(self, task_list_id, task_id):
        task_list = self.get_task_list(task_list_id)
        key = self.client.key(self.task_kind, task_id, parent=task_list.key)
        return self.client.get(key)

    def update_task(self, task_list_id, task_id, message):
        with self.client.transaction():
            task = self.get_task(task_list_id, task_id)
            self.add_history(task_id, task, message)
            task['next_date'] = datetime.now()  \
                + timedelta(days=task['interval'])
            self.client.put(task)

    def add_history(self, task_id, task, message):
        key = self.client.key(self.history_kind, parent=task.key)
        history = datastore.Entity(key=key)
        history.update({
            'message': message,
            'time': datetime.now(),
        })
        self.client.put(history)

    def remove_task(self, task_list_id, task_id):
        with self.client.transaction():
            task_list = self.get_task_list(task_list_id)
            key = self.client.key(self.task_kind, task_id,
                parent=task_list.key)
            self.client.delete(key)

    def pause_task(self, task_list_id, task_id):
        with self.client.transaction():
            task = self.get_task(task_list_id, task_id)
            task['status'] = 'pausing'
            self.client.put(task)

    def resume_task(self, task_list_id, task_id):
        with self.client.transaction():
            task = self.get_task(task_list_id, task_id)
            task['status'] = 'running'
            now = datetime.now(timezone.utc)
            if now > task['next_date']:
                task['next_date'] = now
            self.client.put(task)

    def sort(self, tasks):
        return sorted(tasks, key=lambda e: e['next_date'])

    def get_tasks(self, task_list_id):
        task_list_key = self.client.key(self.task_list_kind, task_list_id)
        query = self.client.query(kind=self.task_kind,
            ancestor=task_list_key)
        tasks = list(query.fetch())
        running_tasks = [t for t in tasks if t['status'] != 'pausing']
        pausing_tasks = [t for t in tasks if t['status'] == 'pausing']
        return self.sort(running_tasks) + self.sort(pausing_tasks)

    def get_histories(self, task_list_id, task_id):
        task = self.get_task(task_list_id, task_id)
        '''
        key = self.client.key(self.history_kind,
            {'task_list': task_list_id, 'task': task_id},
            parent=task.key)
        '''
        #key = self.client.key(self.task_kind, task_id)
        #key = self.client.key(self.task_kind, task_id, parent=task_list.key)
        query = self.client.query(kind=self.history_kind,
            ancestor=task.key)
        histories = list(query.fetch())
        return sorted(histories, key=lambda e: e['time'], reverse=True)
