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
    
    def put(self, username, firstname, lastname,  email, city, country, password):

        response = self.table.put_item(
            Item={
                self.Primary_Column_Name: username,
                self.columns[0]: firstname,
                self.columns[1]: lastname,
                self.columns[2]: email,
                self.columns[3]: city,
                self.columns[4]: country,
                self.columns[5]: self.hash_password(password)
            }
        )

    def create_after_verification(self, username, firstname, lastname,  email, city, country, password):
        if self.username_vacant(username) and self.email_vacant(email):
            self.put(username, firstname, lastname,  email, city, country, password)
            return True
        else:
            return False

    def username_vacant(self, username): #checks if username does not exist in the database
        response = self.table.scan(FilterExpression=Attr("Username").eq(username))
    
        if response["Items"] == []:
            return True
        else:
            return False

    def email_vacant(self, email): #checks if email does not exist in the database
        response = self.table.scan(
            FilterExpression = Attr("Email").eq(email)
            )
        if response["Items"] == []:
            return True
        else:
            return False
    
    def de_hash_password(self, password, hashed):
        if bcrypt.checkpw(password, hashed):
            return True
        else:
            return False

    def authincate_user(self, user, password):
        response = self.table.scan(FilterExpression=Attr("username").eq(user))

        if (len(response["Items"]) > 0):
            hased = response['Items'][0]["password"].encode("utf-8")
            self.de_hash_password(password.encode("utf-8"), hased)
            verification = self.de_hash_password(password.encode("utf-8"), hased)
            
            if (verification):
                return {
                    "Result": True,
                    "Error": None,
                    "City": response['Items'][0]["currentcity"],
                    "Country": response['Items'][0]["currentcountry"],
                    "FirstName": response['Items'][0]["firstname"],
                    "LastName": response['Items'][0]["lastname"],
                    "Email": response['Items'][0]["email"],
                    "Username": response['Items'][0]["username"]
                }
            else:
                return {
                    "Result": False,
                    "Error": "Password incorrect",
                    "City": None,
                    "Country": None
                }
        else:
            return {
                "Result": False,
                "Error": "Username not found",
                "City": None,
                "Country": None
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

    def update_user(self, username, firstname, lastname,  email, city, country, password):

        response = self.table.scan(
            FilterExpression=Attr("username").eq(username)
        )

        if password is None:
            password = response['Items'][0]["password"]
        else:
            password = self.hash_password(password)

        if len(response["Items"]) > 0:
            res = self.table.update_item(
                Key={
                    'username': username
                },
                UpdateExpression="set city=:d, country=:t, firstname=:l, lastname=:c, email=:s, password=:z",
                ExpressionAttributeValues={
                    # ':n': New_BlogName,
                    ':d': city,
                    ':t': country,
                    ':l': firstname,
                    ':c': lastname,
                    ':s': email,
                    ':z': password
                }

            )

            if res["ResponseMetadata"]["HTTPStatusCode"] == 200:
                return {
                    "Result": True,
                    "Error": None,
                    "Description": "User was updated successfully",
                }
            else:
                return {
                    "Result": False,
                    "Error": "Database error",
                    "Description": "Database error",
                }

        else:
            return {
                "Result": False,
                "Error": "DB error",
                "Description": "User info was not updated"
            }
    

    # def password_verification(self,username,password):
    #     response = self.table.scan(FilterExpression=Attr("Username").eq(username))
        
    #     if len(response["Items"]) > 0:
    #         original_password = response["Items"][0]["password"]

    #         self.de_hash_password(password.encode("utf-8"), hased)
    #         if self.de_hash_password(original_password.encode) == password:
    #             return {"Result": True,
    #                     "Error": None,
    #                     "Description": "Password was verified"}
    #         else:
    #             return {"Result": False,
    #                     "Error": "Password error",
    #                     "Description": "Password was not verified"}
    #     else:
    #         return {"Result": False,
    #                     "Error": "Password error",
    #                     "Description": "Password was not verified"}

    def update_password(self, username, password):
        response = self.table.scan(FilterExpression=Attr("username").eq(username)) #get reponse from DynamoDB

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
            FilterExpression=Attr("username").eq(username)
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

    
    
    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        """
        above hased is a byte stream; below we decode back into a striing and save pw as string
        """
        return hashed.decode("utf-8")

    