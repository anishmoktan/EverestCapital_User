import boto3 #to connect our information to AWS DynamoDB
from boto3.dynamodb.conditions import Attr
import bcrypt #library for cryting password


class Users:
    def __init__ (self):
        self.__Tablename__ = "EverestCapital_Users"
        self.client = boto3.client('dynamodb')
        self.DB = boto3.resource('dynamodb')
        self.Primary_Column_Name = "Username"
        # self.Primary_key = 1
        self.columns = ["Firstname", "Lastname", "Email", "Password", "City","Country"]   # providing values for the colmuns
        self.table = self.DB.Table(self.__Tablename__)
    
    def put(self, username, firstname, lastname, email, city, country, password): #to create account
        if verify_username_exists(username) and verify_email_exists(email):
            response = self.table.put_item(
                    Item = {
                        self.Primary_Column_Name: username,
                        self.columns[0]: firstname,
                        self.columns[1]: lastname,
                        self.columns[2]: email,
                        self.columns[3]: city,
                        self.columns[4]: country,
                        self.columns[5]: self.hash_password(password)
                    }
                )
            return True
        else:
            return False

    def verify_username_exists(self, username): #checks if username already exists
        response = self.table.scan(FilterExpression=Attr("Username").eq(username))
        if response["Items"] == []:
            return True
        else:
            return False

    def verify_email_exists(self, email): #checks if email already exists
        response = self.table.scan(FilterExpression=Attr("Email").eq(email))
        if response["Items"] == []:
            return True
        else:
            return False

    def update_account(self, username, firstname, lastname, email, city, country, password): #change values in the column
        if verify_username_exists(username) and verify_email_exists(email):
            response = self.table.put_item(
                    Item = {
                        self.Primary_Column_Name: username,
                        self.columns[0]: firstname,
                        self.columns[1]: lastname,
                        self.columns[2]: email,
                        self.columns[3]: city,
                        self.columns[4]: country,
                        self.columns[5]: self.hash_password(password)
                    }
                )
            return True
        else:
            return False

    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    
    def de_hash_password(self, password, hashed):
        if bcrypt.checkpw(password, hashed):
            return True
        else:
            return False

    def update_password(self, username, password):
        response = self.table.scan(FilterExpression=Attr("username").eq(user)) #get reponse from DynamoDB

        if len(response["Items"]) > 0: # if the response contains a user we bgan to presver dat such as the user city, country, name, etc,
            
            firstname = response["Items"][0]["firstname"]
            lastname = response["Items"][0]["lastname"]
            email = response["Items"][0]['email']
            city = response["Items"][0]["city"]
            country = response["Items"][0]["country"]
            
          
            response = self.table.put_item(
                Item = {
                        self.Primary_Column_Name: username,
                        self.columns[0]: firstname,
                        self.columns[1]: lastname,
                        self.columns[2]: email,
                        self.columns[3]: city,
                        self.columns[4]: country,
                        self.columns[5]: self.hash_password(password)
                    }
                 )
            return{
                "Result": True,
                "Error": None,
                "Description": "User password updated"
            }
        else:
            return{
                "Result": False,
                "Error": "DB Error",
                "Description": "User password was not updated. No such user exists."
            }

    def update_username(self, username, password):
        response = self.table.scan(
            FilterExpression=Attr("username").eq(user)
        )

        if len(response["Items"]) > 0: # if the response contains a user we bgan to presver dat such as the user city, country, name, etc,

            firstname = response["Items"][0]["firstname"]
            lastname = response["Items"][0]["lastname"]
            email = response["Items"][0]['email']
            city = response["Items"][0]["city"]
            country = response["Items"][0]["country"]
          
            response = self.table.put_item(
                Item = {
                        self.Primary_Column_Name: username,
                        self.columns[0]: firstname,
                        self.columns[1]: lastname,
                        self.columns[2]: email,
                        self.columns[3]: city,
                        self.columns[4]: country,
                        self.columns[5]: self.hash_password(password)
                    }
                 )
            return{
                "Result": True,
                "Error": None,
                "Description": "User password updated"
            }
        else:
            return{
                "Result": False,
                "Error": "DB Error",
                "Description": "User password was not updated. No such user exists."
            }

        def delete_account(self, username):
        response = self.table.scan(FilterExpression = Attr("username").eq(username))

        if len(response["Items"]) > 0:
            res = self.table.delete_item(Key={self.Primary_Column_Name:username})
            return {
                "Result": True,
                "Error": None,
                "Description": "Account was deleted"
                }
        else:
            return {
                 "Result": False,
                 "Error": "Account does not exist in database"
                }