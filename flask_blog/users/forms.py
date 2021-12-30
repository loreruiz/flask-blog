from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_blog.models import Usuario

class RegistroForm(FlaskForm):
    usuarionombre = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registro')

    def validate_usuarionombre(self, usuarionombre):
        usuario = Usuario.query.filter_by(usuarionombre=usuarionombre.data).first()
        if usuario:
            raise ValidationError('El nombre de usuario no esta disponible, por favor elija otro.')

    def validate_email(self, email):
        email = Usuario.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Ya existe un usuario registrado con esta cuenta de correo.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    recordar = BooleanField('Recordarme')
    submit = SubmitField('Entrar')

class UpdateAccountForm(FlaskForm):
    usuarionombre = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Cambiar imagen de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit =SubmitField('Actualizar')

    def validate_usuarionombre(self, usuarionombre):
        if usuarionombre.data != current_user.usuarionombre:
            usuario = Usuario.query.filter_by(usuarionombre=usuarionombre.data).first()
            if usuario:
                raise ValidationError('El nombre de usuario no esta disponible, por favor elija otro.')
            
    def validate_email(self, email):
        if email.data != current_user.email:
            email = Usuario.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Ya existe un usuario registrado con esta cuenta de correo.')

class RequestResetForm(FlaskForm):
    email =StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Actualizar contraseña')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario is None:
            raise ValidationError('No existe ninguna cuenta asociada a este correo')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Actualizar')

