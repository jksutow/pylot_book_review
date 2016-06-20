from system.core.controller import *
from flask import redirect, request, flash

class Books(Controller):
    def __init__(self, action):
        super(Books, self).__init__(action)

        self.load_model('Book')
        self.load_model('User')
        self.db = self._app.db

    # def create(self):
    #     # session ['user']['id'] == author id
    #     self.models['Review'].create_review(request.form, session['user']['id'])
    #     return redirect('/users/{}'.format(request.form['user_id']))

    def add(self):
        user = self.models['User'].fetch_user_by_id(session['user']['id'])
        return self.load_view('reviews/add.html', user=user)

    def create(self):
        book_info = request.form
        user_id = session['user']['id']
        book_id=session['user']['id']
        result = self.models['Book'].create_book(user_id, book_info)
        return redirect('/user')

    def show(self, id):
        book_id = id
        book_info = self.models['Book'].book_info(book_id)
        reviews = self.models['Book'].get_reviews(book_id)
        return self.load_view('reviews/book.html', book_info=book_info, reviews=reviews, id=id)
    # def show(self, id):

    def update(self, id):
        user_id = session['id']
        book_id = id
        info = request.form
        reviews = self.models['Book'].add_reviews(user_id, book_id, info)
        return redirect('/books/'+str(reviews))

    def destroy(self, id):
        review_id = id
        delete_review = self.models['Book'].destroy(review_id)
        return redirect('/books/'+str(delete_review))
