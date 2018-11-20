

class User:
   # class to create users
    def __init__(self,userId, username, email, password,role):
        self.userId = userId
        self.username = username
        self.email = email
        self.password_hash = self.create_a_password_for_a_user(password)
        self.role = role


    # # def create_new_user(self):
    # #     global users
    # #     global old_usernames
    # #     sql = '''INSERT INTO users(username, email, password) values('%s', '%s', '%s')'''
    # #     with Database as cursor:
    # #         response = [self.username, self.password_hash, self.email, self.role]
    # #         else:
    # #             return json_response('message', 'failed to create your account.Try again')

    # @staticmethod
    # def create_a_password_for_a_user(password):
    #     return generate_password_hash(password)

    # def verify_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    # @staticmethod
    # def get_user(userId):
    #     for user in users:
    #         if userId in user.keys():
    #             return user[userId]

    # @staticmethod
    # def login(username, password):
    #     for username in old_usernames:
    #         if user['username'] == username:
    #             userId = user['Id']
    #             if check_password_hash(User.get_user(userId), password):
    #                 return True
    #             else:
    #                 return False

    # @staticmethod
    # def get_userId_by_username(username):
    #     for username in old_usernames:
    #         if user['username'] == username:
    #             userId = user['Id']
    #             return userId


    # @staticmethod
    # def logout():
    #     return True
