from django.urls import path
from .views import (UsersListView,
		ProfileView,
		ToDoListView,
		ToDoCreateView,
		ToDoDeleteView,
		ToDoUpdateView,
		LoginView,
		AuthCallbackView,
		SignupView,)

urlpatterns = [
	path('login', LoginView.as_view(), name='open_login'),
	path('signup', SignupView.as_view(), name='signup'),
	path('profile', ProfileView.as_view(), name='profile'),
	path('oauth/callback', AuthCallbackView.as_view(), name='auth_callback'),
	# ToDO APIs
	path('list', ToDoListView.as_view(), name='all_todos'),
	path('create', ToDoCreateView.as_view(), name='add_todo'),
	path('<int:id>/update', ToDoUpdateView.as_view(), name='update_todo'),
	path('<int:id>/delete', ToDoDeleteView.as_view(), name='delete_todo'),
	path('users', UsersListView.as_view(), name='users_list'),
]
