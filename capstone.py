import mysql.connector
import streamlit as st
import pandas as pd
import re 

st.markdown(
    """
    <style>
    /* Apply green background color */
    body {
        background-color: #27ae60; /* Change this to your desired green color */
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# Establish a connection to MySQL Server
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="chiragpranav",
    database="dbms"
)
mycursor = mydb.cursor()
print("Connection Established")



def display_faculty_without_teams_and_panels():
    # SQL query to select faculty members without teams and panels
    query = """
    SELECT F.*
    FROM Faculty AS F
    WHERE EXISTS (
        -- Check if the faculty is mentoring a team
        SELECT 1
        FROM Team AS T
        WHERE T.F_SRN = F.F_SRN
    )
    AND NOT EXISTS (
        -- Ensure the faculty is not on a panel
        SELECT 1
        FROM Panel AS P
        WHERE P.Panel_ID = F.Panel_ID
    ); 
    """
    
    mycursor.execute(query)
    result = mycursor.fetchall()

    if result:
        col_headers = [i[0] for i in mycursor.description]  # Get column headers from cursor description
        st.table([col_headers] + result)  # Prepend column headers to the result
    else:
        st.warning("No faculty members found without teams and panels.")



def common_domain_interest_study_table():
    # SQL query to retrieve the common domains of interest and study
    query = """
    SELECT 
      t.TeamID,
      f.F_SRN,
      f.Department,
      GROUP_CONCAT(DISTINCT dos.Domain) AS Team_Domains,
      GROUP_CONCAT(DISTINCT dk.Domain_of_interest) AS Faculty_Domains
    FROM 
      Faculty f
    JOIN 
      Team t ON f.F_SRN = t.F_SRN
    JOIN 
      DomainOfStudy dos ON t.TeamID = dos.TeamID
    JOIN 
      DomainKnowledge dk ON f.F_SRN = dk.F_SRN
    WHERE dos.Domain IN (SELECT Domain_of_interest FROM DomainKnowledge WHERE F_SRN = f.F_SRN)
    GROUP BY 
      t.TeamID,
      f.F_SRN,
      f.Department;
    """

    # Execute the SQL query
    mycursor.execute(query)
    result = mycursor.fetchall()

    # Display the results in Streamlit
    if result:
        col_headers = [i[0] for i in mycursor.description]  # Get column headers from cursor description
        st.table([col_headers] + result)  # Prepend column headers to the result
    else:
        st.warning("No common domains found.")


    # Connect to the database
def assign_student_to_team():
    # User input fields in Streamlit
    student_srn = st.text_input("Enter Student SRN:")
    team_id = st.text_input("Enter Team ID:")
    project_id = st.text_input("Enter Project ID:")

    # Button to assign the student when clicked
    if st.button("Assign Student"):
        # Connect to the database
       
                try:
                    # Call the stored procedure
                    mycursor.callproc('AssignStudentToTeam', [student_srn, team_id, project_id])
                    
                    # Commit the changes
                    mydb.commit()
                    st.success(f"Student {student_srn} has been successfully assigned to Team {team_id} and Project {project_id}.")

                except mysql.connector.Error as e:
                    st.error(f" COMBINATION OF TEAM AND PROJECT ID DOES NOT EXIST")

def get_faculty_data_with_condition():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="chiragpranav",
        database="dbms"
    )
    mycursor = mydb.cursor()
    
    
    query = "SELECT f.F_SRN,f.First_Name,f.Last_Name,f.Department FROM Faculty f WHERE EXISTS (SELECT 1 FROM Team t INNER JOIN Student s ON t.TeamID = s.TeamID AND t.ProjectID = s.ProjectID WHERE t.F_SRN = f.F_SRN AND s.CGPA > (SELECT AVG(s2.CGPA) FROM Student s2 WHERE s2.Department = f.Department ));`"
    mycursor.execute(query)
    faculty_data = mycursor.fetchall()
    if faculty_data:
            # Display the results in the frontend
            for faculty in faculty_data:
                st.write(f"Faculty SRN: {faculty[0]}, Name: {faculty[1]} {faculty[2]}, Department: {faculty[3]}")
    else:
            # Inform the user that no data was found
            st.warning("No faculty data found that matches the criteria.")
    
    

def create_review_record():
    st.subheader("Create_Review")
    #review_id = st.text_input("Review ID", key="new_review_id")
    
    isa_1 = st.number_input("ISA 1", key="new_isa_1",step=1)
    isa_2 = st.text_input("ISA 2", key="new_isa_2")
    esa_1 = st.text_input("ESA 1", key="new_esa_1")
    isa_3 = st.text_input("ISA 3", key="new_isa_3")
    isa_4 = st.text_input("ISA 4", key="new_isa_4")
    esa_2 = st.text_input("ESA 2", key="new_esa_2")
    esa_3 = st.text_input("ESA 3", key="new_esa_3")
   
    faculty_srn = st.text_input("Faculty SRN", key="new_f_srn")
    student_srn = st.text_input("Student SRN", key="new_srn")

    if st.button("Create Review for student"):
      insert_sql = "INSERT INTO Review(ISA_1,ISA_2,ESA_1,ISA_3,ISA_4,ESA_2,ESA_3,Faculty_ID,SRN) VALUES ( %s,%s, %s, %s, %s,%s,%s,%s,%s)"
      review_data = (isa_1, isa_2, esa_1, isa_3, isa_4, esa_2, esa_3, faculty_srn, student_srn)
      mycursor.execute(insert_sql, review_data)
      mydb.commit()
      st.success("Review record created successfully!")

def update_review_marks():
    st.subheader("Update Review Marks")
    faculty_srn = st.text_input("Faculty SRN", key="update_f_srn")
    student_srn = st.text_input("Student SRN", key="update_s_srn")
    isa_1 = st.text_input("New ISA 1 Marks", key="update_isa_1")
    isa_2 = st.text_input("New ISA 2 Marks", key="update_isa_2")
    esa_1 = st.text_input("New ESA 1 Marks", key="update_esa_1")
    isa_3 = st.text_input("New ISA 3 Marks", key="update_isa_3")
    isa_4 = st.text_input("New ISA 4 Marks", key="update_isa_4")
    esa_2 = st.text_input("New ESA 2 Marks", key="update_esa_2")
    esa_3 = st.text_input("New ESA 3 Marks", key="update_esa_3")

    if st.button("Update Review Marks"):
        update_sql = "UPDATE Review SET ISA_1=%s, ISA_2=%s, ESA_1=%s, ISA_3=%s, ISA_4=%s, ESA_2=%s, ESA_3=%s WHERE Faculty_ID=%s AND SRN=%s"
        update_data = (isa_1, isa_2, esa_1, isa_3, isa_4, esa_2, esa_3, faculty_srn, student_srn)
        mycursor.execute(update_sql, update_data)
        mydb.commit()
        if mycursor.rowcount > 0:
            st.success("Review marks updated successfully!")
        else:
            st.warning("Faculty and Student SRN combination not found. No records updated.")


def delete_review_record():
    st.subheader("Delete Review")
    review_id = st.text_input("Review ID to delete", key="delete_review_id")

    if st.button("Delete Review"):
        # Check if the review_id is provided
        if not review_id:
            st.error("Please enter a Review ID to delete.")
            return

        # Attempt to delete the record with the provided Review ID
        delete_sql = "DELETE FROM Review WHERE Review_ID = %s"
        mycursor.execute(delete_sql, (review_id,))

        if mycursor.rowcount > 0:
            mydb.commit()
            st.success(f"Review record with Review ID {review_id} deleted successfully.")
        else:
            st.error(f"No review record found with Review ID {review_id}.")




def insert_domain_of_study(domain, project_id, team_id):
    # SQL statement to insert values into the DomainOfStudy table
    insert_sql = "INSERT INTO DomainOfStudy (domain, ProjectID, TeamID) VALUES (%s, %s, %s)"
    values = (domain, project_id, team_id)

    try:
        mycursor.execute(insert_sql, values)
        mydb.commit()
        st.success("Values inserted into the DomainOfStudy table.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

def insert_domain_knowledge(F_SRN, domain_of_interest):
# Check if the faculty member with the provided F_SRN exists
        check_faculty_sql = "SELECT * FROM Faculty WHERE F_SRN = %s"
        mycursor.execute(check_faculty_sql, (F_SRN,))
        existing_faculty = mycursor.fetchone()

        if existing_faculty:
            # Insert the new domain knowledge data into the DomainKnowledge table
            insert_domain_sql = "INSERT INTO DomainKnowledge (F_SRN, domain_of_interest) VALUES (%s, %s)"
            insert_domain_values = (F_SRN, domain_of_interest)
            mycursor.execute(insert_domain_sql, insert_domain_values)
            mydb.commit()
            print("Domain Knowledge record created successfully!")
        else:
            print("Faculty member with the provided F_SRN does not exist.")
        
        mycursor.close()
        mydb.close()

    
def read_domain_of_study_table():
     mycursor.execute("SELECT * FROM DOMAINofStudy")
     result = mycursor.fetchall()
     for row in result:
        st.write(row)
    # # SQL query to select all records from the DomainOfStudy table
    #  select_query = "SELECT * FROM DomainOfStudy"

    #  mycursor.execute(select_query)
    #  result = mycursor.fetchall()

    # # Display the results in Streamlit
    #  if result:
    #     col_headers = [i[0] for i in mycursor.description]  # Get column headers from cursor description
    #     st.table([col_headers] + result)  # Prepend column headers to the result
    #  else:
    #     st.warning("No data found in the DomainOfStudy table.")

def delete_domain_attribute(team_id, project_id, attribute_name):
    update_query = "DELETE FROM DomainOfStudy WHERE TeamID = %s AND ProjectID = %s AND Domain = %s"
    update_values = (team_id, project_id, attribute_name)

    if team_id and project_id and attribute_name:
        mycursor.execute(update_query, update_values)

        # Fetch the result (you can use fetchone, fetchall, or fetchmany as needed)
        result = mycursor.fetchall()

        # If you don't need the result, you can close the cursor to release unread results
        # mycursor.close()

        mydb.commit()
        st.success("DELETED")
   
def fetch_faculty_panel_data():
    # Execute the SQL query
    query = '''
    SELECT
        S.SRN AS Student_SRN,
        T.TeamID,
        F.F_SRN AS Faculty_SRN,
        F.Department AS Faculty_Department,
        P.Panel_ID AS Faculty_Panel
    FROM
        Student S
    JOIN
        Team T ON S.TeamID = T.TeamID AND S.ProjectID = T.ProjectID
    JOIN
        Faculty F ON T.F_SRN = F.F_SRN
    JOIN
        Panel P ON F.PANEL_ID = P.PANEL_ID;
    '''
    mycursor.execute(query)
    result = mycursor.fetchall()
    # Define the column labels for the DataFrame
    column_labels = ['Student SRN', 'Team ID', 'Faculty SRN', 'Faculty Department', 'Faculty Panel']

        # Create a DataFrame with the fetched results
    df = pd.DataFrame(result, columns=column_labels)

        # Display the results as a table in Streamlit
    if not df.empty:
            st.table(df)
    else:
            st.warning("No data found.")
    # Display the results in Streamlit
    

def create_faculty_data():
    st.subheader("Create Faculty")
    phone_number = st.text_input("Phone Number", key="new_faculty_phone")
    first_name = st.text_input("First Name", key="new_faculty_first_name")
    last_name = st.text_input("Last Name", key="new_faculty_last_name")
    position = st.text_input("Position", key="new_faculty_position")
    department = st.text_input("Department", key="new_faculty_department")
    f_srn = st.text_input("Faculty SRN", key="new_faculty_srn")
    panel_id = st.text_input("Panel ID", key="new_panel_id")
    if not panel_id:
        panel_id = None

    if st.button("Create Faculty"):
        insert_sql = "INSERT INTO Faculty(Phone_Number,First_Name,Last_Name,Position,Department,F_SRN,Panel_ID) VALUES (%s, %s,%s, %s, %s, %s,%s)"
        insert_val = (phone_number,first_name,last_name,position,department,f_srn,panel_id)
        
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        st.success("Faculty record created successfully!")
    
def update_faculty_position_department(f_srn: str, position: str, department: str, panel_id: int):
    try:
        # Check if the faculty member exists.
        check_sql = "SELECT F_SRN FROM Faculty WHERE F_SRN = %s"
        check_val = (f_srn,)
        mycursor.execute(check_sql, check_val)
        existing_faculty = mycursor.fetchone()

        if existing_faculty:
            # Update the faculty member's record.
            update_sql = "UPDATE Faculty SET Position = %s, Department = %s, Panel_ID = %s WHERE F_SRN = %s"

            update_val = (position, department, panel_id, f_srn)
            mycursor.execute(update_sql, update_val)
            mydb.commit()
            return "Faculty record updated successfully!"
        else:
            raise Exception("Faculty member does not exist.")
    except Exception as e:
        return str(e)


def delete_faculty(f_srn: int):
  """Deletes a faculty member from the Faculty table.

  Args:
    f_srn: The faculty SRN.
  """

  # Check if the faculty member exists.
  check_sql = "SELECT F_SRN FROM Faculty WHERE F_SRN = %s"
  check_val = (f_srn,)
  mycursor.execute(check_sql, check_val)
  existing_faculty = mycursor.fetchone()

  if existing_faculty:
    # Delete the faculty member record.
    delete_sql = "DELETE FROM Faculty WHERE F_SRN = %s"
    delete_val = (f_srn,)
    mycursor.execute(delete_sql, delete_val)
    mydb.commit()
    st.success("Faculty record deleted successfully!")
  else:
    st.error("Faculty member does not exist.")


### PANEL

def create_panel_data():
  st.subheader("Create Panel")
  panel_id = st.text_input("Panel_ID")
  panel_name = st.text_input("Panel_Name")
  #panel_team = st.text_input("Panel_Team")
  no_of_members = st.number_input("No_Of_Members", min_value=2, max_value=4)
  if not panel_id:
    panel_id = None

  if st.button("Create Panel"):
    # Check if the panel already exists.
    check_sql = "SELECT Panel_ID FROM Panel WHERE Panel_ID = %s AND Panel_Name = %s"
    check_val = (panel_id, panel_name)
    mycursor.execute(check_sql, check_val)
    existing_panel = mycursor.fetchone()

    if existing_panel:
      # Update the number of members in the existing panel record.
      update_sql = "UPDATE Panel SET No_Of_Members = %s WHERE Panel_ID = %s AND Panel_Name = %s"
      update_val = (no_of_members, panel_id, panel_name)
      mycursor.execute(update_sql, update_val)
      mydb.commit()
      st.success("Panel record updated successfully!")
    else:
      # Insert a new panel record into the Panel table.
      insert_sql = "INSERT INTO Panel (Panel_ID, Panel_Name, No_Of_Members) VALUES (%s, %s, %s)"
      insert_val = (panel_id, panel_name, no_of_members)
      mycursor.execute(insert_sql, insert_val)
      mydb.commit()
      st.success("Panel record created successfully!")


def delete_panel_data(Panel_ID):
  check_sql = "SELECT Panel_ID FROM Panel WHERE Panel_ID = %s"
  check_val = (Panel_ID,)
  mycursor.execute(check_sql, check_val)
  existing_panel = mycursor.fetchone()

  if existing_panel:
    # Delete the panel record.
    delete_sql = "DELETE FROM Panel WHERE Panel_ID = %s"
    delete_val = (Panel_ID,)
    mycursor.execute(delete_sql, delete_val)
    mydb.commit()
    st.success("Panel record deleted successfully!")
  else:
    st.error("Panel does not exist.")


#### STUDENT


def create_student_data():
    st.subheader("Create Student Record")
    srn = st.text_input("SRN")
    cgpa = st.number_input("CGPA", min_value=0, step=1,max_value=10)
    department = st.text_input("Department")
    section = st.text_input("Section")

    phone_number = st.text_input("Phone Number")
    Email = st.text_input("Email")
    semester = st.number_input("Semester", min_value=6,max_value=8)
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    team_id = st.text_input("TeamID")
    project_id = st.text_input("ProjectID")
    if not team_id:
        team_id = None

    if not project_id:
        project_id = None

    
    

    if st.button("Create student"):
        # Insert the new Student record into the Student table
        insert_sql = "INSERT INTO Student (SRN, CGPA, Department, Section, Phone_number,Email, Semester, First_name, Last_name, TeamID, ProjectID) VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert_val = (srn, cgpa, department, section, phone_number,Email, semester, first_name, last_name, team_id, project_id)
        
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        st.success("Student record created successfully!")

#for individual students:
def read_student_data(username):
    st.header(f"Welcome, {username}")
    student_sql = """
    SELECT SRN, CGPA, Department, Section, Phone_Number, Email, Semester, First_Name, Last_Name
    FROM Student
    WHERE SRN = %s
    """
    review_sql = """
    SELECT ISA_1, ISA_2, ESA_1, ISA_3, ISA_4, ESA_2, ESA_3
    FROM Review
    WHERE SRN = %s
    """
    
    # Fetch student personal details
    mycursor.execute(student_sql, (username,))
    student_result = mycursor.fetchone()
    
    # Fetch review results
    mycursor.execute(review_sql, (username,))
    review_result = mycursor.fetchall()
    
    # Define labels for personal details
    personal_labels = [
        "SRN:",
        "CGPA:",
        "Department:",
        "Section:",
        "Phone Number:",
        "Email:",
        "Semester:",
        "First Name:",
        "Last Name:"
    ]

    # Define labels for review details
    review_labels = [
        "ISA 1:",
        "ISA 2:",
        "ESA 1:",
        "ISA 3:",
        "ISA 4:",
        "ESA 2:",
        "ESA 3:"
    ]

    # Display personal details
    if student_result:
        for label, item in zip(personal_labels, student_result):
            st.text(f"{label} {item}")
    else:
        st.error("No personal records found.")

    # Add some space before the next section
    st.text("\n")

    # Display review details
    if review_result:
        st.write("Review Scores:")
        for review in review_result:
            for label, item in zip(review_labels, review):
                st.text(f"{label} {item}")
            st.text("")  # Add space after each review entry
    else:
        st.error("No review records found.")

#def create_teacher_data():

# Create a function to read data from the Student table for admin:
def read_all_students_data():
    st.subheader("All Students Records")
    student_sql = "SELECT * FROM Student"
    mycursor.execute(student_sql)
    students_result = mycursor.fetchall()
    if students_result:
        # Convert the list of tuples to a dataframe and display it as a table
        df_students = pd.DataFrame(students_result, columns=[x[0] for x in mycursor.description])
        st.dataframe(df_students)
    else:
        st.error("No student records found.")

def update_student_data():
    st.subheader("Update Student Data")
    
    srn = st.text_input("Student SRN", key="update_srn")
    cgpa = st.number_input("New CGPA", min_value=0, step=1, max_value=10, key="update_cgpa")
    email= st.text_input("New EMAIL", key="update_email")
    semester = st.text_input("SEMESTER", key="update_semester")
    phone_number = st.text_input("PHONE NUMBER",key = "update_phone_number")

    if st.button("Update Student Data"):
        update_sql = "UPDATE Student SET CGPA = %s, email = %s, Semester = %s,Phone_Number =%s WHERE SRN = %s"
        update_data = (cgpa,email,semester,phone_number, srn)
        mycursor.execute(update_sql, update_data)
        mydb.commit()

        if mycursor.rowcount > 0:
            st.success("Student data updated successfully!")
        else:
            st.warning("No student found with the provided SRN. No records updated.")

def delete_student_data():
    st.subheader("Delete Student")
    student_srn = st.text_input("Student SRN to delete", key="delete_student_srn")

    if st.button("Delete Student"):
        # Check if the student_srn is provided
        if not student_srn:
            st.error("Please enter a Student SRN to delete.")
            return

        # Attempt to delete the record with the provided Student SRN
        delete_sql = "DELETE FROM Student WHERE SRN = %s"
        mycursor.execute(delete_sql, (student_srn,))

        if mycursor.rowcount > 0:
            mydb.commit()
            st.success(f"Student with SRN {student_srn} deleted successfully.")
        else:
            st.error(f"No student found with SRN {student_srn}.")
# Create a function to read data from the Team table
def read_team_data():
    st.subheader("Read Team Records")
    mycursor.execute("SELECT * FROM Team")
    team_result = mycursor.fetchall()
    if team_result:
        df_team = pd.DataFrame(team_result, columns=[x[0] for x in mycursor.description])
        st.dataframe(df_team)
    else:
        st.error("No team records found.")

def read_review_data():
    st.subheader("Read Review Records")
    
    # Execute a SELECT query to fetch all records from the Review table
    select_sql = "SELECT * FROM Review"
    mycursor.execute(select_sql)
    
    # Fetch all the records
    review_records = mycursor.fetchall()
    
    # Display the records
    if review_records:
        for row in review_records:
            st.write(row)
    else:
        st.warning("No records found in the Review table.")


### TEAM   

def create_team_data():
    st.subheader("Create Team Records")
    phase = st.text_input("Phase", key="new_phase")
    projectname = st.text_input("ProjectName", key="new_project_name")
    projectid = st.text_input("ProjectID", key="new_project_id")
    teamid = st.text_input("TeamID", key="new_team_id")
    f_srn = st.text_input("F_SRN", key="new_F_SRN")
    if not f_srn:
        f_srn = None

    if st.button("Create Team"):
        insert_sql = "INSERT INTO team(Phase,ProjectName,ProjectID,TeamID,F_SRN) VALUES (%s,%s,%s,%s,%s)"
        insert_val = (phase,projectname,projectid,teamid,f_srn)
        
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        st.success("Team record created successfully!")



def update_team_data(team_id: int, f_srn: str, project_name: str):
  """Updates the F_SRN and ProjectName of a team record in the Team table.

  Args:
    team_id: The team ID.
    f_srn: The new F_SRN.
    project_name: The new project name.
  """

  # Check if the team record exists.
  check_sql = "SELECT TeamID FROM Team WHERE TeamID = %s"
  check_val = (team_id,)
  mycursor.execute(check_sql, check_val)
  existing_team = mycursor.fetchone()

  if existing_team:
    # Update the team record.
    update_sql = "UPDATE Team SET F_SRN = %s, ProjectName = %sWHERE TeamID = %s "
    update_val = (f_srn, project_name, team_id)
    mycursor.execute(update_sql, update_val)
    mydb.commit()
    st.success("Team record updated successfully!")
  else:
    st.error("Team record does not exist.")




def delete_team(team_id: int):
  """Deletes a team record from the Team table.

  Args:
    team_id: The team ID.
  """

  # Check if the team record exists.
  check_sql = "SELECT TeamID FROM Team WHERE TeamID = %s"
  check_val = (team_id,)
  mycursor.execute(check_sql, check_val)
  existing_team = mycursor.fetchone()

  if existing_team:
    # Delete the team record.
    delete_sql = "DELETE FROM Team WHERE TeamID = %s"
    delete_val = (team_id,)
    mycursor.execute(delete_sql, delete_val)
    mydb.commit()
    st.success("Team record deleted successfully!")
  else:
    st.error("Team record does not exist.")


# Create a function to read data from the Faculty table
def read_faculty_data():
    st.subheader("Read Faculty Records")
    mycursor.execute("SELECT * FROM Faculty")
    faculty_result = mycursor.fetchall()
    if faculty_result:
        df_faculty = pd.DataFrame(faculty_result, columns=[x[0] for x in mycursor.description])
        st.dataframe(df_faculty)
    else:
        st.error("No faculty records found.")

def read_faculty_details_personal(username):
    st.header(f"Welcome, {username}")
    # SQL Query to select the faculty details by username (or SRN)
    faculty_sql = "SELECT * FROM Faculty WHERE F_SRN = %s"
    
    # Execute the SQL query
    mycursor.execute(faculty_sql, (username,))
    
    # Fetch the faculty details
    faculty_details = mycursor.fetchone()
    
    # Check if faculty details were found
    if faculty_details:
        # Define labels for faculty details
        faculty_labels = [
            "Phone_Number:",
            "First Name:",
            "Last Name:",
            "Position:",
            "Department:",
            "F_SRN:",
            "Panel_ID:"
        ]
        
        for label, item in zip(faculty_labels, faculty_details):
            st.text(f"{label} {item}")
    else:
        st.error("No faculty records found for the provided SRN.")

# Create a function to read data from the Panel table
# 
def read_panel_data():
    st.subheader("Read Panel Records")
    mycursor.execute("SELECT * FROM Panel")
    panel_result = mycursor.fetchall()
    if panel_result:
        df_panel = pd.DataFrame(panel_result, columns=[x[0] for x in mycursor.description])
        st.dataframe(df_panel)
    else:
        st.error("No panel records found.")

def authenticate_user(username, password):
    sql = "SELECT UserType FROM LoginCredentials WHERE Username = %s AND Password = %s"
    mycursor.execute(sql, (username, password))
    return mycursor.fetchone()

# User Authentication and Session Management
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    sql = "SELECT UserType FROM LoginCredentials WHERE Username = %s AND Password = %s"
    val = (username, password)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()
    if result:
        user_role = result[0]
        st.session_state.user_role = user_role
        st.session_state.username = username
    else:
        st.error("Invalid credentials. Please log in with a valid username and password.")

# Toggle button to show/hide the registration form
show_registration_form = st.checkbox("Register")
if show_registration_form:
    with st.form("Registration Form"):
        st.subheader("Registration")
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        new_usertype = st.selectbox("User Type", ["user", "admin", "teacher"])
        submitted = st.form_submit_button("Create Account")
        if submitted:
            student_pattern = "PES[0-9]{2}[0-9]{3}"
            teacher_pattern = "PES[0-9]{5}"
            is_student = new_usertype == "user" and re.fullmatch(student_pattern, new_username)
            is_teacher = new_usertype == "teacher" and re.fullmatch(teacher_pattern, new_username)
            if is_student or is_teacher or new_usertype == "admin":
                check_sql = "SELECT Username FROM LoginCredentials WHERE Username = %s"
                check_val = (new_username,)
                mycursor.execute(check_sql, check_val)
                existing_user = mycursor.fetchone()
                if existing_user:
                    st.error("Username already exists. Please choose a different username.")
                else:
                    insert_sql = "INSERT INTO LoginCredentials (Username, Password, UserType) VALUES (%s, %s, %s)"
                    insert_val = (new_username, new_password, new_usertype)
                    mycursor.execute(insert_sql, insert_val)
                    mydb.commit()
                    st.success("Account created successfully!")
            else:
                if new_usertype == "user":
                    st.error("Invalid format for student username. Format should be PES<year><SRN>.")
                elif new_usertype == "teacher":
                    st.error("Invalid format for teacher username. Format should be PES<5 digits>.")


if "user_role" in st.session_state:
    if st.button("Logout"):
        st.session_state.pop("user_role")
        st.session_state.pop("username", None)
        # Clear the username and password fields
        #st.session_state.username = ""
        #st.session_state.password = ""

        username = ""
        password = ""

# Create Streamlit App
def main():
    st.title("Capstone Management")
   
    #st.title("Faculty Data with Condition")
    #st.subheader("Click the button to retrieve faculty data based on the condition")
    
   
    # Get the current user role
   

# Hide the login page if the user is logged in
    
    # Role-Based Access Control
    if "user_role" in st.session_state:
        if st.session_state.user_role == "admin":
            st.subheader("Admin Panel")
            # Display options for CRUD operations on all tables
            if st.checkbox("Read Student Data"):
                    read_all_students_data()
            if st.checkbox("Create Student Data"):
                create_student_data()
            if st.checkbox("update Student Data"):
                update_student_data()

            if st.checkbox("Read Team Data"):
                read_team_data()
            if st.checkbox("Create Team "):
                create_team_data()
            if st.checkbox("Update Team Data"):
                team_id = st.text_input("Enter Team ID to Update")
                f_srn = st.text_input("Enter New F_SRN")
                project_name = st.text_input("Enter New Project Name")
                update_team_data(team_id, f_srn, project_name)
            if st.checkbox("Read Faculty Data"):
                read_faculty_data()
            if st.checkbox("Create Faculty"):
                create_faculty_data()
            if st.checkbox("Update Faculty"):
                faculty_srn = st.text_input("Enter Faculty SRN to Update")
                faculty_position = st.text_input("Enter New Position")
                faculty_department = st.text_input("Enter New Department")
                panel_id = st.text_input("ENTER PANEL_ID")

            if st.button("Update Faculty Record"):
                result = update_faculty_position_department(faculty_srn, faculty_position, faculty_department, panel_id)
                if "successfully" in result:
                    st.success(result)
                else:
                    st.error(result)
            
            if st.checkbox("Read Panel Data"):

                

                read_panel_data()
            if st.checkbox("Create Panel"):
                create_panel_data()
            
            if st.checkbox("Fetch Faculty Panel Data(FUNCTION)"):
                    fetch_faculty_panel_data()
            if st.checkbox("PROCEDURE"):
                assign_student_to_team()

            if st.checkbox("Insert Values into domain of interest"):
                st.write("Insert values into the DomainOfStudy table:")
                domain = st.text_input("Domain")
                project_id = st.text_input("Project ID")
                team_id = st.text_input("Team ID")

                if domain and project_id and team_id:
                    insert_domain_of_study(domain, project_id, team_id)
                else:
                    st.error("Please fill in all the fields.")

            if st.checkbox("Read DomainOfStudy Table"):
                read_domain_of_study_table()
                #read_panel_data()
            if st.checkbox("DELETE DOMAIN"):
                    team_id = st.text_input("Enter Team_ID")
                    project_id = st.text_input("Enter Project_ID")
                    attribute_name = st.text_input("Enter the Attribute Name to Delete")
                    delete_domain_attribute(team_id, project_id, attribute_name)
            
            if st.checkbox("PROFESSOR DOMAIN"):
                domain = st.text_input("Enter Domain")
                f_srn = st.text_input("Enter F_SRN")
                insert_domain_knowledge(f_srn,domain)
            # if st.checkbox("Correlation"):
                
            #     faculty_data = get_faculty_data_with_condition()
            #     if faculty_data:
            #         st.success(faculty_data)
            #     else:
            #         st.warning("No data found that matches the condition.")
           
            if st.button("Show Common Domains of Interest and Study"):
                common_domain_interest_study_table()
            if st.checkbox("delete student"):
                delete_student_data()
            if st.checkbox("Delete Faculty Member"):
                    faculty_srn = st.text_input("Enter Faculty SRN to Delete")
                    delete_faculty(faculty_srn)

            if st.checkbox("Delete Panel"):
                panel_id = st.text_input("Enter Panel ID to Delete")
                delete_panel_data(panel_id)
            if st.checkbox("DISPLAYING TEACHERS NOT PART OF any PANEL but are mentoring a team(NESTED QUERY)"):
                    display_faculty_without_teams_and_panels()
            
            
            if st.checkbox("DELETE TEAM"):
               team_id = st.text_input("Enter Team ID to Delete")
               delete_team(team_id)
            if st.checkbox("read review"):
                read_review_data()
            
            if st.checkbox("Create Review for student"):
               create_review_record()
            
            if st.checkbox("Update Review"):
               update_review_marks()
          
            

        elif st.session_state.user_role == "user":
            
            st.subheader("Student Panel")
            # Display options for read-only access to the Student table
            if st.checkbox("Read Student Data"):
                read_student_data(username)
            if st.button("Show Common Domains of Interest and Study"):
                common_domain_interest_study_table()
        elif st.session_state.user_role == "teacher":
            st.subheader("Teacher Panel")
            if st.checkbox("Read Faculty Data"):
                read_faculty_details_personal(username)
            if st.checkbox("UPDATE reivew"):
                update_review_marks()
            
            

            # Implement access control for teachers (e.g., read their team's data)
            # Create a function to fetch and display teacher-specific data
            # For example, read_teacher_data(username) for the teacher's username
        else:
            st.error("Invalid credentials. Please log in.")
    else:
        st.warning("Please log in.")

if __name__ == "__main__":
    main()
