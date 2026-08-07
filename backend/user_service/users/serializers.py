from rest_framework import serializers
from .models import User

class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "user_name", "push_token", "preferences", "created_at", "updated_at"]