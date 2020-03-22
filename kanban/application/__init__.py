from flask import Flask, render_template, url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import sys, os



app = Flask(__name__, instance_relative_config=True)
orig_dir = os.getcwd()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(orig_dir, 'kanban.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


with app.app_context():
    from application import routes
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)