from employee_management_system.backend.models.person import Person


class Employee(Person):
    def __init__(self, id: int, name: str, age: int, salary: float):
        super().__init__(name, age)
        self.id = id          
        self.salary = salary

    def __repr__(self):
        return f"Employee(id={self.id}, name={self.name}, age={self.age}, salary={self.salary})"
