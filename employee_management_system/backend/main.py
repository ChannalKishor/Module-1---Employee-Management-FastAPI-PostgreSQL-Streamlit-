# # main.py

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# import db.db_utils as db

# # FastAPI app instance
# app = FastAPI(title="Employee Management System", version="1.0.0")


# # ---------- Request/Response Models ----------
# class EmployeeIn(BaseModel):
#     name: str
#     age: int
#     salary: float


# class EmployeeOut(BaseModel):
#     id: int
#     name: str
#     age: int
#     salary: float


# # ---------- Routes ----------

# @app.on_event("startup")
# def startup_event():
#     """Ensure the employees table exists when the app starts."""
#     db.create_table()


# @app.post("/employee", response_model=dict)
# def add_employee(employee: EmployeeIn):
#     emp_id = db.add_employee(employee.name, employee.age, employee.salary)
#     if not emp_id:
#         raise HTTPException(status_code=500, detail="Failed to add employee")
#     return {"message": "Employee added successfully", "employee_id": emp_id}


# @app.get("/employees", response_model=List[EmployeeOut])
# def get_all_employees():
#     employees = db.get_all_employees()
#     return employees


# @app.delete("/employee/{emp_id}", response_model=dict)
# def delete_employee(emp_id: int):
#     deleted = db.delete_employee_by_id(emp_id)
#     if not deleted:
#         raise HTTPException(status_code=404, detail="Employee not found")
#     return {"message": f"Employee with id={emp_id} deleted successfully"}


# @app.get("/stats/median-age", response_model=dict)
# def get_median_age():
#     median_age = db.get_median_age()
#     return {"median_age": median_age}


# @app.get("/stats/median-salary", response_model=dict)
# def get_median_salary():
#     median_salary = db.get_median_salary()
#     return {"median_salary": median_salary}


# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from backend.db import db_utils as db
from employee_management_system.backend.models.employee import Employee

# FastAPI app instance
app = FastAPI(title="Employee Management System", version="1.0.0")


# ---------- Request Models ----------
class EmployeeIn(BaseModel):
    name: str
    age: int
    salary: float


# ---------- Routes ----------

@app.on_event("startup")
def startup_event():
    """Ensure the employees table exists when the app starts."""
    db.create_table()


@app.post("/employee")
def add_employee(employee: EmployeeIn):
    """Add a new employee and return as Employee object."""
    emp_id = db.add_employee(employee.name, employee.age, employee.salary)
    if not emp_id:
        raise HTTPException(status_code=500, detail="Failed to add employee")

    # Wrap in Employee class before returning
    new_emp = Employee(emp_id, employee.name, employee.age, employee.salary)
    return {"message": "Employee added successfully", "employee": new_emp.__dict__}


@app.get("/employees")
def get_all_employees():
    """Fetch all employees and return as list of Employee objects."""
    employees = db.get_all_employees()
    return [Employee(emp["id"], emp["name"], emp["age"], emp["salary"]).__dict__ for emp in employees]


@app.delete("/employee/{emp_id}")
def delete_employee(emp_id: int):
    """Delete employee by ID."""
    deleted = db.delete_employee_by_id(emp_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": f"Employee with id={emp_id} deleted successfully"}


@app.get("/stats/median-age")
def get_median_age():
    """Get median age of employees."""
    median_age = db.get_median_age()
    return {"median_age": median_age}


@app.get("/stats/median-salary")
def get_median_salary():
    """Get median salary of employees."""
    median_salary = db.get_median_salary()
    return {"median_salary": median_salary}
