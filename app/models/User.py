from system.core.model import Model
#import for email regex
import re
# regex for email
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()
        # make dictionary to keep track of errors
        self.validation_errors = {
            'name_exist': "Name can't be blank",
            'email_exist': "Email can't be blank",
            'email_valid': "Email must be valid",
            'alias_exist': "Alias can't be blank",
            'password_exist': "Password can't be blank",
            'password_match': "Passwords must match",
            'password_length': "Password must be at least 8 characters",
            'email_taken': "Email already in use",
            'login_fail': "Email/password don't match"
        }
        self.queries = {
            'get_user_by_email': "SELECT * FROM users WHERE email = :email LIMIT 1",
            'create_user': "INSERT INTO users (name, alias, email, pw_hash, created_at, updated_at) VALUES (:name, :alias, :email, :pw_hash, NOW(), NOW())",
            'fetch_user_by_id': "SELECT id, name, alias, email FROM users WHERE id = :id ",
            'fetch_all_users': "SELECT id, name, alias, email, created_at FROM users WHERE id = :id"
        }

    def login(self, form_data):
        result = self.get_user_by_email(form_data['email'])
        password = form_data['password']
        pw_hash = result[0]['pw_hash']

        # Check to see if password and pw_hash match
        test_password_result = self.bcrypt.check_password_hash(pw_hash, password)
        if test_password_result == False:
            return [self.validation_errors['login_fail']]
        else:
            return {
                'id': result[0]['id'],
                'name': result[0]['name'],
                'alias': result[0]['alias'],
                'email': result[0]['email']
            }
    def get_user_by_email(self, email):
        query = self.queries['get_user_by_email']
        data = {
            'email': email
        }
        return self.db.query_db(query, data)

    def register(self, form_data):
        #Encrypt password
        pw_hash = self.bcrypt.generate_password_hash(form_data['password'])

        # Make a DB query to create a user
        query = self.queries['create_user']
        data = {
            'name': form_data['name'],
            'alias': form_data['alias'],
            'email': form_data['email'],
            'pw_hash': pw_hash
        }

        result = self.db.query_db(query, data)

        return self.fetch_user_by_id(result)

    def fetch_user_by_id(self, id):
        query = self.queries['fetch_user_by_id']
        data = {
            'id': id
        }
        result = self.db.query_db(query, data)
        return result[0]

    def fetch_all_users(self, id):
        query = self.queries['fetch_all_users']
        data = {
            'id': id
        }
        result = self.db.query_db(query, data)
        return result

    def user_info(self, user_id):
        user_id_query = "SELECT * FROM users WHERE id = {}".format(user_id)
        user = self.db.query_db(user_id_query)
        return user[0]
        
    def validate_reg_info(self, form_data):
        errors = []

        # Validate the following data:
        # Make sure name, email, password exist
        if len(form_data['name']) < 1:
            errors.append(self.validation_errors['name_exist'])
        if len(form_data['alias']) < 1:
            errors.append(self.validation_errors['alias_exist'])
        if len(form_data['email']) < 1:
            errors.append(self.validation_errors['email_exist'])
        if not EMAIL_REGEX.match(form_data['email']):
            errors.append(self.validation_errors['email_valid'])
        if len(form_data['password']) < 1:
            errors.append(self.validation_errors['password_exist'])
        if len(form_data['password']) < 8:
            errors.append(self.validation_errors['password_length'])
        # Make sure password/password confirm match
        if form_data['password'] != form_data['password_confirm']:
            errors.append(self.validation_errors['password_match'])

        # Do errors exist? If so, don't bother with DB query...
        if len(errors) > 0:
            return errors

        # Want to grab users by email
        result = self.get_user_by_email(form_data['email'])

        # Make sure email isn't already in database
        if len(result) > 0:
            errors.append(self.validation_errors['email_taken'])
            return errors

        # If we're here, we know all validations passed, so can register users
        return self.register(form_data)
