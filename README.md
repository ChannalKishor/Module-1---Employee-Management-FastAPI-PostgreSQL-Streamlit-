# Employee Management System

A **full-stack CRUD application** built with **FastAPI** for the backend and designed to manage employee records efficiently. It provides RESTful APIs for adding, retrieving, updating, and deleting employee data.

---

## 🚀 Features

- ➕ **Add employees** with details like name, age, and salary  
- 📋 **View all employees** in the database  
- ✏️ **Update employee information**  
- ❌ **Delete employees** by ID  
- 🧪 **Comprehensive test suite** using `pytest` and `TestClient`  

---

## 🛠️ Tech Stack

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/)  
- **Database:** PostgreSQL / SQLite (depending on config)  
- **Testing:** `pytest` with `fastapi.testclient`  
- **Package Management:** `pip`  

---

| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| POST   | `/employee`      | Add a new employee         |
| GET    | `/employees`     | Fetch all employees        |
| DELETE | `/employee/{id}` | Remove an employee         |

🌟 Future Improvements

- Add authentication & authorization
- Implement a React/Next.js frontend
- Add Docker support for easy deployment
- Support advanced queries (filtering, pagination)

