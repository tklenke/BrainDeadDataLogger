# app.py or app/__init__.py
from flask import Flask, render_template, request, send_file
import re
import threading
import time, datetime
import os
import csv
import pygal

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config.from_object('config')


# Now we can access the configuration variables via app.config["VAR_NAME"].
DEBUG=app.config["DEBUG"]

@app.route("/")
def home():
    return render_template('home.html')
    
@app.route("/initstream/<stream_name>")
def initialize_stream(stream_name):
	if invalid_key():
		return ("0 invalid key".format(stream_name))
	if invalid_stream_name(stream_name):
		return ("0 invalid stream name:{}".format(stream_name))
		
	#create header row for CSV file
	cols = sorted(request.args.keys(), key=int)  #need to convert to integer during sort
	hrow = '"timestamp"'
	numcols = 0
	for c in cols:
		if request.args[str(c)] == '0':
			continue
		hrow += ',"' + request.args[c].replace('"','""') + '"'
		numcols +=1
		
	#check to see if max columns exceeded
	if numcols > app.config["MAX_COLUMNS"]:
		return ("0 number of columns {} exceeds max columns of {}".format(numcols,app.config["MAX_COLUMNS"]))
		
	#check to see if the file exists -- if so then move it, otherwise open it
	fname = "{}/{}.csv".format(app.config["PATH_TO_DATA"],stream_name) 

	if os.path.isfile(fname):	
		#create filename (path + stream name + year,mon,day,h,m,s)
		foldname = "{}/{}_{}.csv".format(app.config["PATH_TO_DATA"],stream_name,time.strftime("%Y_%m_%d_%H_%M_%S"))
		os.rename(fname,foldname)
		
	#open file and write header row
	lock = threading.Lock()
	with lock:
		f = open(fname,'w')
		f.write(hrow + "\r\n")	
		f.close()
		
	return ("1 {} stream initialized with {} columns".format(stream_name,numcols))	
#	return render_template('test.html',stream_name=stream_name, hrow=hrow, fname=fname)

@app.route("/log/<stream_name>")
def log_stream(stream_name):
	if invalid_key():
		return ("0 invalid key".format(stream_name))
	if invalid_stream_name(stream_name):
		return ("0 invalid stream name:{}".format(stream_name))
	#check to see if the file exists
	fname = "{}/{}.csv".format(app.config["PATH_TO_DATA"],stream_name) 
	if os.path.isfile(fname) == False:
		return ("0 {} stream not initialized".format(stream_name))
	
	#create row for CSV file
	cols = sorted(request.args.keys(), key=int)  #need to convert to integer during sort
	maxcol = 0
	if len(cols) > 1:
		maxcol = int(cols[-1])
	else:
		maxcol = len(cols)
		
	numdata = 0
	numcols = 0
	row = '"{}",'.format(time.strftime(app.config['TIMESTAMP_FORMAT']))
	for c in range(1,maxcol+1):
		if 	request.args.get(str(c),None) != None:  #count number of entries with data
			#skip the key column
			if request.args[str(c)] == '0':
				continue
			numdata += 1
			#put non-numeric data in quotes
			r = re.compile('^-?(0|[1-9]\d*)(\.\d+)?$')
			s = str(request.args[str(c)])
			if r.match(s):
				row += ',' + s
			else:
				row += ',"' + s.replace('"','""') + '"'
			
		numcols += 1
		
	#open file and write data row
	lock = threading.Lock()
	with lock:
		f = open(fname,'a')
		f.write(row + "\r\n")
		f.close()		
	
	return ("1 {} data elements in {} columns written to stream {}".format(numdata, numcols, stream_name))	

@app.route("/csv/<stream_name>")
def read_stream_as_csv(stream_name):
	if invalid_stream_name(stream_name):
		return render_template('error.html',msg="Invalid stream name"), 404
	#check to see if the file exists
	fname = "{}/{}.csv".format(app.config["PATH_TO_DATA"],stream_name) 
	if os.path.isfile(fname) == False:
		return render_template('error.html',msg="Stream not initialized"), 404
		
	return send_file(fname,mimetype='text/csv',as_attachment=True)
	
@app.route("/table/<stream_name>")
def read_stream_as_table(stream_name):
	if invalid_stream_name(stream_name):
		return render_template('error.html',msg="Invalid stream name"), 404
	#check to see if the file exists
	fname = "{}/{}.csv".format(app.config["PATH_TO_DATA"],stream_name) 
	if os.path.isfile(fname) == False:
		return render_template('error.html',msg="Stream not initialized"), 404
	
	nrows = request.args.get('nrows')
	if nrows:
		nrows=int(nrows)
	
	r = csv.reader(open(fname))
	
	return render_template('table.html',reader=r, nrows=nrows)
	
@app.route("/chart/<stream_name>")
def read_stream_as_chart(stream_name):
	if invalid_stream_name(stream_name):
		return render_template('error.html',msg="Invalid stream name"), 404
	#check to see if the file exists
	fname = "{}/{}.csv".format(app.config["PATH_TO_DATA"],stream_name) 
	if os.path.isfile(fname) == False:
		return render_template('error.html',msg="Stream not initialized"), 404
	out =""
	readr = csv.reader(open(fname))
	hrow = next(readr)
	frow = next(readr)
	numcols = len(frow)
	maxrows = request.args.get('nrows')
	if maxrows:
		maxrows=int(maxrows)
	else:
		maxrows=app.config['DEFAULT_CHART_ROWS']
	
	#set up array of columns using the header row and the first row
	data=[[] for x in range(numcols)]
	for idx, cell in enumerate(frow):
		out += str(idx) + ":" + str(cell) 
		#handle the header row
		if idx < len(hrow):
			data[idx].append(hrow[idx])
			out += ":" + hrow[idx]
		else:
			data[idx].append('blank')
			out += ":blank"
		#handle the cell
		data[idx].append(tonum(cell))
		out += "<br>"
		
	nrows = 1
		
	#get the rest of the rows
	for row in readr:
		nrows += 1
		for idx, cell in enumerate(row):
			try:
				if idx == 0:
					data[idx].append(tonum(cell))
				else:
					data[idx].append(tonum(cell))
			except:
				render_template('error.html', msg="Error reading data. <br>Consider reinitializing if you changed the machine that is posting log data" )
				
	#set up the chart
	bar_chart = pygal.DateTimeLine(x_label_rotation=65)
	bar_chart.title = stream_name
			
	#now make the array of tuples for the columns columns
	#cd = chartdata
	cd = [[] for x in range(numcols)]
	for i in range(1,numcols):
		#put in the description
		cd[i].append(data[i][0] ) 
		for j in range(1,nrows+1):
			cd[i].append((data[0][j],data[i][j]))
		bar_chart.add(cd[i].pop(0),cd[i])

	try:
		chart = bar_chart.render(is_unicode=True)
	except:
		render_template('error.html', msg="Error rendering chart. <br>Consider reinitializing if you changed the machine that is posting log data" )

	return render_template('chart.html', chart=chart )	
	
def invalid_stream_name(name):
	#validate stream name (alpha numeric only)
	r = re.compile('[\W]+')
	if r.search(name):
		return (True)  #true: it is invalid
	else:
		return (False)
		
def invalid_key():
	key = request.args.get('0')
	if key == None or key != app.config['UPDATE_KEY']:
		return True
	return False
		
def tonum(s):
	try:
		return int(s)
	except ValueError:
		try:
			return float(s)
		except ValueError:
			try:
				return datetime.datetime.strptime(s,app.config['TIMESTAMP_FORMAT'])
			except ValueError:
				return None

if __name__ == "__main__":
   app.run(host='0.0.0.0')
