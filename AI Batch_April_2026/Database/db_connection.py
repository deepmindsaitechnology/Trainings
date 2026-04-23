import mysql.connector

try:
    # Establish connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="school_db"
    )

    if conn.is_connected():
        print("✅ Connected to MySQL database successfully!")

        cursor = conn.cursor()
        print ("Cursor #### : ", cursor)

        # Example query
        cursor.execute("SELECT * FROM student_details")



        print("\n📋 Student Details:")
        for row in cursor.fetchall():
            print ("details are here")
            print(row) 

except mysql.connector.Error as e:
    print("❌ Error while connecting to MySQL:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("\n🔒 MySQL connection closed.")