import os

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgres://maksym:TaBTYw7Ssbjns3eaYzscjDoYi0iSCM5c@dpg-cm3ldp6n7f5s73bprakg-a/backendprojectdb'
#SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ["POSTGRES_USER"]}:{os.environ["POSTGRES_PASSWORD"]}@{os.environ["POSTGRES_HOST"]}/{os.environ["POSTGRES_DB"]}'
#SQLALCHEMY_DATABASE_URI = 'postgresql://maksym:123456@localhost/backendProjDB'
SQLALCHEMY_TRACK_MODIFICATIONS = False;
API_TITLE = "BackendProject REST API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cnd.jsdelivr.net/npm/swagger-ui-dist/"
SECRET_KEY = os.environ.get('SECRET_KEY', 'a_default_secret_key')

