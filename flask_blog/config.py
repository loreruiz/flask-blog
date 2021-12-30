import os

class Config:
    # SECRET_KEY = os.environ.get('SECRET_KEY')   # crear variable de entorno con SECRET_KEY
    SECRET_KEY = 'hk5b4!cb6+*9kwc3&ml%j1g(0xlq9zla4b2-%y6vqj=$7_&#&)'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') # crear variable de entorno con URI
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'lorenaruizballester@gmail.com'
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = 'cqrfzbyrsivfhyhd'
    # 'MAIL_PASSWORD = os.environ.get('EMAIL_PASS')