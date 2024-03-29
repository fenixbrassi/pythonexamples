from flask import Blueprint, render_template,request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required , logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Bienvenido' + user.first_name , category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
    return render_template("login.html")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
    
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Ese correo ya ha sido registrado.', category='error')
            return render_template("sign_up.html")

        if len(email) < 4:
            flash('El correo electronico debe ser mayor a 3 caracteres.', category='error')
        elif password1 != password2:
            flash('Los passwords no coinciden.', category='error')
        else:
            new_user = User(email=email, first_name = first_name, password=generate_password_hash(password1) )
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado correctamente', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)