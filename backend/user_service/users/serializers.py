from rest_framework import serializers
from .models import User

class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "user_name", "push_token", "preferences", "created_at"]

from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    #variables not in db but to be recognized by serializer

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "firstname",
            "lastname",
            "middlename",
            "password",
            "push_token",
            "preferences",
            "reg_number",
            "department",
            "level",
            "group",
        ]

    def validate(self, attrs):
        group = attrs.get("group")

        if group not in ["Admin", "Student", "Lecturer"]:
            raise serializers.ValidationError({
                "error": "Invalid group. Choose Admin, Student, or Lecturer."
            })

        preferences = attrs.get("preferences")

        if preferences is not None:

            if not isinstance(preferences, dict):
                raise serializers.ValidationError({
                    "error": "Preferences must be a dictionary."
                })

            if "email" not in preferences or "push" not in preferences:
                raise serializers.ValidationError({"error": "Preferences must include 'email' and 'push'."})

            if (not isinstance(preferences["email"], bool) or not isinstance(preferences["push"], bool)):
                raise serializers.ValidationError({"error": "'email' and 'push' must be boolean values."})
            
        return attrs

    def create(self, validated_data):
        group_name = validated_data.pop("group")
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            **validated_data
        )

        group = Group.objects.get(name=group_name)
        user.groups.add(group)

        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "firstname",
            "lastname",
            "middlename",
            "push_token",
            "preferences",
            "reg_number",
            "department",
            "level",
        ]