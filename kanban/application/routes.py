from flask import render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask import current_app as app
from datetime import datetime
from application import db
import os, sys

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    
    return url_for(endpoint, **values)

class Tasks(db.Model):
    task_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    details = db.Column(db.String(100), nullable=True)
    start_date = db.Column(db.DateTime('%Y-%m-%d %H:%M'), nullable=True)
    due_date = db.Column(db.DateTime('%Y-%m-%d %H:%M'), nullable=True)
    end_date = db.Column(db.DateTime('%Y-%m-%d %H:%M'), nullable=True)
    state = db.Column(db.String(10))

@app.route('/')
def index():
    do = Tasks.query.filter_by(state='do').all()
    doing = Tasks.query.filter_by(state='doing').all()
    done = Tasks.query.filter_by(state='done').all()
    deleted = Tasks.query.filter_by(state='deleted').all()
    
    return render_template('index.html', do=do, doing=doing, done=done, deleted=deleted)
    
@app.route('/add/<category>', methods=['GET', 'POST'])
def add(category):
    
    start_date = None
    end_date = None
    
    if category == 'add-do':
        state = "do"
    elif category == 'add-doing':
        state = "doing"
        start_date = datetime.now()
    elif category == 'add-done':
        state = "done"
        end_date = datetime.now()
    
    name = request.form['name']
    details = request.form['details']
    due_date = datetime.strptime(request.form.get('due_date'), '%Y-%m-%dT%H:%M')

    task = Tasks(name=name, details=details, due_date=due_date, end_date=end_date, state=state)
    
    db.session.add(task)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/move/<category>/<task_id>', methods=['GET'])
def move(category, task_id):
    
    task = Tasks.query.filter_by(task_id=int(task_id)).one()
    
    if category == 'move-do':
        state = "do"
        task.start_date = None
    elif category == 'move-doing':
        state = "doing"
        if task.start_date == None: #task hasn't been started yet
            task.start_date = datetime.now()
        if task.start_date != None: #task has started already
            end_date = None
    elif category == 'move-done':
        state = "done"
        task.end_date = datetime.now()
        if task.start_date == None:
            task.start_date = datetime.now()
    elif category == 'delete':
        state = 'deleted'
        task.start_date = None
        task.end_date = None

    task.state = state
    
    db.session.commit()

    return redirect(url_for('index'))

