import json
import hashlib
import flask_login



class User(flask_login.UserMixin):
    # Constructor
    def __init__(self,user):
        self.id = user["userid"]
        self.name = user["username"]
        self.active = user["active"]
        self.authenticated = True


    # Override
    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return self.authenticated and self.is_active
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
    

    # Getter
    def get_from_id(user_id):
        # Check if user really exists
        f = open("keys/users.json",mode="r",encoding="utf-8")
        userlist = json.loads(f.read())
        f.close()

        for user in userlist:
            if user["userid"] == user_id:
                return User(user)

        return None

    # Authentication
    def authenticate_user(username, password):
        # Check if user really exists
        f = open("keys/users.json",mode="r",encoding="utf-8")
        userlist = json.loads(f.read())
        f.close()

        user = None

        for elem in userlist:
            if elem["username"] == username:
                if elem["hashed_password"] == hashlib.md5(password.encode("utf-8")).hexdigest():
                    user = elem
                    break

        # Incorrect login
        if user == None:
            return None
        
        # Build the user
        return_user = User(user)
        return return_user


    # Change password
    def change_password(user,old_password,new_password):
        # Check if user really exists
        f = open("keys/users.json",mode="r",encoding="utf-8")
        userlist = json.loads(f.read())
        f.close()

        user = None

        for elem in userlist:
            if elem["username"] == user.name:
                if elem["hashed_password"] == hashlib.md5(old_password.encode("utf-8")).hexdigest():
                    user = elem
                    break

        # Incorrect login
        if user == None:
            return False
        
        # Good user, change the password
        new_userlist = list()
        for elem in userlist:
            if elem == user:
                user["hashed_password"] = hashlib.md5(new_password.encode("utf-8")).hexdigest()
                new_userlist.append(user)
            else:
                new_userlist.append(elem)

        f = open("keys/users.json",mode="w",encoding="utf-8")
        f.write(json.dumps(new_userlist))
        f.close()

        return True
    
    # Create User
    def create_user(username,password):
        # Check if user really exists
        f = open("keys/users.json",mode="r",encoding="utf-8")
        userlist = json.loads(f.read())
        f.close()

        user = None
        chosen_userid = 1

        for elem in userlist:
            if elem["userid"] == chosen_userid:
                chosen_userid += 1
            if elem["username"] == username:
                user = elem
                break

        # User already exists login
        if user != None:
            return False
        
        # New user, add it to the database
        new_userlist = userlist
        new_user = dict()
        new_user["userid"] = chosen_userid
        new_user["active"] = True
        new_user["username"] = username
        new_user["hashed_password"] = hashlib.md5(password.encode("utf-8")).hexdigest()
        new_userlist.append(new_user)

        new_userlist.sort(key=lambda i: int(i["userid"]), reverse=False)

        f = open("keys/users.json",mode="w",encoding="utf-8")
        f.write(json.dumps(new_userlist))
        f.close()

        return True