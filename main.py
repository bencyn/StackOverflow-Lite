from flask import Flask,request,jsonify

app = Flask(__name__)

users =[]


def _validator(user):
    for key,value in user.items():
        if key == 'name' or key == 'value':
            if len(value) < 5:
                return jsonify({
                    "err": "{} is too short".format(key)
                })

@app.route("/")
def index():
    return "Http Homepage %s"% request.method

# user signup and get users
@app.route("/register", methods=['POST'])
def register():
    """user signup"""
    data = request.get_json()
    if not data:
        return jsonify({"Message": 'Cannot send empty data'})
    if not all(field in data for field in ['username', 'email','password']):
        return jsonify({"Message": "All fields are required"})

    username = request.get_json()['username']
    email = request.get_json()['email']
    password = request.get_json()['password']
    user = {
        "username": username,
        "email": email,
        "password":password
    }
    users.append(user)

    return jsonify({'user': user}), 201


@app.route("/users", methods=['GET'])
def getUsers():
    if request.method == 'GET':
        return jsonify(users)

if __name__=="__main__":
    app.run(debug=True)