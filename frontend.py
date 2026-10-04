import streamlit as st
import requests

API_BASE_URL = st.secrets.get("BACKEND_URL", "https://erp-attendance-system.onrender.com")

st.set_page_config(page_title="ERP Attendance System", page_icon="📊", layout="wide")

# 1. Custom CSS Styling (Styles your real metrics and buttons)
st.markdown(
    """
    <style>
    /* Metric Card Styling */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600;
        font-size: 0.9rem;
    }
    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
        font-size: 1.8rem;
        font-weight: 700;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 2. Main Title
st.title("📊 ERP Student Attendance System")
st.markdown("---")

# 3. Sidebar: Register Student
with st.sidebar:
    st.header("➕ Register Student")
    with st.form("register_form", clear_on_submit=True):
        new_usn = st.text_input("USN", placeholder="e.g. 1RL24CY013").strip().upper()
        new_name = st.text_input("Full Name", placeholder="e.g. Raju Kumar").strip()
        submit_btn = st.form_submit_button("Register Student")

        if submit_btn:
            if not new_usn or not new_name:
                st.warning("Please provide both USN and Name.")
            else:
                try:
                    res = requests.post(
                        f"{API_BASE_URL}/student",
                        json={"USN": new_usn, "Name": new_name}
                    )
                    if res.status_code == 201:
                        st.success(f"Student {new_name} added successfully!")
                        st.rerun()
                    else:
                        st.error(res.json().get("detail", "Failed to add student."))
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to FastAPI backend. Is it running?")

# 4. Student Roster & Live Real Metrics
st.subheader("📋 Student Attendance Roster")

try:
    response = requests.get(f"{API_BASE_URL}/students")

    if response.status_code == 200:
        students = response.json()

        if not students:
            st.info("No students registered yet. Add students from the sidebar.")
        else:
            students = sorted(students, key=lambda x: str(x["USN"]))
            # REAL Live Metrics from your database
            total_students = len(students)
            total_present = sum(1 for s in students if s.get("status") == "Present")
            total_absent = total_students - total_present

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Students", total_students)
            col2.metric("Present Today", total_present)
            col3.metric("Absent Today", total_absent)

            st.write("")

            # Header row
            head_col1, head_col2, head_col3, head_col4, head_col5 = st.columns([2, 3, 2, 2, 1])
            head_col1.markdown("**USN**")
            head_col2.markdown("**Student Name**")
            head_col3.markdown("**Current Status**")
            head_col4.markdown("**Action**")
            head_col5.markdown("**Delete**")
            st.divider()

            # Render rows directly from DB
            for student in students:
                usn = student["USN"]
                name = student["Name"]
                current_status = student.get("status", "Absent")

                c1, c2, c3, c4, c5 = st.columns([2, 3, 2, 2, 1])
                c1.write(f"`{usn}`")
                c2.write(name)

                # Status indicator
                if current_status == "Present":
                    c3.success("Present")
                else:
                    c3.error("Absent")

                # Action toggle
                target_status = "Absent" if current_status == "Present" else "Present"
                btn_label = f"Mark {target_status}"
                if c4.button(btn_label, key=f"toggle_{usn}"):
                    update_res = requests.put(
                        f"{API_BASE_URL}/attendance/{usn}",
                        json={"status": target_status}
                    )
                    if update_res.status_code == 200:
                        st.rerun()
                    else:
                        st.error("Failed to update status.")

                # Delete action
                if c5.button("🗑️", key=f"del_{usn}"):
                    del_res = requests.delete(f"{API_BASE_URL}/student/{usn}")
                    if del_res.status_code == 200:
                        st.rerun()
                    else:
                        st.error("Failed to delete record.")
    else:
        st.error(f"Error fetching data: {response.text}")

except requests.exceptions.ConnectionError:
    st.error("⚠️ Backend server is offline. Make sure Uvicorn is running.")