from main import app, db, login_manager, mail
from flask import render_template, redirect, jsonify, request, session, make_response
from model import User, Post, to_json
from flask_login import current_user, login_user, login_required, logout_user
from forms import LoginForm, RegistrationForm, VerificationForm
from sqlalchemy import func
from flask_mail import Message
from random import randint


@app.route('/index')
@app.route('/')
def index():
    return redirect('/login')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(f'/user/{current_user.id}')
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(f'/user/{user.id}')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        check = db.session.query(User).filter(User.username == form.username.data).first()
        if not check:
            user_id = db.session.query(func.max(User.id)).scalar()
            if not user_id:
                user_id = 0
            user_id += 1
            user = User(
                id=user_id,
                username=form.username.data,
                password=form.password.data,
                mail=form.mail.data
            )
            msg = Message('Код верификации на сайте to-do list', recipients=[user.mail])
            code = randint(100000, 999999)
            session['verification_code'] = str(code)
            session['new_user'] = to_json(user)
            msg.body = f'Код подтверждения: {code}'
            mail.send(msg)
            return redirect('/verification')
    return render_template('register.html', form=form)


@app.route('/verification', methods=['GET', 'POST'])
def verification():
    form = VerificationForm()
    if form.validate_on_submit():
        code = session.get('verification_code')
        if not code:
            return redirect('/register')
        if code == form.code.data:
            user = User.from_json(session.get('new_user'))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(f'/user/{user.id}')
    return render_template('verification.html', form=form)


@app.route('/user/<int:user_id>')
@login_required
def user(user_id):
    items = db.session.query(Post).filter(Post.user_id == user_id)
    return render_template('index.html', items=items)


@app.route('/load_data', methods=['GET', 'PUT'])
@login_required
def load_data():
    data = db.session.query(Post).filter(Post.user_id == current_user.id).all()
    return list(map(to_json, data))


@app.route('/add_post', methods=['PUT'])
@login_required
def add_post():
    data = request.get_json()
    post = Post()
    post_id = db.session.query(func.max(Post.id)).scalar()
    if not post_id:
        post_id = 0
    post_id += 1
    post.id = post_id
    post.content = data
    post.user_id = current_user.id
    db.session.add(post)
    db.session.commit()
    return redirect('/load_data')


@app.route('/delete_data', methods=['DELETE'])
@login_required
def delete_data():
    data = request.get_json()
    result = db.session.query(Post).filter(Post.id == data).first()
    if result:
        db.session.delete(result)
        db.session.commit()
    return make_response({}, 200)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)
