from flask import Flask, render_template, request, redirect, url_for
from pymysql import connections
import os
# import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb
)
output = {}
table = 'admin', 'supervisor', 'company', 'student'

@app.route('/')
def home():
    return render_template('AdminAdministration.html')

# Admin 
@app.route('/AdminAdministration')
def AdminAdministration():
    return render_template('AdminAdministration.html')

@app.route("/AddAdmin", methods=['POST'])
def AddAdmin():
    name = request.form['name']
    email = request.form['email']
    contactNum = request.form['contactNum']
    
    insert_sql = "INSERT INTO admin VALUES (%s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (name, email, contactNum))
    db_conn.commit()
    cursor.close()

    return render_template('AdminAdministration.html')



# Supervisor 
@app.route('/SupervisorAdministration')
def SupervisorAdministration():
    return render_template('SupervisorAdministration.html')

@app.route("/AddSupervisor", methods=['POST'])
def AddSupervisor():
    staffID = request.form['staffID']
    name = request.form['name']
    email = request.form['email']
    contactNum = request.form['contactNum']
    
    insert_sql = "INSERT INTO supervisor VALUES (%s, %s, %s, %s)"
    cursor = db_conn.cursor()
    cursor.execute(insert_sql, (staffID, name, email, contactNum))
    db_conn.commit()
    cursor.close()

    return render_template('SupervisorAdministration.html')



# Company 
@app.route('/CompanyAdministration')
def CompanyAdministration():
    cursor = db_conn.cursor()
    status_approved = 'approved'
    cursor.execute('SELECT * FROM company WHERE status = %s', status_approved)
    data = cursor.fetchall()
    cursor.close()

    return render_template('CompanyAdministration.html', company = data)

@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def deleteCompany(id):
    cursor = db_conn.cursor()
    cursor.execute('DELETE FROM company WHERE companyID = %s', id)
    db_conn.commit() 
    return redirect(url_for('CompanyAdministration'))

@app.route('/CompanyRegistration')
def CompanyRegistration():
    cursor = db_conn.cursor()
    status_pending = 'pending'
    cursor.execute('SELECT * FROM company WHERE status = %s', status_pending)
    data = cursor.fetchall()
    cursor.close()

    return render_template('CompanyRegistration.html', company = data)

@app.route('/rejectCompany/<string:id>', methods = ['POST', 'GET'])
def rejectCompany(id):
    cursor = db_conn.cursor()
    status_change = 'rejected'
    cursor.execute("""
            UPDATE company
            SET status = %s
            WHERE companyID = %s
        """, (status_change, id))
    db_conn.commit() 
    return redirect(url_for('CompanyRegistration'))

@app.route('/approveCompany/<string:id>', methods = ['POST', 'GET'])
def approveCompany(id):
    cursor = db_conn.cursor()
    status_change = 'approved'
    cursor.execute("""
            UPDATE company
            SET status = %s
            WHERE companyID = %s
        """, (status_change, id))
    db_conn.commit() 
    return redirect(url_for('CompanyRegistration'))



# Student 
@app.route('/StudentRegistration')
def StudentRegistration():
    cursor = db_conn.cursor()
    status_value = 'pending'
    cursor.execute('SELECT * FROM student WHERE status = %s', status_value)
    data = cursor.fetchall()
    cursor.close()

    return render_template('StudentRegistration.html', student = data)

@app.route('/rejectStudent/<string:id>', methods = ['POST', 'GET'])
def rejectStudent(id):
    cursor = db_conn.cursor()
    status_change = 'rejected'
    cursor.execute("""
            UPDATE student
            SET status = %s
            WHERE studentID = %s
        """, (status_change, id))
    db_conn.commit() 
    return redirect(url_for('StudentRegistration'))

@app.route('/approveStudent/<string:id>', methods = ['POST', 'GET'])
def approveStudent(id):
    cursor = db_conn.cursor()
    status_change = 'approved'
    cursor.execute("""
            UPDATE student
            SET status = %s
            WHERE studentID = %s
        """, (status_change, id))
    db_conn.commit() 
    return redirect(url_for('StudentRegistration'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

