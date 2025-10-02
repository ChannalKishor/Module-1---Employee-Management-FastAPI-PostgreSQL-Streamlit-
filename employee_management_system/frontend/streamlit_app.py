# # streamlit_app.py

# import streamlit as st
# import requests

# API_URL = "http://127.0.0.1:8000"  # FastAPI backend

# st.set_page_config(page_title="Employee Management System", page_icon="👩‍💼", layout="centered")

# st.title("👩‍💼 Employee Management System 👨‍💼")
# st.markdown("---")


# # ---------------- ADD EMPLOYEE FORM ----------------
# st.header("➕ Add New Employee")

# with st.form("add_employee_form"):
#     name = st.text_input("Name")
#     age = st.number_input("Age", min_value=18, max_value=100, step=1)
#     salary = st.number_input("Salary", min_value=0.0, step=1000.0)
#     submitted = st.form_submit_button("Add Employee")

#     if submitted:
#         response = requests.post(f"{API_URL}/employee", json={"name": name, "age": age, "salary": salary})
#         if response.status_code == 200:
#             st.success(f"✅ Employee '{name}' added successfully!")
#         else:
#             st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")


# st.markdown("---")


# # ---------------- VIEW EMPLOYEES ----------------
# st.header("📋 Employee List")

# try:
#     employees = requests.get(f"{API_URL}/employees").json()
#     if employees:
#         st.table(employees)
#     else:
#         st.info("No employees found. Add some above!")
# except Exception as e:
#     st.error("Could not fetch employees. Is the API running?")


# st.markdown("---")


# # ---------------- DELETE EMPLOYEE ----------------
# st.header("❌ Delete Employee")

# try:
#     employees = requests.get(f"{API_URL}/employees").json()
#     employee_ids = [emp["id"] for emp in employees]

#     if employee_ids:
#         emp_to_delete = st.selectbox("Select Employee ID to Delete", employee_ids)

#         if st.button("Delete Employee"):
#             response = requests.delete(f"{API_URL}/employee/{emp_to_delete}")
#             if response.status_code == 200:
#                 st.success(response.json()["message"])
#             else:
#                 st.error(response.json().get("detail", "Error deleting employee"))
#     else:
#         st.info("No employees available for deletion.")

# except Exception:
#     st.error("Error fetching employee list for deletion.")


# st.markdown("---")


# # ---------------- STATS ----------------
# st.header("📊 Employee Statistics")

# col1, col2 = st.columns(2)

# with col1:
#     try:
#         response = requests.get(f"{API_URL}/stats/median-age").json()
#         st.metric("Median Age", response.get("median_age", "N/A"))
#     except:
#         st.error("Failed to fetch median age")

# with col2:
#     try:
#         response = requests.get(f"{API_URL}/stats/median-salary").json()
#         st.metric("Median Salary", response.get("median_salary", "N/A"))
#     except:
#         st.error("Failed to fetch median salary")



# streamlit_app.py

import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # FastAPI backend

st.set_page_config(page_title="Employee Management System", page_icon="👩‍💼", layout="centered")

st.title("👩‍💼 Employee Management System 👨‍💼")
st.markdown("---")


# ---------------- ADD EMPLOYEE FORM ----------------
st.header("➕ Add New Employee")

with st.form("add_employee_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    salary = st.number_input("Salary", min_value=0.0, step=1000.0)
    submitted = st.form_submit_button("Add Employee")

    if submitted:
        response = requests.post(f"{API_URL}/employee", json={"name": name, "age": age, "salary": salary})
        if response.status_code == 200:
            st.success(f"✅ Employee '{name}' added successfully!")
        else:
            st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")


st.markdown("---")


# ---------------- VIEW EMPLOYEES ----------------
st.header("📋 Employee List")

if st.button("🔄 Fetch Employee List"):
    try:
        employees = requests.get(f"{API_URL}/employees").json()
        if employees:
            st.table(employees)
        else:
            st.info("No employees found. Add some above!")
    except Exception as e:
        st.error("Could not fetch employees. Is the API running?")


st.markdown("---")


# ---------------- DELETE EMPLOYEE ----------------
st.header("❌ Delete Employee")

try:
    employees = requests.get(f"{API_URL}/employees").json()
    employee_ids = [emp["id"] for emp in employees]

    if employee_ids:
        emp_to_delete = st.selectbox("Select Employee ID to Delete", employee_ids)

        if st.button("Delete Employee"):
            response = requests.delete(f"{API_URL}/employee/{emp_to_delete}")
            if response.status_code == 200:
                st.success(response.json()["message"])
            else:
                st.error(response.json().get("detail", "Error deleting employee"))
    else:
        st.info("No employees available for deletion.")

except Exception:
    st.error("Error fetching employee list for deletion.")


st.markdown("---")


# ---------------- STATS ----------------
st.header("📊 Employee Statistics")

if st.button("📊 Fetch Statistics"):
    col1, col2 = st.columns(2)

    with col1:
        try:
            response = requests.get(f"{API_URL}/stats/median-age").json()
            st.metric("Median Age", response.get("median_age", "N/A"))
        except:
            st.error("Failed to fetch median age")

    with col2:
        try:
            response = requests.get(f"{API_URL}/stats/median-salary").json()
            st.metric("Median Salary", response.get("median_salary", "N/A"))
        except:
            st.error("Failed to fetch median salary")
