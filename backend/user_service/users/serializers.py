from rest_framework import serializers
from .models import User
from entities.models import Department

class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "push_token", "preferences", "created_at"]

from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    department = serializers.CharField()
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
        #these are serializer fields first then db fields(for those not in serializer)
        #thus the data type validation order is serializer first then database

    def validate(self, attrs):
        ##type checking

        #group validator
        group = attrs.get("group")
        preferences = attrs.get("preferences")
        department = attrs.get("department")

        if group not in ["Student", "Lecturer"]:
            raise serializers.ValidationError({
                "error": "Invalid group. Choose Student, or Lecturer."
            })
        
        #preferences validator
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
        department_name = validated_data.pop("department")

        try:
            department = Department.objects.get(name=department_name)
        except Department.DoesNotExist:
            raise serializers.ValidationError({
                "department": f"Department '{department_name}' does not exist."
            })

        user = User.objects.create(
            password=password, department=department, **validated_data
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

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "firstname",
            "lastname",
            "middlename",
        ]
    def validate(self, attrs):
        return attrs
    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance