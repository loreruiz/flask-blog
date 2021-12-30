from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_blog import db, bcrypt
from flask_blog.models import Usuario, Post
from flask_blog.users.forms import RegistroForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_blog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

@users.route("/registro", methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistroForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        usuario = Usuario(usuarionombre = form.usuarionombre.data, email = form.email.data, password = hashed_pass) 
        db.session.add(usuario)
        db.session.commit()
        flash(f'{form.usuarionombre.data}, cuenta creada con éxito', 'success')
        return redirect(url_for('users.login'))
    return render_template("registro.html", title='Registro',form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.password, form.password.data):
            login_user(usuario, remember=form.recordar.data)
            return redirect(url_for('main.home'))
        else:
            flash('Tus datos no son correctos', 'danger')
    return render_template("login.html", title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.usuarionombre = form.usuarionombre.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Información de cuenta actualizada', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.usuarionombre.data = current_user.usuarionombre
        form.email.data = current_user.email
    image_file=url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Mi cuenta', image_file=image_file, form=form)

@users.route("/user/<string:usuarionombre>")
def user_posts(usuarionombre):
    page = request.args.get('page', 1, type=int)
    user = Usuario.query.filter_by(usuarionombre=usuarionombre).first_or_404()
    posts = Post.query.filter_by(autor=user).order_by(Post.fecha.desc()).paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Hemos enviado un correo con las instrucciones para actualizar tu contraseña', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)   

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = Usuario.verify_reset_token(token)
    if user is None:
        flash('El enlace no es válido o ha expirado', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Tu contraseña ha sido actualizada. Ya puedes utilizarla desde el formulario de login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Actualizar contraseña', form=form)   

