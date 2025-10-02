class Config(object):
    USER = 'zpenr'
    PASSWORD = 'Qq12ww345'
    HOST = '127.0.0.1'
    PORT = '5532'
    DB = 'mydb'


    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = 'qewerjhgnbv3214365adgffcxcdufghv'
    SQLALCHEMY_TRACK_MODIFICATIONS = True