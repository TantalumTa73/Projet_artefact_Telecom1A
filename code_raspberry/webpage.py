# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request
import controller
import time
import datetime
import module_camera


# Moteurs 

c = controller.Controller()
c.set_motor_shutdown_timeout(2)
c.standby()

# Flask constructor takes the name of 
# current module (__name__) as argument.
app = Flask(__name__)

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.


@app.route('/', methods=['GET','POST'])
def page():
	global c 

	if request.method == 'POST':
		if request.form['button'] == '1':
			c.set_raw_motor_speed(100,100)
		if request.form['button'] == '2':
			c.standby()

	# If the method is GET,render the HTML page to the user
	#if request.method == 'GET':
	#return 

	return render_template("page.html")	

@app.route('/slider', methods=['POST'])
def slider():
	global c 

	if request.method == 'POST':
		number = int(request.form['valeur'])
		c.set_raw_motor_speed(-number,number)
	return render_template("page.html")	


@app.route('/update')
def update():
    """send current content"""
    #return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    return "test_camera"



# main driver function
if __name__ == '__main__':
	# run() method of Flask class runs the application 
	# on the local development server.
	#app.run()
	app.run(debug=False,host="0.0.0.0")

