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
    
    def put(self, username, firstname, lastname,  email, city, country, password): #Uploads to DB right away

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

    def create_after_verification(self, username, firstname, lastname, email, city, country, password):
        if self.username_vacant(username) and self.email_vacant(email): #Uses True and False from the functions
            self.put(username, firstname, lastname, email, city, country, password)
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
    
    def hash_password(self, password):
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()) #Takes in the password and encodes
        #"""
        #above hased is a byte stream; below we decode back into a striing and save pw as string
        #"""
        return hashed.decode("utf-8") #Returns the hashed password

    def de_hash_password(self, password, hashed): #Takes in password entered and hashed passowrd from the DB
        if bcrypt.checkpw(password, hashed): #Compares the two
            return True #True if they match
        else:
            return False #False if they don't

    def authincate_user(self, username, password): #Used for logging in the website
        response = self.table.scan(FilterExpression=Attr("username").eq(username)) #scans DynamoDB for the username and sets it as reponse if found

        if (len(response["Items"]) > 0): #If found
            hased = response['Items'][0]["password"].encode("utf-8") #Encodes the password in the DB
            #self.de_hash_password(password.encode("utf-8"), hased)
            verification = self.de_hash_password(password.encode("utf-8"), hased) #Compares the password entered and password in the DB
            
            if (verification):
                return {
                    "Result": True,
                    "Error": None,
                    "Username": response['Items'][0]["username"], #What is received from DynamoDB
                    "Firstname": response['Items'][0]["firstname"],
                    "LastName": response['Items'][0]["lastname"],
                    "Email": response['Items'][0]["email"],
                    "City": response['Items'][0]["city"],
                    "Country": response['Items'][0]["country"]
                }

            else:
                return {
                    "Result": False,
                    "Error": "Password incorrect",
                    "City": None,
                    "Country": None
                }

        else: #Triggered if username not found in DynamoDB
            return {
                "Result": False,
                "Error": "Username not found",
                "City": None,
                "Country": None
            }

    def delete_account(self, username):
        response = self.table.scan(FilterExpression = Attr("username").eq(username))

        if len(response["Items"]) > 0:
            res = self.table.delete_item( Key = {self.Primary_Column_Name:username})
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

        response = self.table.scan(FilterExpression=Attr("username").eq(username))

        if password is None:
            password = response['Items'][0]["password"]
        else:
            password = self.hash_password(password)

        if len(response["Items"]) > 0:
            res = self.table.update_item(
                Key = {
                    'username': username
                },
                UpdateExpression = "set firstname=:d, lastname=:t, email=:l, city=:c, country=:s, password=:z",
                ExpressionAttributeValues = {
                    # ':n': New_BlogName,
                    ':d': firstname,
                    ':t': lastname,
                    ':l': email,
                    ':c': city,
                    ':s': country,
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

    # def update_password(self, username, password): #Updates the DB by first getting back the response
    #     response = self.table.scan(FilterExpression=Attr("username").eq(username)) #Sets response at the index for the username

    #     if len(response["Items"]) > 0: 

    #         firstname = response["Items"][0]["firstname"]
    #         lastname = response["Items"][0]["lastname"]
    #         email = response["Items"][0]['email']
    #         city = response["Items"][0]["city"]
    #         country = response["Items"][0]["country"]
          
    #         response = self.table.put_item(
    #             Item = {
    #                     self.Primary_Column_Name: username,
    #                     self.columns[0]: firstname,
    #                     self.columns[1]: lastname,
    #                     self.columns[2]: email,
    #                     self.columns[3]: city,
    #                     self.columns[4]: country,
    #                     self.columns[5]: self.hash_password(password)
    #                 }
    #              )
    #         return{
    #             "Result": True,
    #             "Error": None,
    #             "Description": "User password updated"
    #         }
    #     else:
    #         return{
    #             "Result": False,
    #             "Error": "DB Error",
    #             "Description": "User password was not updated. No such user exists."
    #         }

    # def update_username(self, username, password):
    #     response = self.table.scan(
    #         FilterExpression=Attr("username").eq(username)
    #     )

    #     if len(response["Items"]) > 0: # if the response contains a user we bgan to presver dat such as the user city, country, name, etc,

    #         firstname = response["Items"][0]["firstname"]
    #         lastname = response["Items"][0]["lastname"]
    #         email = response["Items"][0]['email']
    #         city = response["Items"][0]["city"]
    #         country = response["Items"][0]["country"]
          
    #         response = self.table.put_item(
    #             Item = {
    #                     self.Primary_Column_Name: username,
    #                     self.columns[0]: firstname,
    #                     self.columns[1]: lastname,
    #                     self.columns[2]: email,
    #                     self.columns[3]: city,
    #                     self.columns[4]: country,
    #                     self.columns[5]: self.hash_password(password)
    #                 }
    #              )
    #         return{
    #             "Result": True,
    #             "Error": None,
    #             "Description": "User password updated"
    #         }
    #     else:
    #         return{
    #             "Result": False,
    #             "Error": "DB Error",
    #             "Description": "User password was not updated. No such user exists."
    #         }