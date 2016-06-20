
from system.core.router import routes

routes['GET']['/'] = 'Welcome#display_login_reg'

routes['POST']['/user'] = 'Users#create'
routes['POST']['/user/login'] = 'Users#login'
routes['GET']['/user'] = 'Users#home'
routes['GET']['/users/<int:id>'] = 'Users#show'
routes['GET']['/user/logout'] = 'Users#logout'

routes['GET']['/books/new'] = 'Books#add'
routes['POST']['/books/create'] = 'Books#create'
routes['GET']['/books/<int:id>'] = 'Books#show'
routes['POST']['/books/<int:id>/update'] = 'Books#update'
routes['POST']['/books/<int:id>/delete'] = 'Books#destroy'

routes['POST']['/register'] = 'Users#register'
