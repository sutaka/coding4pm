from flask import Flask, render_template, redirect, request, session, flash
import setup
from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

def create_app(test_config=None):
    app = setup.init(test_config)
    @app.get('/')
    def home():
        user_id = session.get('user_id')
        if user_id is None:
            return redirect('/login')
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()
        return render_template('home.html', name=user['username'])

    @app.get('/logout')
    def logout():
        session.clear()
        return redirect('/')

    @app.get('/login')
    def login_get():
        if session.get('user_id') is not None:
            return redirect("/")

        return render_template('login.html')

    @app.post('/login')
    def login_post():
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            return render_template('login.html', message = 'ユーザー名が違います')
        elif not check_password_hash(user['password_hash'], password):
            return render_template('login.html', message = 'パスワードが違います')

        session.clear()
        session['user_id'] = user['id']
        return redirect('/')


    @app.get('/register')
    def register_get():
        if session.get('user_id') is not None:
            return redirect("/")

        return render_template('register.html')

    @app.post('/register')
    def register_post():
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        try:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            return render_template('register.html', message="ユーザー名がすでに使われています")
        else:
            return redirect('/login')
    
    return app