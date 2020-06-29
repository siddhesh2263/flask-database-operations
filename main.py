from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from sqlalchemy import desc
# from models import User

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test_database.db')

db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


# **********************************************************

# Register operation

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register_user.html')

    ssn_id = int(request.form.get('ssn_id'))
    name = request.form.get('name')
    age = int(request.form.get('age'))
    date = request.form.get('date')
    address = request.form.get('address')
    state = request.form.get('state')

    new_user = User(ssn_id=ssn_id, name=name, age=age, date=date, address=address, state=state)
    db.session.add(new_user)
    db.session.commit()
    print('User added')

    return redirect(url_for('register'))

# ************************************************************

# Delete operation

@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == "GET":
        return render_template('delete_user.html')
    
    actions = request.form.getlist('action[]')
    id_matched = request.form.get('id')

    if actions[0] == "Delete" or len(id_matched) == 0:
        c_id = Temp.query.order_by(desc(Temp.date_posted)).all()
        current_id = c_id[0].store_id
        delete_user = User.query.filter_by(id=current_id).first()
    else:
        delete_user = User.query.filter_by(id=id_matched).first()

    if delete_user:
        new_id = Temp(store_id=id_matched)
        db.session.add(new_id)
        db.session.commit()
        if actions[0] == "Get ID":
            print('User found')
            return render_template('delete_user.html', id_matched=id_matched, user=delete_user)
        db.session.delete(delete_user)
        db.session.commit()
        print('User deleted')
        return redirect(url_for('delete'))
    else:
        print('User not found')
        return redirect(url_for('delete'))

# **************************************************************

# Update operation

@app.route('/update', methods=["GET", "POST"])
def update():
    if request.method == "GET":
        return render_template('update_user.html')
    
    actions = request.form.getlist('action[]')
    id_matched = request.form.get('id')

    if actions[0] == "Update" or len(id_matched) == 0:
        c_id = Temp.query.order_by(desc(Temp.date_posted)).all()
        current_id = c_id[0].store_id
        update_user = User.query.filter_by(id=current_id).first()
    else:
        update_user = User.query.filter_by(id=id_matched).first()

    if update_user:
        new_id = Temp(store_id=id_matched)
        db.session.add(new_id)
        db.session.commit()
        if actions[0] == "Get ID":
            print('User found')
            return render_template('update_user.html', id_matched=id_matched, user=update_user)

        update_user.ssn_id = int(request.form.get('ssn_id'))
        update_user.name = request.form.get('name')
        update_user.age = int(request.form.get('age'))
        update_user.date = request.form.get('date')
        update_user.address = request.form.get('address')
        update_user.state = request.form.get('state')
        db.session.commit()
        print('User updated')
        return redirect(url_for('update'))
    else:
        return redirect(url_for('update'))



# ***********************Database Operations********************************


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ssn_id = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)

class Temp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)