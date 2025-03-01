from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import Integer, String

class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
#db = SQLAlchemy(app)

#run in terminal these commands
#from app import app, db
#with app.app_context()
#   db.create_all()

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default =0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    

@app.route('/', methods=['POST','GET'])
def index():
    
    if request.method == 'POST':
        
        task_content = request.form['content']
        new_task =Todo(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        
        except:
            return 'There is an issue submitting your request'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('/index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'
    
    return 'Data deleted'

@app.route('/baseTemplate')
def baseTemplate():
    return render_template('base.html')

if __name__ == "__main__":
    app.run(debug=True)