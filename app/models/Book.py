from system.core.model import Model


class Book(Model):
    def __init__(self):
        super(Book, self).__init__()
        # Put queries in dictionary incase we want to use again
    #     self.queries = {
    #         # 'create_review': "INSERT INTO reviews (review, rating, created_at, updated_at, user_id, book_id) VALUES (:review, :rating, NOW(), NOW(), ,
    #         'author_query': "SELECT * FROM authors WHERE name = :name",
    #         'create_author': "INSERT INTO authors(name, created_at, updated_at) VALUES (:name, NOW(), NOW())",
    #         'get_author': "SELECT * FROM authors ORDER BY id DESC LIMIT 1",
    #         'get_book': "SELECT * FROM books ORDER BY id DESC LIMIT 1",
    #         'create_book': "INSERT INTO books (title, created_at, updated_at) VALUES (:title, NOW(), NOW())",
    #         'book_id': "SELECT id FROM books WHERE id = :id",
    #         'insert_review': "INSERT INTO reviews(review, rating, created_at, updated_at, user_id, book_id) VALUES (:review, :rating, NOW(), NOW(), :user_id, :book_id)",
    #         'fetch_books_by_user_id': "SELECT * FROM books LEFT JOIN books_has_users ON books.id = books_has_users.user_id"
    #     }
    #
    def create_book(self, user_id, book_info):
        author_query = "SELECT * FROM authors WHERE name='{}'".format(book_info['author'])
        author = self.db.query_db(author_query)
        if not author:
            insert_author_query = "INSERT INTO authors (name, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(book_info['author'])
            self.db.query_db(insert_author_query)
        else:
            insert_author_query = "INSERT INTO authors (name, created_at, updated_at) VALUES ('{}', NOW(), NOW())".format(book_info['author'])
            self.db.query_db(insert_author_query)

        get_author_query = "SELECT * FROM authors ORDER BY id DESC LIMIT 1"
        author = self.db.query_db(get_author_query)

        insert_book_query = "INSERT INTO books (title, author_id, created_at, updated_at) VALUES ('{}', '{}', NOW(), NOW())".format(book_info['title'], author[0]['id'])
        self.db.query_db(insert_book_query)

        get_book_query = "SELECT * FROM books ORDER BY id DESC LIMIT 1"
        book = self.db.query_db(get_book_query)


        insert_review_query = "INSERT INTO reviews(review, rating, created_at, updated_at, user_id, book_id) VALUES ('{}', '{}', NOW(), NOW(), '{}', '{}')".format(book_info['review'], book_info['rating'], user_id, book[0]['id'])
        self.db.query_db(insert_review_query)
        return book[0]['id']

    def add_reviews(self, user_id, book_id, info):
        add_reviews_query = "INSERT INTO reviews (review, rating, created_at, updated_at, user_id, book_id) VALUES ('{}', '{}', NOW(), NOW(), '{}', '{}')".format(info['add_review'], info['rating'], user_id, book_id)
        self.db.query_db(add_reviews_query)

        book_id_query = "SELECT id FROM books WHERE id = {}".format(book_id)
        book_id = self.db.query_db(book_id_query)
        return book_id[0]['id']

    def recent_reviews(self):
        recent_reviews = "SELECT reviews.rating, reviews.review, users.name, users.id as user_id, reviews.created_at, books.title, books.id FROM reviews JOIN books ON reviews.book_id = books.id LEFT JOIN users ON users.id = reviews.user_id ORDER BY reviews.created_at DESC LIMIT 3"
        reviews = self.db.query_db(recent_reviews)
        return reviews

    def other_reviews(self):
        other_reviews_query = "SELECT books.title, books.id FROM reviews JOIN books ON reviews.book_id = books.id GROUP BY books.title ORDER BY reviews.created_at ASC"
        other_reviews = self.db.query_db(other_reviews_query)
        return other_reviews

    def total_reviews(self, user_id):
        total_reviews_query = "SELECT COUNT(*) AS total_reviews FROM reviews WHERE user_id = {}".format(user_id)
        total_reviews = self.db.query_db(total_reviews_query)
        return total_reviews[0]

    def review_titles(self, user_id):
        review_titles_query = "SELECT books.title, books.id FROM reviews JOIN books ON reviews.book_id = books.id WHERE user_id = {} GROUP BY books.title".format(user_id)
        review_titles = self.db.query_db(review_titles_query)
        return review_titles

    def book_info(self, id):
        book_info_query = "SELECT books.title, authors.name, books.id FROM books JOIN authors ON authors.id = books.author_id WHERE books.id = '{}'".format(id)
        book_info = self.db.query_db(book_info_query)
        return book_info[0]

    def get_reviews(self, id):
        get_reviews_query = "SELECT reviews.rating, reviews.review, users.name, reviews.created_at, users.id, reviews.id AS review_id FROM reviews JOIN books ON reviews.book_id = books.id LEFT JOIN users ON users.id = reviews.user_id WHERE books.id = '{}'".format(id)
        reviews = self.db.query_db(get_reviews_query)
        return reviews

    def destroy(self, review_id):
        book_id_query = "SELECT books.id FROM books  JOIN reviews ON reviews.book_id = books.id WHERE reviews.id = {}".format(review_id)
        book_id = self.db.query_db(book_id_query)
        print book_id
        delete_query = "DELETE FROM reviews WHERE id='{}'".format(review_id)
        delete = self.db.query_db(delete_query)
        return book_id[0]['id']
        # book_id_query = "SELECT books.id FROM books  JOIN reviews ON reviews.book_id = books.id WHERE reviews.id = {}".format(review_id)
        # book_id = self.db.query_db(book_id_query)
        # delete_query = "DELETE FROM reviews WHERE id='{}'".format(review_id)
        # delete = self.db.query_db(delete_query)
        # return book_id[0]['id']
    # # def create_review(self, form_data, user_id):
    # #     query = self.queries['create_review']
    # #     data = {
    # #         'user_id': user_id,
    # #         'title': form_data['title'],
    # #         'author': form_data['author'],
    # #         'review': form_data['review']
    # #     }
    # #     result = self.db.query_db(query, data)
    # #     return result
    # def create_book(self, user_id, form_data):
    #     book_query = self.queries['create_book']
    #     data = {
    #         'user_id': user_id,
    #         'title': form_data['title'],
    #     }
    #     result = self.db.query_db(book_query, data)
    #     return result
    # def create_author(self, author_id, form_data):
    #     author_query = self.queries['create_author']
    #     data = {
    #         'author_id': author_id,
    #         'author': form_data['author'],
    #     }
    #     result = self.db.query_db(author_query, data)
    #     return result
    # def create_review(self, user_id, form_data):
    #     review_query = self.queries['create_review']
    #     data = {
    #         'user_id': user_id,
    #         'review': form_data['review'],
    #         'rating': form_data['rating']
    #     }
    #     result = self.db.query_db(review_query, data)
    #     return result
    #
    #
    # def add_reviews(self, user_id, book_id, info):
    #     add_review = self.queries['insert_review']
    #     self.db.query_db(add_review)
    #
    #     book_id_query = self.queries['book_id']
    #     book_id = self.db.query_db(book_id_query)
    #     return book_id[0]['id']
