from flask import Flask, render_template,request
import pyodbc
from pyodbc import IntegrityError

#Application Name

app = Flask(__name__)

#Application Log-in routing
@app.route("/login", methods=['GET', 'POST'])
def login():	
	return render_template("login.html")

#Application Main Page Routing
@app.route("/home_page",methods =['GET','POST'])
def index():
	if request.method == 'POST':
	#User Validation and home page redirect
		if 'form3'in request.form:
			username = request.form.get('username')
			password = request.form.get('password')
			sqlcommand = """\
			DECLARE @out nvarchar(max);
			EXEC [Login_User] @UserName = ?,@PW = ?, @responseMessage = @out OUTPUT;
			SELECT @out AS the_output;
			"""
			values=(username, password)
			cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
			cursor = cnxn.cursor()
			cursor.execute(sqlcommand,values)
			rows=cursor.fetchone()
			if rows.the_output=="User successfully logged in":
				items = []
				cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
				cursor1 = cnxn.cursor()
				cursor2 = cnxn.cursor()
				cursor2.execute("select * from Users where user_emailid=?", username)
				record = cursor2.fetchone()
				cursor1.execute("SELECT * from Application")
				while 1:
					row = cursor1.fetchone()
					if row == None:
						break
					items.append(row)
					if not row:
						break
				return render_template('test.html',form=items, fname=record.User_fname, lname = record.User_lname, email = record.User_emailid, phnumber=record.User_phone_number )
			else:
				return render_template("logout.html")
		
		#Adding Application to the db		
		if 'form1'in request.form:
			username=request.form.get('username')
			app_name = request.form.get('app_name')
			app_size = request.form.get('app_size')
			price = request.form.get('price')
			app_version = request.form.get('app_version')
			category = request.form.get('category')
			developer = request.form.get('Developer')
			app_logo_link = request.form.get('app_logo_link')
			cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
			cursor1 = cnxn.cursor()
			cursor1.execute("SELECT Count(*) as count from application")
			rowcount = cursor1.fetchone()
			cnt = rowcount.count + 1
			cursor = cnxn.cursor()
			try:
				cursor.execute("insert into application values (?,?,GETDATE(),?,?,?,?,?,?)",cnt,app_name,app_size,price,app_version,category,developer,app_logo_link)
				cnxn.commit()
				cursor4 = cnxn.cursor()
				cursor4.execute("EXEC [dbo].[insert_Application_by_user] @username = ?,@appid = ?",username,cnt)
				cursor4.commit()
				items = []
				cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
				cursor1 = cnxn.cursor()
				cursor2 = cnxn.cursor()
				cursor2.execute("select * from Users where user_emailid=?", username)
				record = cursor2.fetchone()
				cursor1.execute("SELECT * from Application")
				while 1:
					row = cursor1.fetchone()
					if row == None:
						break
					items.append(row)
					if not row:
						break
				return render_template('test.html',form=items, fname=record.User_fname, lname = record.User_lname, email = record.User_emailid, phnumber=record.User_phone_number )
						
			except pyodbc.IntegrityError:
				items = []
				cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
				cursor1 = cnxn.cursor()
				cursor2 = cnxn.cursor()
				cursor2.execute("select * from Users where user_emailid=?", username)
				record = cursor2.fetchone()
				cursor1.execute("SELECT * from Application")
				while 1:
					row = cursor1.fetchone()
					if row == None:
						break
					items.append(row)
					if not row:
						break
				return render_template('test.html',form=items, fname=record.User_fname, lname = record.User_lname, email = record.User_emailid, phnumber=record.User_phone_number )
		
		#Application Deletion
		if 'delete' in request.form:
			items = []
			app_id = request.form.get('delete')
			username = str(request.form.get('username'))
			cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
			cursor1 = cnxn.cursor()
			cursor3 = cnxn.cursor()
			cursor4 = cnxn.cursor()
			cursor1.execute("delete from Application where app_Id = ?",app_id)
			cursor1.commit()	
			cursor4.execute("EXEC [dbo].[delete_Application_by_user] @username = ?,@appid = ?",username,app_id)
			cursor4.commit()
			cursor2 = cnxn.cursor()
			cursor2.execute("select * from Users where user_emailid=?", username)
			record = cursor2.fetchone()
			cursor3.execute("SELECT * from Application")
			while 1:
				row = cursor3.fetchone()
				if row == None:
					break
				items.append(row)
				if not row:
					break
			return render_template('test.html',form=items, fname=record.User_fname, lname = record.User_lname, email = record.User_emailid, phnumber=record.User_phone_number )
		
		#User Details Update
		if 'form2' in request.form:
			fname=request.form.get('fname')
			lname=request.form.get('lname')
			email=request.form.get('email')
			phone=request.form.get('phone')
			cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
			cursor1= cnxn.cursor()
			cursor1.execute("update Users set User_fname = ?, User_lname = ?, User_phone_number = ? where User_emailid = ? ", fname, lname, phone, email)
			cnxn.commit()
			cnxn.close()
			items = []
			cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
			cursor = cnxn.cursor()
			cursor1 = cnxn.cursor()
			cursor1.execute("Select * from users where user_emailid=?", email)
			record = cursor1.fetchone()
			cursor.execute("SELECT * from Application")
			while 1:
				row = cursor.fetchone()
				if row == None:
					break
				items.append(row)
				if not row:
					break
			cnxn.close()
			return render_template('test.html',form=items, fname=record.User_fname, lname = record.User_lname, email = record.User_emailid, phnumber=record.User_phone_number )
				
			
			
#User registration page routing
@app.route("/reg",methods =['GET','POST'])
def reg():
	if request.method =='POST':
		email=request.form.get('email')
		fname=request.form.get('firstname')
		lname=request.form.get('lastname')
		password=request.form.get('passwd')
		phnumber=request.form.get('phnumber')
		cnxn = pyodbc.connect(r'Driver={SQL Server};Server=LAPTOP-N49SNNN1;Database=python_project;Trusted_Connection=yes;timeout=5000')
		cursor1= cnxn.cursor()
		cursor2= cnxn.cursor()
		cursor1.execute("select Count(*) as count from Users")
		rowcount= cursor1.fetchone()
		cnt=200+(rowcount.count+1)
		cursor2.execute("insert into Users values (?,?,?,?,[dbo].[ENCRYPT](?),?)", cnt, fname, lname, email, password, phnumber)
		cnxn.commit()
		cnxn.close()
	return render_template('login.html')
	



if __name__ == "__main__":
    app.run(debug=True)