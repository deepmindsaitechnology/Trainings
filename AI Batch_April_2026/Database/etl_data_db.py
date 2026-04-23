import pandas as pd
import mysql.connector

try:
    # Step 1: Read CSV
    file_path = r"C:\\Users\\ADMIN\\Desktop\\Trainings\\AI Batch_March\\1. Python\\files\\Student.csv"

    df = pd.read_csv(file_path)   # if comma separated

    # If tab-separated:
    # df = pd.read_csv(file_path, delimiter='\t')

    print("📄 CSV Data Preview:")
    print(df.head())

    # Step 2: Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="school_db"
    )

    cursor = conn.cursor()

    # Step 3: Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ETL_student_details (
            st_id INT,
            st_name VARCHAR(100),
            Math INT,
            Science INT,
            English INT,
            Sports VARCHAR(100)
        )
    """)

    # Optional: clear old data
    cursor.execute("TRUNCATE TABLE ETL_student_details")

    # Step 4: Insert data
    insert_query = """
        INSERT INTO ETL_student_details (st_id, st_name, Math, Science, English, Sports)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    data = [tuple(row) for row in df.values]

    cursor.executemany(insert_query, data)

    conn.commit()

    print("✅ Data loaded successfully using pandas!")

except Exception as e:
    print("❌ Error:", e)

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
        print("🔒 Connection closed")