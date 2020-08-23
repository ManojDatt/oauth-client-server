from django.db import models
from django.contrib.auth.models import User
class ToDos(models.Model):
	PRIORITY = (
		('HIGH', 'HIGH'),
		('MEDIUM', 'MEDIUM'),
		('MODERATE', 'MODERATE'),)

	class Meta:
		verbose_name = "Todos"
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	task_name = models.CharField(max_length=255)
	details = models.TextField()
	priority = models.CharField(max_length=20, choices=PRIORITY)
	complete = models.BooleanField(default=False)
	assigned_to = models.ManyToManyField(User, blank=True, related_name='assigned_users')
	created_at = models.DateTimeField(auto_now=True)
	updated_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.task_name