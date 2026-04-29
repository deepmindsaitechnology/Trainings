import pandas as pd
import mysql.connector


# 📂 File paths (update if needed)
student_file =  r"C:\\Users\\ADMIN\\Desktop\\Trainings\\student_details.csv"
teacher_file = r"C:\\Users\\ADMIN\\Desktop\\Trainings\\teachers.csv"
marks_file = r"C:\\Users\\ADMIN\\Desktop\\Trainings\\student_marks.csv"

# 📘 Load CSVs
students_df = pd.read_csv(student_file)
teachers_df = pd.read_csv(teacher_file)
marks_df = pd.read_csv(marks_file)


# 🔗 DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   # change if needed
    database="source_db"
)

cursor = conn.cursor()

# -------------------------------
# 🚀 Insert Students
# -------------------------------
for _, row in students_df.iterrows():
    #print ("data row ####", tuple(row))
    cursor.execute("""
        INSERT INTO student_details
        (student_id, student_name, class, hobby, father_name, contact_number, address, bus_route)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# -------------------------------
# 👨‍🏫 Insert Teachers
# -------------------------------
for _, row in teachers_df.iterrows():
    print ("data row ####", tuple(row))
    cursor.execute("""
        INSERT INTO teachers
        (teacher_id, teacher_name, teaching_subject, experience_years, teaching_classes, contact_number, joining_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# -------------------------------
# 📝 Insert Marks
# -------------------------------
for key, row in marks_df.iterrows():
    cursor.execute("""
        INSERT INTO student_marks
        (test_id, student_id, math, science, social_science, english, computer, exam_date)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row))

# 💾 Commit changes
conn.commit()

print("✅ Data loaded successfully!")

# 🔒 Close connection
cursor.close()
conn.close()