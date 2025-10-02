from models.employee import Employee

class HRManager(Employee):
    def __init__(self, id: int, name: str, age: int, salary: float, department: str):
        super().__init__(id, name, age, salary)
        self.department = department

    def hire_employee(self, name: str, age: int, salary: float):
        """Simulate hiring a new employee (returns an Employee object, id will be set by DB)."""
        return Employee(id=None, name=name, age=age, salary=salary)

    def fire_employee(self, employee: Employee):
        """Simulate firing an employee (returns a message)."""
        return f"Employee {employee.name} (id={employee.id}) has been removed from {self.department} department."

    def __repr__(self):
        return f"HRManager(id={self.id}, name={self.name}, dept={self.department}, salary={self.salary})"
