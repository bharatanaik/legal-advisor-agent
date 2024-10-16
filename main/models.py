# import uuid
# from django.db import models
# from django.contrib.auth.models import User

# # Create your models here.
# class Conversation(models.Model):
#    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)

#    def __str__(self):
#         return f"{self.user}:{self.uuid}"

# class ChatMessage(models.Model):
#     conversation = models.ForeignKey(Conversation, default=None, on_delete=models.CASCADE)
#     user_response = models.TextField(null=True, default='')
#     ai_response = models.TextField(null=True, default='')
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.conversation}"