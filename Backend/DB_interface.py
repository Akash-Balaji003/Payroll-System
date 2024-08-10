from datetime import date
import json
from fastapi.responses import JSONResponse
import mysql.connector
from Utilities.Response_manager import Att_decoder
from decimal import Decimal


def Get_data():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()
            read_query = "SELECT emp_id, emp_name, DA_Percentage, No_Leave_Bonus, Shift_Type, Basic_Per_Day, Basic_Per_Month, BATA, NLB_Threshold FROM employee;"
            cursor.execute(read_query)
            rows = cursor.fetchall()
            json_data = []

            # Iterate through rows and create JSON objects
            for row in rows:
                emp_id, emp_name, DA_Percentage, No_Leave_Bonus, Shift_Type, Basic_Per_Day, Basic_Per_Month, BATAs, NLB_Threshold = row
                data = {
                    'emp_id': emp_id,
                    'emp_name': emp_name,
                    'DA_Percentage': DA_Percentage,
                    'No_Leave_Bonus': No_Leave_Bonus,
                    'Shift_Type': Shift_Type,
                    'Basic_Per_Day': Basic_Per_Day,
                    'Basic_Per_Month': Basic_Per_Month,
                    'BATA': BATAs,
                    'NLB_Threshold': NLB_Threshold
                }
                json_data.append(data)

            # Convert Python list to JSON string
            json_string = json.dumps(json_data, indent=2)
            print(json_string)

    except mysql.connector.Error as error:
        print(f"Error updating record: {error}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            # Make sure to fetch all remaining results before closing cursor
            cursor.fetchall()
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")
    return(json_string)

def insert_data(data: dict):
    insert_cmd = "INSERT INTO Attendance (Emp_id, Emp_name, Attendance_date, Submitted_date, Attendance, Company_id, Basic_Per_Day, Basic_Per_Month, BATA, DA_Percentage, OT, No_Leave_Bonus, NLB_Threshold, Daily_Wage)"
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()

            # SQL query to update a record
            for record in data:
                insert_query = f"{insert_cmd} VALUES ({record['Emp_id']}, '{record['Emp_name']}', '{record['attendance_date']}', '{record['submitted_date']}',{record['attendance_code']}, {record['Company_id']}, {record['Basic_Per_Day']}, {record['Basic_Per_Month']}, {record['BATA']}, {record['DA_Percentage']}, {record['OT']}, {record['No_Leave_Bonus']}, {record['NLB_Threshold']}, {record['Daily_Wage']} );"
                print(insert_query)
                cursor.execute(insert_query)
            connection.commit()

    except mysql.connector.Error as error:
        print(f"Error updating record: {error}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            # Make sure to fetch all remaining results before closing cursor
            cursor.fetchall()
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def get_att_data(selected_date: str):
    json_data = []
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            cursor = connection.cursor()
            read_query = f"SELECT emp_id, emp_name, attendance, OT FROM Attendance where attendance_date = '{selected_date}'"
            cursor.execute(read_query)
            rows = cursor.fetchall()

            # Iterate through rows and create JSON objects
            for row in rows:
                emp_id, emp_name, attendance, OTt = row
                data = {
                    'emp_id': emp_id,
                    'emp_name': emp_name,
                    'attendance_code': attendance,
                    'OT':OTt
                }
                json_data.append(data)

            # Close cursor
            cursor.close()

            # Apply Att_decoder function to modify json_data
            Att_decoder(json_data)

            # Convert Python list to JSON string
            json_string = json.dumps(json_data, indent=2)
            print(json_string)

    except mysql.connector.Error as error:
        print(f"Error retrieving data: {error}")

    finally:
        # Close connection
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

    return json_data

def update_data(data: dict):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()

            # SQL query to update a record
            for record in data:
                update_query = f"UPDATE Attendance SET Submitted_date = '{record['submitted_date']}', Attendance = {record['attendance_code']} WHERE Emp_id = {record['Emp_id']} AND Attendance_date = '{record['attendance_date']}' "
                print(update_query)
                cursor.execute(update_query)
            connection.commit()

    except mysql.connector.Error as error:
        print(f"Error updating record: {error}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            # Make sure to fetch all remaining results before closing cursor
            cursor.fetchall()
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def insert_data_Txn(data: dict):
    insert_cmd = "INSERT INTO Emp_Transaction (Emp_id, Company_id, Txn_date, Submitted_date, Description, Debit, Credit, MOP, Ref_No_Cheque_No, Emp_Dues)"
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()

            # SQL query to update a record
            insert_query = f"{insert_cmd} VALUES ({data['Emp_id']}, {data['Company_id']}, '{data['Txn_date']}', '{data['submitted_date']}', '{data['Description']}', {data['Debit']}, {data['Credit']}, '{data['MOP']}', '{data['ref']}', {data['actual_due']} );"
            print(insert_query)
            cursor.execute(insert_query)
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Error updating record: {error}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            # Make sure to fetch all remaining results before closing cursor
            cursor.fetchall()
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def get_due(id: int):
    
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()
            read_query = f"SELECT Emp_dues FROM Emp_Transaction WHERE Emp_id = {id} ORDER BY updated_at DESC LIMIT 1;"
            cursor.execute(read_query)
            row = cursor.fetchone()  # Fetch only one row

            # Ensure that the response is a single dictionary with the 'dues' key
            if row:
                emp_dues = row[0]
                return JSONResponse(content={"dues": emp_dues})
            else:
                return JSONResponse(content={"dues": 0.0})

    except mysql.connector.Error as error:
        print(f"Error updating record: {error}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            # Make sure to fetch all remaining results before closing cursor
            cursor.fetchall()
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def get_att_sal(emp_id, month_year):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )
        cursor = conn.cursor()

        query = f"""
        SELECT 
            emp_id, 
            DA_Percentage, 
            No_Leave_Bonus, 
            BATA, 
            Basic_Per_Month,
            NLB_Threshold,
            SUM(Basic_Per_Day * CASE 
            WHEN attendance IN (2, 3) THEN 0.5 
            ELSE attendance 
            END) AS Total_Daily_Wage,
            SUM(
                CASE 
                    WHEN attendance IN (2, 3) THEN 0.5 
                    ELSE attendance 
                END
            ) AS Total_Attendance
        FROM 
            attendance
        WHERE 
            emp_id = {emp_id}
            AND DATE_FORMAT(Attendance_date, '{month_year}')
        GROUP BY 
            emp_id, 
            DA_Percentage, 
            No_Leave_Bonus, 
            BATA,
            Basic_Per_Month,
            NLB_Threshold;
        """

        

        cursor.execute(query)
        print(f"Executing query: {query}")

        result = cursor.fetchone()

        result_dict = {
            'emp_id': result[0],
            'Total_Daily_Wage': float(result[6]) if result[6] is not None else 0,
            'Total_Attendance': float(result[7]) if result[7] is not None else 0,
            'DA_Percentage': float(result[1]) if result[1] is not None else 0,
            'No_Leave_Bonus': result[2],
            'BATA': result[3],
            'Basic_Per_Month': float(result[4]) if result[4] is not None else 0,
            'NLB_Threshold': float(result[5]) if result[5] is not None else 0
        }

        cursor.close()
        conn.close()

        json_string = json.dumps(result_dict, indent=2)
        print(json_string)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return {"data": result_dict}

def  insert_data_payroll(data: dict):
    insert_cmd = "INSERT INTO Payroll (Emp_id, Company_id, Days_worked, Salary_date, Description, Wage, DA_Amount, MOP, Due, BATA, No_Leave_Bonus, Recovery, Salary, OtherBonus)"
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()

            # SQL query to update a record
            insert_query = f"{insert_cmd} VALUES ({data['Emp_id']}, {data['Company_id']}, {data['Days_worked']}, '{data['Salary_date']}', '{data['Description']}', {data['Wage']}, {data['DA_Amount']}, '{data['MOP']}', {data['Due']}, {data['BATA']}, {data['No_Leave_Bonus']}, {data['Recovery']}, {data['Salary']}, {data['OtherBonus']} );"
            print(insert_query)
            cursor.execute(insert_query)
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Error updating record: {error}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            # Make sure to fetch all remaining results before closing cursor
            cursor.fetchall()
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection closed")

def get_data_Txn(id: int):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )

        if connection.is_connected():
            print('Connected to MySQL database')

            # Create a cursor object using cursor() method
            cursor = connection.cursor()
            read_query = f"SELECT Txn_date, Credit, Debit, Emp_dues, Description, Ref_No_Cheque_No, MOP FROM Emp_Transaction WHERE Emp_id = {id} ORDER BY updated_at DESC LIMIT 10;"
            cursor.execute(read_query)
            print(f"Executing query: {read_query}")

        results = cursor.fetchall()

            # Check if results are not empty
        if results:
            result_dict = []
            for row in results:
                result_dict.append({
                    'Txn_date': row[0].isoformat() if isinstance(row[0], date) else row[0],
                    'Credit': float(row[1]) if row[1] is not None else 0,
                    'Debit': float(row[2]) if row[2] is not None else 0,
                    'Emp_dues': float(row[3]) if row[3] is not None else 0,
                    'Description': row[4],
                    'Ref_No_Cheque_No': row[5],
                    'MOP': row[6]
                })

            json_string = json.dumps(result_dict, indent=2)
            print(json_string)
        else:
            print("No results found")
            result_dict = []

        cursor.close()
        connection.close()


    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return {"data": result_dict}

def get_payroll(emp_id, month_year):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='RO',
            user='root',
            password='Akash003!'
        )
        cursor = conn.cursor()

        query = f"""
        SELECT 
            Wage, 
            DA_Amount, 
            No_Leave_Bonus, 
            BATA, 
            OtherBonus,
            Recovery,
            Days_worked,
            Salary,
            Description,
            MOP,
            Due
        FROM 
            payroll
        WHERE 
            emp_id = {emp_id}
            AND DATE_FORMAT(Salary_date, '{month_year}');
        """

        

        cursor.execute(query)
        print(f"Executing query: {query}")

        result = cursor.fetchone()

        result_dict = {
            'Wage': result[0],
            'DA_Amount': result[1],
            'No_Leave_Bonus': result[2],
            'BATA': result[3],
            'OtherBonus': result[4],
            'Recovery': result[5],
            'Days_worked': float(result[6]) if result[6] is not None else 0,
            'Salary': result[7],
            'Description': result[8],
            'MOP': result[9],
            'Due': result[10]
        }

        cursor.close()
        conn.close()

        json_string = json.dumps(result_dict, indent=2)
        print(json_string)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return {"data": result_dict}
