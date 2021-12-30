from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog import db
from flask_blog.models import Post
from flask_blog.posts.forms import PostForm

posts = Blueprint('posts',__name__)

@posts.route("/post/new", methods=['GET', 'POST'])    # nueva publicación
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, contenido=form.contenido.data, autor=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Publicación creada', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='Nueva publicación', form=form, legend='Nueva publicación')

@posts.route("/post<int:post_id>")    # mostrar las publicaciones
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', titulo=post.titulo, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])   # actualizar publicación
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.titulo = form.titulo.data
        post.contenido = form.contenido.data
        db.session.commit()
        flash('Publicación actualizada', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.titulo.data = post.titulo
        form.contenido.data = post.contenido
    return render_template('create_post.html', title='Actualizar publicación', form=form, legend='Actualizar publicación')

@posts.route("/post/int<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.autor != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Publicación eliminada', 'success')
    return redirect(url_for('main.home'))
