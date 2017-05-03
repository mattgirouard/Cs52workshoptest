from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flask.ext.mysql import MySQL
from flask.ext.cors import CORS
import json

# Setup for this REST api was adapted from:
# https://github.com/codehandbook/RESTfulApiUsingPythonFlask

mysql = MySQL()
app = Flask(__name__)
CORS(app)

app.config['MYSQL_DATABASE_USER'] = 'b1ba3ee4b6964c'
app.config['MYSQL_DATABASE_PASSWORD'] = '91b1dd37'
app.config['MYSQL_DATABASE_DB'] = 'heroku_567546a5d8d43a6'
app.config['MYSQL_DATABASE_HOST'] = 'us-cdbr-iron-east-03.cleardb.net'

mysql.init_app(app)

api = Api(app)

class PutEvent(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('user', type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('date', type=str)
            args = parser.parse_args()

            name = args['name']
            user = args['user']
            description = args['description']
            date = args['date']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("""INSERT INTO users (username, postname, postdate, detail)
            VALUES (%s, %s, %s, %s)""", (user, name, date, description))
            conn.commit()
            conn.close()

            return {'StatusCode':'200'}

        except Exception as e:
            return {'error': str(e)}


class EventsForUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('user', type=str, help='Email address to create user')
            args = parser.parse_args()
            user = args['user']

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute("""SELECT * from users where username=%s""", (user,))
            conn.commit()
            data = cursor.fetchall()
            ret_data = "["
            for row in data:
                ret_data += """{'user': '%s', 'name': '%s', 'description': '%s', 'date': '%s'}, """ % (row[0], row[1], row[2], row[3])

            ret_data = ret_data[:-2]
            ret_data += "]"

            conn.close()

            return ret_data

        except Exception as e:
            return {'error': str(e)}


class AllEvents(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            query = """SELECT * FROM users"""
            cursor.execute(query)
            data = cursor.fetchall()
            ret_data = "["
            for row in data:
                ret_data += """{'user': '%s', 'name': '%s', 'description': '%s', 'date': '%s'}, """ % (row[0], row[1], row[2], row[3])

            ret_data = ret_data[:-2]
            ret_data += "]"

            conn.close()

            return ret_data

        except Exception as e:
            return {'error': str(e)}


class DeleteEvent(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('user', type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('date', type=str)
            args = parser.parse_args()

            name = args['name']
            user = args['user']
            description = args['description']
            date = args['date']

            conn = mysql.connect()
            cursor = conn.cursor()

            query = """DELETE FROM users WHERE username="%s" and postname="%s" and postdate="%s" and detail="%s" """ % (user, name, description, date)
            cursor.execute(query)
            conn.commit()

            conn.close()

            return {'StatusCode':'200','Message': 'Delete success'}

        except Exception as e:
            return {'error': str(e)}


api.add_resource(PutEvent, '/PutEvent')
api.add_resource(EventsForUser, '/EventsForUser')
api.add_resource(AllEvents, '/AllEvents')
api.add_resource(DeleteEvent, '/DeleteEvent')

if __name__ == '__main__':
    app.run(debug=True)
