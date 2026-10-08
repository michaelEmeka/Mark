from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from entities.models import Department, Level, School, University
from users.models import User
from users.serializers import CreateUserSerializer, UpdateUserSerializer, UserDetailSerializer


class CreateUserSerializerTests(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            name="Test University",
            code="TU",
            address="123 Campus Road",
            city="Test City",
            state="Test State",
            zip_code="10001",
        )
        self.school = School.objects.create(
            name="School of Computing",
            code="SOC",
            address="1 School Lane",
            university=self.university,
        )
        self.department = Department.objects.create(
            name="Computer Science",
            code="CS",
            school=self.school,
        )
        self.level = Level.objects.create(code=100)
        Group.objects.get_or_create(name="Student")
        Group.objects.get_or_create(name="Lecturer")

    def test_create_user_serializer_hashes_password_and_sets_relationships(self):
        payload = {
            "email": "student@example.com",
            "username": "student01",
            "firstname": "Ada",
            "lastname": "Lovelace",
            "middlename": "Byron",
            "password": "StrongPass123!",
            "push_token": "device-token",
            "preferences": {"email": True, "push": False},
            "reg_number": "CS-2024-001",
            "university": self.university.id,
            "school": self.school.id,
            "department": self.department.id,
            "level": self.level.id,
        }

        serializer = CreateUserSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertEqual(user.university, self.university)
        self.assertEqual(user.school, self.school)
        self.assertEqual(user.department, self.department)
        self.assertEqual(user.level, self.level)


class ProfileUpdateSerializerTests(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            name="Profile University",
            code="PU",
            address="789 Campus Road",
            city="Profile City",
            state="PS",
            zip_code="30003",
        )
        self.school = School.objects.create(
            name="School of Health",
            code="SH",
            address="3 Health Lane",
            university=self.university,
        )
        self.department = Department.objects.create(
            name="Nursing",
            code="NUR",
            school=self.school,
        )
        self.level = Level.objects.create(code=300)
        self.set = self.department.sets.create(
            start_year=2024,
            end_year=2028,
            timetable=None,
        )
        self.user = User.objects.create_user(
            email="profile@example.com",
            password="StrongPass123!",
            firstname="Jane",
            lastname="Doe",
            reg_number="NUR-2024-011",
            department=self.department,
            level=self.level,
            university=self.university,
            school=self.school,
            set=self.set,
        )

    def test_update_user_serializer_accepts_partial_optional_fields(self):
        serializer = UpdateUserSerializer(
            instance=self.user,
            data={
                "username": "jane.doe",
                "middlename": "Mary",
                "push_token": "device-123",
                "preferences": {"theme": "dark"},
            },
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()

        self.assertEqual(updated.username, "jane.doe")
        self.assertEqual(updated.middlename, "Mary")
        self.assertEqual(updated.push_token, "device-123")
        self.assertEqual(updated.preferences, {"theme": "dark"})

    def test_user_detail_serializer_exposes_display_fields(self):
        payload = UserDetailSerializer(self.user).data

        self.assertEqual(payload["department_name"], "Nursing")
        self.assertEqual(payload["level_code"], 300)
        self.assertEqual(payload["school_name"], "School of Health")
        self.assertEqual(payload["university_name"], "Profile University")

    def test_update_user_serializer_accepts_department_matching_set(self):
        self.user.set = None
        self.user.save(update_fields=["set"])

        serializer = UpdateUserSerializer(
            instance=self.user,
            data={"set": self.set.id},
            partial=True,
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated = serializer.save()
        self.assertEqual(updated.set_id, self.set.id)

    def test_update_user_serializer_rejects_set_from_different_department(self):
        other_school = School.objects.create(
            name="School of Engineering",
            code="ENG",
            address="9 Engineering Lane",
            university=self.university,
        )
        other_department = Department.objects.create(
            name="Electrical Engineering",
            code="EE",
            school=other_school,
        )
        other_set = other_department.sets.create(
            start_year=2024,
            end_year=2028,
            timetable=None,
        )

        serializer = UpdateUserSerializer(
            instance=self.user,
            data={"set": other_set.id},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("set", serializer.errors)

    def test_update_user_serializer_rejects_changing_existing_set(self):
        replacement_set = self.department.sets.create(
            start_year=2025,
            end_year=2029,
            timetable=None,
        )

        serializer = UpdateUserSerializer(
            instance=self.user,
            data={"set": replacement_set.id},
            partial=True,
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("set", serializer.errors)


class LoginUserViewTests(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            name="Another University",
            code="AU",
            address="456 Campus Ave",
            city="Test City",
            state="Test State",
            zip_code="20002",
        )
        self.school = School.objects.create(
            name="School of Engineering",
            code="SOE",
            address="2 Engineering Road",
            university=self.university,
        )
        self.department = Department.objects.create(
            name="Software Engineering",
            code="SE",
            school=self.school,
        )
        self.level = Level.objects.create(code=200)
        self.student_group = Group.objects.get_or_create(name="Student")[0]

    def test_login_returns_tokens_for_valid_credentials(self):
        user = User.objects.create_user(
            email="engineer@example.com",
            password="StrongPass123!",
            firstname="Grace",
            lastname="Hopper",
            university=self.university,
            school=self.school,
            department=self.department,
            level=self.level,
            reg_number="SE-2024-010",
        )
        user.groups.add(self.student_group)

        response = self.client.post(
            reverse("login_user"),
            {"email": "engineer@example.com", "password": "StrongPass123!"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("access", payload)
        self.assertIn("refresh", payload)
