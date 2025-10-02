import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5433)),
}


def get_connection():
    """Establish and return a PostgreSQL database connection."""
    return psycopg2.connect(**DB_CONFIG)


def create_table():
    """Create the employees table if it doesn't exist."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS employees (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        age INT NOT NULL CHECK (age > 0),
                        salary NUMERIC(12,2) NOT NULL CHECK (salary >= 0)
                    )
                """)
    except psycopg2.Error as e:
        print("Error creating table:", e)


def add_employee(name: str, age: int, salary: float):
    """Insert a new employee and return the employee ID."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO employees (name, age, salary) VALUES (%s, %s, %s) RETURNING id",
                    (name, age, salary),
                )
                emp_id = cursor.fetchone()[0]
                return emp_id
    except psycopg2.Error as e:
        print("Error adding employee:", e)
        return None


def get_all_employees():
    """Fetch all employees as a list of dictionaries."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT id, name, age, salary FROM employees ORDER BY id")
                return cursor.fetchall()
    except psycopg2.Error as e:
        print("Error fetching employees:", e)
        return []


def delete_employee_by_id(emp_id: int):
    """Delete an employee by ID. Returns True if deleted, False otherwise."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM employees WHERE id = %s", (emp_id,))
                return cursor.rowcount > 0
    except psycopg2.Error as e:
        print("Error deleting employee:", e)
        return False


def get_median_age():
    """Return the median age of employees using PostgreSQL percentile_cont."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY age) FROM employees"
                )
                result = cursor.fetchone()[0]
                return int(result) if result is not None else None
    except psycopg2.Error as e:
        print("Error calculating median age:", e)
        return None


def get_median_salary():
    """Return the median salary of employees using PostgreSQL percentile_cont."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY salary) FROM employees"
                )
                result = cursor.fetchone()[0]
                return float(result) if result is not None else None
    except psycopg2.Error as e:
        print("Error calculating median salary:", e)
        return None


# Example usage (for local testing)
if __name__ == "__main__":
    create_table()
    print("\n -------------------Adding employees-------------------")
    emp1 = add_employee("Alice", 30, 55000)
    emp2 = add_employee("Bob", 40, 72000)
    print(f"Inserted employees with IDs: {emp1}, {emp2}")

    print("All employees:", get_all_employees())
    print("Median age:", get_median_age())
    print("Median salary:", get_median_salary())

    print("Deleting employee with id=1:", delete_employee_by_id(1))
    print("All employees after deletion:", get_all_employees())
