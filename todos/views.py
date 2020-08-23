from oauth2_provider.views.generic import ProtectedResourceView
from rest_framework.permissions import AllowAny, IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasScope
from rest_framework.views import APIView
from django.conf import settings
from django.urls import reverse_lazy
import pdb, requests, json
from django.http import JsonResponse
from .models import ToDos
from .serializers import ToDosSerializer, UserSerializer
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
import base64
from django.db.models import Q

class LoginView(APIView):
	permission_classes = (AllowAny,)
	def get(self, request, *args, **kwargs):
		#http://localhost:8000/oauth/authorize/?response_type=code&client_id=xzFisMHERT97LmmKQwloYePmd3bFc93Ctq8F4uDA&redirect_uri=http://localhost:8000/api/index
		redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse_lazy('auth_callback')}"
		authorize_url = f"{settings.AUTH_SERVER_BASE_URL}/oauth/authorize/?response_type=code&client_id={settings.AUTH_SERVER_CLIENT_ID}&redirect_uri={redirect_uri}"
		return HttpResponseRedirect(authorize_url)


class ProfileView(ProtectedResourceView):
	def get(self, request, *args, **kwargs):
		#request.resource_owner
		seri = UserSerializer(request.resource_owner)
		return JsonResponse({'message': 'Profile details.', 'code': 200, 'data': seri.data})


#Used to list all users to assigned in dropdown
class UsersListView(ProtectedResourceView):
	def get(self, request, *args, **kwargs):
		#request.resource_owner
		users = User.objects.filter(is_active=True).exclude(id=request.resource_owner.id)
		seri = UserSerializer(users, many=True)
		return JsonResponse({'message': 'Profile details.', 'code': 200, 'data': seri.data})

class ToDoListView(ProtectedResourceView):
	def get(self, request, *args, **kwargs):
		#request.resource_owner
		querysets = ToDos.objects.filter(Q(user=request.resource_owner)|Q(assigned_to=str(request.resource_owner.id))).distinct()
		seri = ToDosSerializer(querysets, many=True)
		return JsonResponse({'message': 'List of all todos.', 'code': 200, 'data': seri.data})


class ToDoCreateView(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request, *args, **kwargs):
		#request.user
		params = request.data
		params['user'] = request.user.id
		seri = ToDosSerializer(data=params)
		if seri.is_valid():
			seri.save()
			return JsonResponse({'message':'Task added', 'code': 200})
		error_message = " & ".join(["`%s` %s"%(error.title(), str(seri.errors.get(error)[0])) for error in seri.errors])
		return JsonResponse({'message': 'Failed to add task', 'code': 500, 'error_detail': error_message})

class ToDoUpdateView(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request, id):
		todos = ToDos.objects.filter(user=request.user, id=id)
		if not todos.exists():
			return JsonResponse({'message': 'No task found', 'code': 404})
		todo = todos.first()
		seri = ToDosSerializer(data=request.data, instance=todo, partial=True)
		if seri.is_valid():
			seri.save()
			return JsonResponse({'message':'Task updated', 'code': 200})
		return JsonResponse({'message': 'Failed to update task', 'code': 500})


class ToDoDeleteView(ProtectedResourceView):
	def get(self, request, id):
		todos = ToDos.objects.filter(id=id, )
		if todos.exists():
			todos.delete()
			return JsonResponse({'message':'Task deleted', 'code': 200})
		return JsonResponse({'message': 'No task found', 'code': 404})

class SignupView(APIView):
	permission_classes = (AllowAny,)
	def post(self, request, *args, **kwargs):
		code = request.GET.get('code', False)
		payload = request.data
		session = requests.Session()
		session = requests.post(f"{settings.AUTH_SERVER_BASE_URL}/users/signup",data=payload)
		if session.status_code == 200:
			return JsonResponse(session.json())
		else:
			return JsonResponse({'error': str(session.text)})

class AuthCallbackView(APIView):
	permission_classes = (AllowAny,)
	def get(self, request, *args, **kwargs):
		code = request.GET.get('code', False)
		if code:
			redirect_uri = f"{request.scheme}://{request.META['HTTP_HOST']}{reverse_lazy('auth_callback')}"
			payload = {
				"grant_type": "authorization_code",
				"code": code,
				"redirect_uri": redirect_uri,
				"client_id": settings.AUTH_SERVER_CLIENT_ID
			}
			session = requests.Session()
			session = requests.post(f"{settings.AUTH_SERVER_BASE_URL}/oauth/token/",data=payload)
			if session.status_code == 200:
				auth_detail = json.dumps(session.json())
				base64_data = base64.urlsafe_b64encode(auth_detail.encode()).decode("utf-8")
				return HttpResponseRedirect(f"{settings.CLIENT_SERVER}?secData={base64_data}")
			else:
				return JsonResponse({'error': str(session.text)})
		else:
			return JsonResponse({'error': "Some Error"})


