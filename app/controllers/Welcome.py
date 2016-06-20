from system.core.controller import *

class Welcome(Controller):
    def __init__(self, action):
        super(Welcome, self).__init__(action)

    #
    # def index(self):
    #     return self.load_view('index.html')

    def display_login_reg(self):
        # Flash errors
        if 'val_errors' in session:
            for error in session['val_errors']:
                flash (error)
            #clear val erorrs on a page refresh
            session.pop('val_errors')
        return self.load_view('loginreg.html')
