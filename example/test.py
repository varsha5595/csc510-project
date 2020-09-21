from flask import Flask, request
import requests

# To check list of employees
def test_get_employees_check_status_code_equals_200():
     response = requests.get("http://127.0.0.1:5002/employees")
     assert response.status_code == 200

# Test to check get employee info
def test_get_employee_info_check_status_code_equals_200():
     response = requests.get("http://127.0.0.1:5002/employee?employee_id=1")
     assert response.status_code == 200

# Test to check get employee info
def test_get_employee_info():
     response = requests.get("http://127.0.0.1:5002/employee?employee_id=1")
     response_body = response.json()
     assert response_body["data"][0]["Email"] == "andrew@chinookcorp.com"
