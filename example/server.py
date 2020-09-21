from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify

# Connecting to the DB
db_connect = create_engine('sqlite:///sample.db')

# Creating the application
app = Flask(__name__)
api = Api(app)

# API to get the list of all the empoyees
class Employee(Resource):
    def get(self):
        conn = db_connect.connect() # connect to database
        query = conn.execute("select * from employees") # This line performs query and returns json result
        return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is employee ID

# API to get info about an empoyee
class Employee_info(Resource):
    def get(self):
        conn = db_connect.connect()
        emp = request.args.get('employee_id')
        query = conn.execute("select * from employees where EmployeeId =%d "  %int(emp))
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        return jsonify(result)

# Publishing APIs
api.add_resource(Employee, '/employees') # Route 1
api.add_resource(Employee_info, '/employee') # Route 2

if __name__ == '__main__':
    app.run(port=5002)