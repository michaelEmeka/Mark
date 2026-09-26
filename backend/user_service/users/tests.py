from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from entities.models import Department, Level, School, University
from users.models import User
from users.serializers import CreateUserSerializer


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
            "department": self.department.name,
            "level": self.level.id,
            "group": "Student",
        }

        serializer = CreateUserSerializer(data=payload)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        user = serializer.save()

        self.assertTrue(user.check_password("StrongPass123!"))
        self.assertEqual(user.department, self.department)
        self.assertEqual(user.level, self.level)
        self.assertTrue(user.groups.filter(name="Student").exists())


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
