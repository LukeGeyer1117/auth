from flask import Flask, jsonify, request
from flask_cors import cross_origin # needed!
from cli import addguest, addhost, addCampground, addCampsite, addReservation, findHost, findGuest, getcampgrounds, deleteCampground, editCampground, getmreservations, checkEmail
from passlib.hash import bcrypt

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Campsight App!"

@app.route('/addguest', methods=['POST'])
@cross_origin()
def add_guest_route():
    # Route to run the addguest click command
    # print('calling addguest')
    data = request.get_json()
    if not data:
        return jsonify({'error' : 'No JSON data received'}), 400
    
    username = data.get("username")
    f_name = data.get("f_name")
    l_name = data.get("l_name")
    password = data.get("password")
    email = data.get("email")

    password = bcrypt.hash(password)

    if not username or not f_name or not l_name or not password or not email:
        return jsonify({'error' : 'Invalid or empty request'}), 400

    try:
        addguest.main([username, f_name, l_name, password, email], standalone_mode=False)
        return jsonify({"message": f"Guest {username} added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/addhost', methods=['POST'])
@cross_origin()
def add_host_route():
    # Route to run the addhost click command
    data = request.get_json()
    if not data:
        return jsonify({'error' : 'No JSON data received'}), 400
    
    username = data.get("username")
    f_name = data.get("f_name")
    l_name = data.get("l_name")
    password = data.get("password")
    email = data.get("email")

    password = bcrypt.hash(password)

    if not username or not f_name or not l_name or not password or not email:
        return jsonify({'error' : 'Invalid or empty request'}), 400

    try:
        addhost.main([username, f_name, l_name, password, email], standalone_mode=False)
        return jsonify({"message": f"Host {username} added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/loginhost', methods=['GET', 'POST'])
@cross_origin()
def host_login_route():
    if request.method == 'POST':
        # Get the data from the form
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        print(email, password)

        if not email or not password:
            return jsonify({'error' : 'email and password are required!'})
        
        try:
            # try to find the host account
            host_account = findHost.main([email], standalone_mode=False)
            if host_account:
                host_data = {
                    'id': host_account[0],
                    'username': host_account[1],
                    'fname' : host_account[2],
                    'lname' : host_account[3],
                    'password': host_account[4],  # Consider NOT sending this for security reasons!
                    'email': host_account[5]
                }
                # Return a json so frontend can redirect to home page
                return jsonify({'message' : 'Host found!', 'host': host_data}), 200
            else:
                return jsonify({'error' : 'Invalid credentials'}), 401
        except Exception as e:
            return jsonify({'error' : str(e)}), 500
        
@app.route('/loginguest', methods=['GET', 'POST'])
@cross_origin()
def guest_login_route():
    if request.method == 'POST':
        # Get the data from the json
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({'error' : 'email and password are required!'})
        
        try:
            # try to find the guest account
            guest_account = findGuest.main([email], standalone_mode=False)
            print(guest_account)
            if guest_account:
                guest_data = {
                    'id': guest_account[0],
                    'username': guest_account[1],
                    'fname' : guest_account[2],
                    'lname' : guest_account[3],
                    'password': guest_account[4],
                    'email': guest_account[5]
                }
                print(password, guest_data['password'])
                if bcrypt.verify(password, guest_data['password']):
                    return jsonify({'message' : 'Guest found!', 'guest': guest_data}), 200
                else:
                    return jsonify({'error' : 'Invalid Credentials'}), 401
            else:
                return jsonify({'error' : 'Invalid credentials'}), 401

        except Exception as e:
            return jsonify({'error' : str(e)}), 500

@app.route('/campgrounds', methods = ['POST'])
@app.route('/campgrounds/<int:c_id>', methods = ['DELETE', 'PUT'])
@cross_origin()
def campground_route(c_id = None):
    # Add a new campground
    if request.method == 'POST':
        data = request.get_json()
        name = data.get("name")
        address = data.get("address")
        description = data.get("description")
        host_id = data.get("host_id")
        try:
            host_id = int(host_id)
        except:
            return jsonify({'message' : 'invalid host_id'}), 400
        
        if not name or not host_id or not address:
            return jsonify({"error" : "Invalid or empty request."}), 400
        
        try:
            print('trying to add campground')
            print(name, type(host_id), address)
            addCampground.main([name, str(host_id), address, description], standalone_mode=False)
            return jsonify({'message' : 'successfully added campground'})
        except Exception as e:
            return jsonify({'error' : str(e)}), 500
        
    # Edit a campground's description
    elif request.method == 'PUT':
        # run the editCampground click command
        data = request.get_json()
        description = data.get("description")

        if not c_id or not description:
            return jsonify({'error' : 'missing campground_id or description'})

        try:
            print(f"Editing campground with ID: {c_id} and new description: {description}")
            editCampground.main([str(c_id), description])
            return jsonify({'message' : 'successfully edited campground'}), 200
        except Exception as e:
            return jsonify({'error' : str(e)}), 500
    
    # Delete a campground
    elif request.method == 'DELETE':
        # run the delete campground click command
        # data = request.get_json()
        # c_id = data.get("c_id")

        if not c_id:
            return jsonify({'error' : 'no campground_id received'})

        try:
            deleteCampground.main([str(c_id)], standalone_mode=False)
            return jsonify({'message': 'successfully deleted campground'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
@app.route('/campgrounds/<int:host_id>', methods = ['GET'])
@cross_origin()
def get_campground(host_id):
    if request.method == "GET":
        # run the getcampgrounds click command
        if not host_id:
            return jsonify({"error" : "No data or no host id"})
        
        # Call click command to get all campgrounds managed by the current host
        try:
            campgrounds = getcampgrounds.main([str(host_id)], standalone_mode=False)
            if not campgrounds:
                return jsonify({'message' : 'no campgrounds associated'}), 200
            return jsonify({'campgrounds' : campgrounds}), 200
        except Exception as e:
            return jsonify({'error at get' : str(e)}), 500

        


@app.route('/campsites', methods=['POST'])
@cross_origin()
def campsite_route():
    # Create a new campsite
    if request.method == "POST":
        data = request.get_json()
        campground_id = data.get("c_id")

        if not campground_id:
            return jsonify({"error" : "no valid campground id"})
        
        try:
            addCampsite.main([campground_id], standalone_mode=False)
            return jsonify({"message" : f"Created campsite for campground {campground_id}"})
        except Exception as e:
            return jsonify({"error" : str(e)}), 500

    
@app.route('/addreservation', methods=['POST'])
def add_reservation_route():
    # Route to run the addReservation click command
    guest_id = request.form.get("guest_id")
    campground_id = request.form.get("campground_id")
    campsite_id = request.form.get("campsite_id")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if not guest_id or not campground_id or not campsite_id or not start_date or not end_date:
        return jsonify({"error" : "invalid or empty request"})
    
    try:
        if not addReservation.main([guest_id, campground_id, campsite_id, start_date, end_date], standalone_mode=False):
            return jsonify({'message' : 'reservation could not be created due to overlap with other reservation'})
        return jsonify({'message' : "created reservation"})
    except Exception as e:
        return jsonify({'error' :  str(e)})
    
@app.route('/getmanaged', methods=['POST'])
@cross_origin()
def get_managed_route():
    data = request.get_json()
    if not data:
        return jsonify({'error' : 'no JSON data received'})
    host_id = data.get("id")
    if not host_id:
        return jsonify({'error' : 'missing required parameter: id'}), 400
    # Call click command to get all campgrounds managed by the current host
    try:
        campgrounds = getcampgrounds.main([str(host_id)], standalone_mode=False)
        if not campgrounds:
            return jsonify({'message' : 'no campgrounds associated'})
        return jsonify({'campgrounds' : campgrounds})
    except Exception as e:
        return jsonify({'error at get' : str(e)}), 500
    
@app.route('/getmreservations', methods=['POST'])
@cross_origin()
def get_managed_reservations():
    data = request.get_json()
    if not data:
        return jsonify({'error' : 'no JSON data received'})
    host_id = data.get("id")
    if not host_id:
        return jsonify({'error': 'missing required parameter: id'}), 400
    # Call the click command to get all reservations to campgrounds you manage
    try:
        reservations = getmreservations.main([str(host_id)], standalone_mode=False)
        if not reservations:
            return jsonify({'message' : 'no reservations associated'})
        return jsonify({'reservations' : reservations})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    
@app.route('/email', methods=['POST'])
@cross_origin()
def check_for_email():
    data = request.get_json()
    if not data:
        return jsonify({'error' : 'no JSON data received'})
    email = data.get("email")
    if not email:
        return jsonify({'error' : 'missing required parameter : email'}), 400
    # Call the click command to see if the email is in the hosts or guest table
    try:
        emailAvailable = checkEmail.main([email], standalone_mode=False)
        if emailAvailable:
            return jsonify({'message' : 'email is valid'}), 200
        else:
            return jsonify({'error' : 'email is already in use'}), 400
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    
def run():
    app.run(port=8080, host='0.0.0.0')

if __name__ == '__main__':
    # uncomment the line below to show all api routes
    # print(app.url_map) 
    app.run(debug=True)