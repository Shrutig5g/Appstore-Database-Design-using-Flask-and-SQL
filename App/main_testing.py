from flask import Flask, render_template,request,abort,flash

import urllib.request, json,pyodbc
from pyodbc import IntegrityError
from  werkzeug.debug import get_current_traceback

app = Flask(__name__)

@app.route("/",methods=['GET', 'POST'])
def index():
	items = []
	cnxn = pyodbc.connect(r'Driver={SQL Server};Server=DEVILSDEN;Database=trigger_demo;Trusted_Connection=yes;timeout=5000')
	cursor = cnxn.cursor()
	cursor.execute("SELECT * from employee")
	while 1:
		row = cursor.fetchone()
		if row == None:
			break
		items.append(row)
		if not row:
			break
	return render_template("index.html",form=items)
	
@app.route('/form')
def show_form():
	items = []
	cnxn = pyodbc.connect(r'Driver={SQL Server};Server=DEVILSDEN;Database=trigger_demo;Trusted_Connection=yes;timeout=5000')
	cursor = cnxn.cursor()
	cursor.execute("SELECT * from employee")
	while 1:
		row = cursor.fetchone()
		if row == None:
			break
		items.append(row)
		if not row:
			break
	return render_template('form.html',form=items)
	

@app.route('/<app_id>/<app_version>', methods=['GET','POST'])
def delete_application(app_id,app_version):
	items = []
	appid = app_id
	appversion = app_version
	print(appid,appversion)
	cnxn = pyodbc.connect(r'Driver={SQL Server};Server=DEVILSDEN;Database=Python_project;Trusted_Connection=yes;timeout=5000')
	cursor = cnxn.cursor()
	cursor.execute("SELECT * from Application where app_id = ? AND app_version = ?",(appid,appversion))
	while 1:
		row = cursor.fetchone()
		if row == None:
			break
		items.append(row)
		if not row:
			break
	return render_template('test.html',form=items)
	
	
@app.route("/test", methods =['GET','POST'])
def form_request():
	if request.method == 'POST':  #this block is only entered when the form is submitted
		app_id = request.form.get('app_id')
		app_name = request.form.get('app_name')
		app_size = request.form.get('app_size')
		price = request.form.get('price')
		app_version = request.form.get('app_version')
		category = request.form.get('category')
		developer = request.form.get('Developer')
		app_logo_link = request.form.get('app_logo_link')
		cnxn = pyodbc.connect(r'Driver={SQL Server};Server=DEVILSDEN;Database=Python_project;Trusted_Connection=yes;timeout=5000')
		cursor = cnxn.cursor()
		try:
			cursor.execute("insert into application values (?,?,GETDATE(),?,?,?,?,?,?)",app_id,app_name,app_size,price,app_version,category,developer,app_logo_link)
			cnxn.commit()
			while 1:
				row = cursor.fetchone()
				if row == None:
					break
				items.append(row)
				if not row:
					break
			return render_template('test.html',form=items)
		
		except pyodbc.IntegrityError:
			pass
	items = []
	cnxn = pyodbc.connect(r'Driver={SQL Server};Server=DEVILSDEN;Database=Python_project;Trusted_Connection=yes;timeout=5000')
	cursor = cnxn.cursor()
	cursor.execute("SELECT * from Application")
	while 1:
		row = cursor.fetchone()
		if row == None:
			break
		items.append(row)
		if not row:
			break
	return render_template('test.html',form=items)
	


if __name__ == "__main__":
    app.run(debug=False, use_reloader = False)