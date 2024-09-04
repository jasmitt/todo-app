from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    items = TodoItem.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['POST'])
def add():
    content = request.form.get('content')
    if content:
        new_item = TodoItem(content=content)
        db.session.add(new_item)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:item_id>')
def update(item_id):
    item = TodoItem.query.get_or_404(item_id)
    item.done = not item.done
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    item = TodoItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

