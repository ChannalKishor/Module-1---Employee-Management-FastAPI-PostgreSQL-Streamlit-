import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# from fastapi.testclient import TestClient
# from employee_management_system.backend.main import app
# import db.db_utils as db

# from fastapi.testclient import TestClient
# from employee_management_system.backend.main import app
# import employee_management_system.backend.db.db_utils as db

from fastapi.testclient import TestClient
from employee_management_system.backend.main import app
import employee_management_system.backend.db.db_utils as db


client = TestClient(app)


def setup_function():
    """Run before each test to reset DB"""
    db.create_table()
    conn = db.get_connection()
    with conn.cursor() as cur:
        cur.execute("DELETE FROM employees")
    conn.commit()
    conn.close()


def test_add_employee():
    response = client.post("/employee", json={"name": "Alice", "age": 30, "salary": 50000})
    assert response.status_code == 200
    data = response.json()
    assert data["employee"]["name"] == "Alice"
    assert data["employee"]["age"] == 30
    assert data["employee"]["salary"] == 50000


def test_get_employees():
    # Add one employee
    client.post("/employee", json={"name": "Bob", "age": 40, "salary": 60000})

    # Fetch employees
    response = client.get("/employees")
    assert response.status_code == 200
    employees = response.json()
    assert isinstance(employees, list)
    assert len(employees) == 1
    assert employees[0]["name"] == "Bob"


def test_delete_employee():
    # Add employee
    res = client.post("/employee", json={"name": "Charlie", "age": 28, "salary": 45000})
    emp_id = res.json()["employee"]["id"]

    # Delete employee
    delete_res = client.delete(f"/employee/{emp_id}")
    assert delete_res.status_code == 200
    assert "deleted successfully" in delete_res.json()["message"]

    # Confirm deletion
    employees = client.get("/employees").json()
    assert all(emp["id"] != emp_id for emp in employees)


def test_median_stats():
    # Add multiple employees
    client.post("/employee", json={"name": "David", "age": 25, "salary": 40000})
    client.post("/employee", json={"name": "Eve", "age": 35, "salary": 60000})
    client.post("/employee", json={"name": "Frank", "age": 45, "salary": 80000})

    # Median age
    age_resp = client.get("/stats/median-age")
    assert age_resp.status_code == 200
    assert age_resp.json()["median_age"] == 35

    # Median salary
    salary_resp = client.get("/stats/median-salary")
    assert salary_resp.status_code == 200
    assert salary_resp.json()["median_salary"] == 60000