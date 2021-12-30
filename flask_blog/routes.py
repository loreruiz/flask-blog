import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login.utils import logout_user
from flask_wtf import form
from flask_blog import app, db, bcrypt, mail
from flask_blog.models import Usuario, Post
from flask_blog.forms import RegistroForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, current_user, logout_user, login_required   
from flask_mail import Message

# definimos nuestra página de inicio
@app.route("/") # route llama a funciones, no pinta html
@app.route("/home")
@login_required
def home():
    page = request.args.get('pagina', 1, type=int)
    posts = Post.query.order_by(Post.fecha.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

# definimos página nosotros
@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html", title='Nosotros')
