import datetime
from flask import Flask, render_template, url_for, redirect, request
from datastore_model import DatastoreModel

app = Flask(__name__)
model = DatastoreModel()

@app.route('/')
def root():
    return render_template(
        'index.html')

@app.route('/new')
def new():
    task_list_id = model.new_task_list()
    return redirect(url_for('task_list', task_list_id=task_list_id))

@app.route('/tasks/<int:task_list_id>')
def task_list(task_list_id):
    today = datetime.date.today()
    tasks = model.get_tasks(task_list_id)
    for task in tasks:
        task['update_link'] = url_for('update', task_list_id=task_list_id, task_id=task.id)
        task['remove_link'] = url_for('remove', task_list_id=task_list_id, task_id=task.id)
    return render_template(
        'task_list.html', tasks=tasks, task_list_id=task_list_id,
        today=today)

@app.route('/add/<int:task_list_id>', methods=['POST'])
def add(task_list_id):
    model.add_task(task_list_id,
      request.form['name'],
      int(request.form['year']),
      int(request.form['month']),
      int(request.form['day']),
      int(request.form['interval']),
    )
    return redirect(url_for('task_list', task_list_id=task_list_id))

@app.route('/update/<int:task_list_id>/<int:task_id>')
def update(task_list_id, task_id):
    model.update_task(task_list_id, task_id)
    return redirect(url_for('task_list', task_list_id=task_list_id))

@app.route('/remove/<int:task_list_id>/<int:task_id>')
def remove(task_list_id, task_id):
    model.remove_task(task_list_id, task_id)
    return redirect(url_for('task_list', task_list_id=task_list_id))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
