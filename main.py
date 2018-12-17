from flask import Flask,request,jsonify
import re, itertools

app = Flask(__name__)

users =[]
def validate_password(password):
    exp = r'[A-Za-z0-9@#$%^&+=]{8,}'
    if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
        return  True
    else:
        return False

# no match

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

    # print(validate_password(password))
    if validate_password(password) == False:
        return jsonify({"Message": "Invalid Password"})

    if any(i['username'] == username for i in users):
        return jsonify({'msg': 'username already exists'}), 409
    if any(i['email'] == email for i in users):
        return jsonify({'msg': 'email already exists'}), 409
    else:
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


questions = []
counter = itertools.count()
next(counter)

# get questions
@app.route("/questions", methods=['GET'])
def getQuestions():
    return jsonify(questions)

# post question
@app.route("/question/create", methods=['POST'])
def postQuestions():
    data = request.get_json()
    if not data:
        return jsonify({"Message": 'Cannot send empty data'})
    if not all(field in data for field in ['title','description']):
        return jsonify({"Message": "All fields are required"})

    title = request.get_json()['title']
    description = request.get_json()['description']
    count=next(counter)

    question= {
        'id':count,
        'title' : title,
        'description': description
    }

    questions.append(question)

    return jsonify({'question': question}), 201



# update questions

# delete questions

if __name__=="__main__":
    app.run(debug=True)