from flask import render_template, request, Blueprint
from flask_blog.models import Post
from flask_login import login_required 

main = Blueprint('main', __name__)

# definimos nuestra página de inicio
@main.route("/") # route llama a funciones, no pinta html
@main.route("/home")
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.fecha.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

# definimos página nosotros
@main.route("/nosotros")
def nosotros():
    return render_template("nosotros.html", title='Nosotros')
