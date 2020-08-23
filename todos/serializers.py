from rest_framework.serializers import ModelSerializer, DateTimeField, SerializerMethodField
from .models import ToDos
from django.contrib.auth.models import User
from datetime import datetime

class ToDosSerializer(ModelSerializer):
	username = SerializerMethodField(read_only=True)
	created_at = DateTimeField(format="%d/%m/%Y %I:%M %p", required=False, default=datetime.now())
	class Meta:
		model = ToDos
		fields = '__all__'

	def get_username(self, obj):
		return obj.user.username

class UserSerializer(ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'username', 'last_login', 'date_joined', 'is_active',)