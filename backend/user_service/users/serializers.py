from rest_framework import serializers

from entities.models import Department, Level, School, Set, University

from .models import User


class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "push_token", "preferences", "created_at"]

from rest_framework import serializers

from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    university = serializers.PrimaryKeyRelatedField(queryset=University.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    level = serializers.PrimaryKeyRelatedField(queryset=Level.objects.all())

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
            "university",
            "school",
            "department",
            "level",
        ]

    def validate(self, attrs):
        university = attrs.get("university")
        school = attrs.get("school")
        department = attrs.get("department")

        if school and university and school.university_id != university.id:
            raise serializers.ValidationError({"school": "School does not belong to the selected university."})

        if department and school and department.school_id != school.id:
            raise serializers.ValidationError({"department": "Department does not belong to the selected school."})

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField()
    school_name = serializers.SerializerMethodField()
    university_name = serializers.SerializerMethodField()
    level_code = serializers.SerializerMethodField()
    set_id = serializers.SerializerMethodField()
    set_years = serializers.SerializerMethodField()

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
            "department_name",
            "school",
            "school_name",
            "university",
            "university_name",
            "level",
            "level_code",
            "set_id",
            "set_years",
        ]

    def get_department_name(self, obj):
        return obj.department.name if obj.department else None

    def get_school_name(self, obj):
        return obj.school.name if obj.school else None

    def get_university_name(self, obj):
        return obj.university.name if obj.university else None

    def get_level_code(self, obj):
        return obj.level.code if obj.level else None

    def get_set_id(self, obj):
        from entities.models import Set

        current_set = obj.set
        if current_set and (
            current_set.department_id != obj.department_id
            or current_set.department.school_id != obj.school_id
            or current_set.department.school.university_id != obj.university_id
        ):
            current_set = None

        if current_set is None:
            current_set = (
                Set.objects.filter(
                    department__school__university_id=obj.university_id,
                    department__school_id=obj.school_id,
                    department_id=obj.department_id,
                )
                .order_by("-start_year", "-end_year")
                .first()
            )

        return current_set.id if current_set else None

    def get_set_years(self, obj):
        set_id = self.get_set_id(obj)
        if not set_id:
            return None

        from entities.models import Set

        current_set = Set.objects.filter(id=set_id).first()
        if not current_set:
            return None

        return {
            "start_year": current_set.start_year,
            "end_year": current_set.end_year,
        }


class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, allow_blank=True)
    middlename = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    push_token = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    preferences = serializers.JSONField(required=False, allow_null=True)
    set = serializers.PrimaryKeyRelatedField(queryset=Set.objects.all(), required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "username",
            "middlename",
            "push_token",
            "preferences",
            "set",
        ]

    def validate(self, attrs):
        selected_set = attrs.get("set")
        instance = getattr(self, "instance", None)

        if instance is not None and instance.set_id is not None:
            if "set" in attrs:
                if selected_set is None:
                    raise serializers.ValidationError({"set": "Set is fixed once assigned and cannot be cleared."})
                if selected_set.id != instance.set_id:
                    raise serializers.ValidationError({"set": "Set cannot be changed after it has been assigned."})
            return attrs

        if selected_set is None:
            return attrs

        if instance is not None:
            if selected_set.department_id != instance.department_id:
                raise serializers.ValidationError({"set": "Set does not belong to the selected department."})
            if selected_set.department.school_id != instance.school_id:
                raise serializers.ValidationError({"set": "Set does not belong to the selected school."})
            if selected_set.department.school.university_id != instance.university_id:
                raise serializers.ValidationError({"set": "Set does not belong to the selected university."})

        return attrs

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if field == "set":
                if instance.set_id is None:
                    instance.set = value
                continue
            setattr(instance, field, value)

        if instance.set_id is None:
            matching_set = (
                Set.objects.filter(
                    department__school__university_id=instance.university_id,
                    department__school_id=instance.school_id,
                    department_id=instance.department_id,
                )
                .order_by("-start_year", "-end_year")
                .first()
            )
            instance.set = matching_set

        instance.save()
        return instance