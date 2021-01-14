from flask import Flask, request
from devbops_user_microservice.user_functions import Users
#from user_functions import Users
user = Users()
app = Flask(__name__)


@app.route('/register', methods=['POST'])
def signup():
    res = request.json
    username = res["Username"]
    firstname = res["FirstName"]
    lastname = res["LastName"]
    email = res["Email"]
    city = res["City"]
    country = res["Country"]
    password = res["Password"]

    if user.create_after_verification(username=username, firstname=firstname, lastname=lastname, email=email, city=city, country=country, password=password):
        return {
            "Result": True,
            "Error": None
        }
    else:
        return {
            "Result": False,
            "Error": "Username or email is already taken"
        }


@app.route("/login", methods=['POST'])
def login():
    res = request.json
    username = res["Username"]
    password = res["Password"]
    login = user.authincate_user(username=username, password=password)
    # return dict{}
    return login #returns what is written in the class


@app.route("/delete", methods=['POST'])
def delete():
    res = request.json
    username = res["Username"]
    deleted = user.delete_account(username=username)
    return deleted


@app.route("/update-user-info", methods=["POST"]) #updates everything in an account
def update_info():
    res = request.json
    username = res["Username"]
    firstname = res["FirstName"]
    lastname = res["LastName"]
    email = res['Email']
    city = res["City"]
    country = res["Country"]
    password = res['Password']

    updated_user = user.update_user(username=username, firstname=firstname, lastname=lastname, email=email, city=city, country=country, password=password)
    return updated_user


if __name__ == "__main__":
    app.run(debug=True)