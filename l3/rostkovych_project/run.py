from app import create_app
from os import environ
app = create_app(config_name='dev')
if __name__ == '__main__':
     app.run(debug=True)