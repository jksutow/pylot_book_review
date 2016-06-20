from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)

        self.load_model('User')
        self.load_model('Book')
        self.db = self._app.db

    # display book review pg w/ 3 current reviews
    def index(self):
        user = self.models['User'].fetch_user_by_id(session['user']['id'])
        return self.load_view('reviews/show.html', user=user)

    def register(self):
        #validate registration information
        validation_result = self.models['User'].validate_reg_info(request.form)
        return self.handle_login_reg_response(validation_result)

    def handle_login_reg_response(self, result):
        if type(result) == list:
            session['val_errors'] = result
            return redirect('/')
        self.set_user_session(result)
        return redirect('/user')

    def set_user_session(self, validation_result):
        session['user'] = validation_result
        return

    def login(self):
        login_result = self.models['User'].login(request.form)
        return self.handle_login_reg_response(login_result)
        return redirect('/books')

    def home(self):
        recent_reviews = self.models['Book'].recent_reviews()
        other_reviews = self.models['Book'].other_reviews()
        return self.load_view('reviews/show.html', recent_reviews = recent_reviews, other_reviews = other_reviews)

    def show(self, id):
        user_id = id
        user_info = self.models['User'].user_info(user_id)
        total_reviews = self.models['Book'].total_reviews(user_id)
        review_titles = self.models['Book'].review_titles(user_id)
        return self.load_view('reviews/user.html', user_info=user_info, total_reviews=total_reviews, review_titles=review_titles)

    def logout(self):
        session.pop=['id']
        session.pop=['name']
        return redirect('/')
