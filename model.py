class Model:
    def new_task_list(self):
        raise NotImeplementedError
    def get_tasks(self):
        raise NotImeplementedError
    def add_task(self, name, start_date, interval):
        raise NotImeplementedError
    def update_task(self, task_list_id, task_id):
        raise NotImeplementedError
    def remove_task(self, task_list_id, task_id):
        raise NotImeplementedError
    def pause_task(self, task_list_id, task_id):
        raise NotImeplementedError
    def resume_task(self, task_list_id, task_id):
        raise NotImeplementedError
    def get_histories(self, task_list_id, task_id):
        raise NotImeplementedError

class UnknownTaskListError(RuntimeError): pass
