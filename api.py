from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask.ext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'b1ba3ee4b6964c'
app.config['MYSQL_DATABASE_PASSWORD'] = '91b1dd37'
app.config['MYSQL_DATABASE_DB'] = 'heroku_567546a5d8d43a6'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-03.cleardb.net'


mysql.init_app(app)

api = Api(app)

class CreateUser(Resource):
    def get(self):
        try:
            # Parse the arguments
            # parser = reqparse.RequestParser()
            # parser.add_argument('email', type=str, help='Email address to create user')
            # parser.add_argument('password', type=str, help='Password to create user')
            # args = parser.parse_args()

            _userEmail = 'test'
            _userPassword = 'testPass'

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT * from users where username='Matt Girouard'")
            data = cursor.fetchone()

            if data is None:
                return "Username wrong"
            else:
                return data['postname']

        except Exception as e:
            return {'error': str(e)}



api.add_resource(CreateUser, '/CreateUser')

if __name__ == '__main__':
    app.run(debug=True)
