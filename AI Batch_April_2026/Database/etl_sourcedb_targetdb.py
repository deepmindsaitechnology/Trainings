import mysql.connector


# 🔗 DB Connection
source_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   # change if needed
    database="source_db"
)

source_cursor = source_conn.cursor()

query = "SELECT * FROM student_details"
source_cursor.execute(query)

# 📥 Fetch all data
rows = source_cursor.fetchall()

print("📋 Student Data:\n")

for row in rows:
        
    
    print(row)



# 🔗 DB Connection
target_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",   # change if needed
    database="target_db"
)

target_cursor = target_conn.cursor()


    # Step 3: Create table
target_cursor.execute("""
        CREATE TABLE IF NOT EXISTS etl_student_details (
            st_id INT,
            st_name VARCHAR(100)
        )
    """)
print ('create table successfully')

