import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="Student Progress Tracker",
    layout="wide"
)


# -----------------------------
# STORE STUDENT DATA
# -----------------------------

if "students" not in st.session_state:
    st.session_state.students = []


# -----------------------------
# FUNCTION TO ADD STUDENT
# -----------------------------

def add_student():

    student_name = st.session_state.student_name
    student_id = st.session_state.student_id

    python_marks = st.session_state.python_marks
    statistics_marks = st.session_state.statistics_marks
    ai_marks = st.session_state.ai_marks
    ml_marks = st.session_state.ml_marks

    # Check name and ID

    if student_name == "" or student_id == "":
        st.session_state.message = "Please enter Student Name and Student ID."
        return

    # Calculate total

    total = (
        python_marks
        + statistics_marks
        + ai_marks
        + ml_marks
    )

    # Calculate percentage

    percentage = total / 4

    # Calculate status

    if percentage >= 80:
        status = "Excellent"

    elif percentage >= 50:
        status = "Good"

    else:
        status = "Needs Improvement"

    # Create student record

    student = {
        "Student ID": student_id,
        "Student Name": student_name,
        "Python": python_marks,
        "Statistics": statistics_marks,
        "AI": ai_marks,
        "Machine Learning": ml_marks,
        "Total": total,
        "Percentage": percentage,
        "Status": status
    }

    # Add student

    st.session_state.students.append(student)

    # Message

    st.session_state.message = "Student added successfully!"

    # Clear input fields

    st.session_state.student_name = ""
    st.session_state.student_id = ""

    st.session_state.python_marks = 0
    st.session_state.statistics_marks = 0
    st.session_state.ai_marks = 0
    st.session_state.ml_marks = 0


# -----------------------------
# TITLE
# -----------------------------

st.title(" Student Progress Tracker")

st.write(
    "Add students, enter their marks and check their academic performance."
)


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header(" Student Details")


student_name = st.sidebar.text_input(
    "Student Name",
    key="student_name"
)


student_id = st.sidebar.text_input(
    "Student ID",
    key="student_id"
)


# -----------------------------
# MARKS
# -----------------------------

st.sidebar.subheader(" Enter Marks")


python_marks = st.sidebar.number_input(
    "Python",
    min_value=0,
    max_value=100,
    value=0,
    key="python_marks"
)


statistics_marks = st.sidebar.number_input(
    "Statistics",
    min_value=0,
    max_value=100,
    value=0,
    key="statistics_marks"
)


ai_marks = st.sidebar.number_input(
    "Artificial Intelligence",
    min_value=0,
    max_value=100,
    value=0,
    key="ai_marks"
)


ml_marks = st.sidebar.number_input(
    "Machine Learning",
    min_value=0,
    max_value=100,
    value=0,
    key="ml_marks"
)


# -----------------------------
# ADD STUDENT BUTTON
# -----------------------------

st.sidebar.button(
    "+ Add Student",
    on_click=add_student
)


# -----------------------------
# SHOW MESSAGE
# -----------------------------

if "message" in st.session_state:

    if st.session_state.message == "Student added successfully!":

        st.sidebar.success(
            st.session_state.message
        )

    else:

        st.sidebar.error(
            st.session_state.message
        )

    # Remove message after displaying

    del st.session_state.message


# ============================================================
# DISPLAY STUDENTS
# ============================================================

if len(st.session_state.students) == 0:

    st.info(
        " Add a student using the form on the left."
    )


else:

    # -----------------------------
    # CREATE DATAFRAME
    # -----------------------------

    students_df = pd.DataFrame(
        st.session_state.students
    )


    # -----------------------------
    # OVERVIEW
    # -----------------------------

    st.subheader(" Student Overview")

    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Total Students",
        len(students_df)
    )


    col2.metric(
        "Average Percentage",
        f"{students_df['Percentage'].mean():.1f}%"
    )


    col3.metric(
        "Highest Percentage",
        f"{students_df['Percentage'].max():.1f}%"
    )


    col4.metric(
        "Lowest Percentage",
        f"{students_df['Percentage'].min():.1f}%"
    )


    # -----------------------------
    # ALL STUDENTS
    # -----------------------------

    st.subheader(" All Students")

    st.dataframe(
        students_df,
        use_container_width=True
    )


    # -----------------------------
    # CHECK STUDENT
    # -----------------------------

    st.subheader(" Check Student Performance")


    # Create student selection

    student_options = (
        students_df["Student ID"]
        + " - "
        + students_df["Student Name"]
    )


    selected_student = st.selectbox(
        "Select Student",
        student_options
    )


    # Get selected ID

    selected_id = selected_student.split(" - ")[0]


    # Find selected student

    student = students_df[
        students_df["Student ID"] == selected_id
    ].iloc[0]


    # -----------------------------
    # STUDENT DETAILS
    # -----------------------------

    st.write("###  Student Details")


    col1, col2 = st.columns(2)


    col1.write(
        f"**Student Name:** {student['Student Name']}"
    )


    col2.write(
        f"**Student ID:** {student['Student ID']}"
    )


    # -----------------------------
    # PERFORMANCE
    # -----------------------------

    st.subheader(" Performance")


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Total Marks",
        student["Total"]
    )


    col2.metric(
        "Percentage",
        f"{student['Percentage']:.1f}%"
    )


    col3.metric(
        "Performance",
        student["Status"]
    )


    # -----------------------------
    # PROGRESS BAR
    # -----------------------------

    st.write("###  Overall Performance")


    st.progress(
        int(student["Percentage"])
    )


    # -----------------------------
    # SUBJECT MARKS
    # -----------------------------

    st.subheader(" Subject-wise Marks")


    subjects = [
        "Python",
        "Statistics",
        "AI",
        "Machine Learning"
    ]


    marks = [
        student["Python"],
        student["Statistics"],
        student["AI"],
        student["Machine Learning"]
    ]


    # -----------------------------
    # BAR CHART
    # -----------------------------

    fig, ax = plt.subplots()


    ax.bar(
        subjects,
        marks
    )


    ax.set_xlabel("Subjects")
    ax.set_ylabel("Marks")
    ax.set_ylim(0, 100)


    plt.xticks(
        rotation=30
    )


    plt.tight_layout()


    st.pyplot(fig)


    # -----------------------------
    # PERFORMANCE ANALYSIS
    # -----------------------------

    st.subheader(" Performance Analysis")


    if student["Percentage"] >= 80:

        st.success(
            "Excellent performance! Keep up the good work."
        )

    elif student["Percentage"] >= 50:

        st.warning(
            "Good performance. There is still room for improvement."
        )

    else:

        st.error(
            "Performance needs improvement. Focus more on the subjects."
        )


    # -----------------------------
    # PROGRESS STATUS
    # -----------------------------

    st.subheader(" Progress Status")


    if student["Percentage"] >= 70:

        st.success(
            "Status: On Track"
        )

    elif student["Percentage"] >= 50:

        st.warning(
            "Status: Needs Improvement"
        )

    else:

        st.error(
            "Status: At Risk"
        )


    # -----------------------------
    # DOWNLOAD CSV
    # -----------------------------

    st.subheader("⬇ Download Student Data")


    csv_data = students_df.to_csv(
        index=False
    )


    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="student_progress.csv",
        mime="text/csv"
    )


# -----------------------------
# FOOTER
# -----------------------------

st.markdown("---")

