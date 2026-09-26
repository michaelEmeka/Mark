from django.db import IntegrityError
from django.test import TestCase

from entities.models import Department, Level, School, Set, University


class EntityConstraintTests(TestCase):
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

    def test_unique_set_per_department_constraint(self):
        Set.objects.create(
            department=self.department,
            start_year=2024,
            end_year=2027,
        )

        with self.assertRaises(IntegrityError):
            Set.objects.create(
                department=self.department,
                start_year=2024,
                end_year=2027,
            )
