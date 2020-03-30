from models.employee import Employee
from models.base import Base
from flask import Flask, request, jsonify
from flask_api import status
from sqlalchemy import create_engine, MetaData, func
from sqlalchemy.orm import sessionmaker
import os

DB_HOST = 'db'
DB_USER = os.getenv('MYSQL_USER')
DB_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD')
DB_NAME = os.getenv('MYSQL_DATABASE')
DB_PORT = os.getenv('MYSQL_PORT', 3306)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4' \
                                        .format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME))

engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}?charset=utf8mb4' \
                       .format(DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME), echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

@app.route('/api/employees/add', methods=['POST'])
def add_employee():
    try:
        response = {}
        try:
            body = request.data
            print(str(body), flush=True )
        except Exception as e:
            pass
        name = request.args.get('name')
        benefit_cost = request.args.get('benefit_cost')
        if name is None or benefit_cost is None:
            response['status'] = 'Invalid parameters. Employee was not added.'
            response = jsonify(response)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response, status.HTTP_400_BAD_REQUEST
        e = Employee(name=name, benefit_cost=benefit_cost)
        session.add(e)
        session.commit()

        response['status'] = 'Employee succesfully added.' 
        response = jsonify(response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, status.HTTP_200_OK
    except Exception as e:
        response['status'] = 'Error occurred while adding Employee: %s' % str(e)
        response = jsonify(response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response, status.HTTP_500_INTERNAL_SERVER_ERROR

@app.route('/api/employee/benefits', methods=['GET'])
def get_benefits():
    response = {}
    name = request.args.get('name')
    queryset = session.query(Employee).filter(func.lower(Employee.name) == name.lower()).all()
    for employee in queryset:
        response['name'] = employee.benefit_cost
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)