from datetime import date, time

from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIClient

from attendance.models import Attendance
from entities.models import (
    Course,
    Department,
    Hall,
    Level,
    School,
    Semester,
    Session,
    Set,
    Timetable,
    TimetableEntry,
    TimetableEntrySchedule,
    University,
)
from users.models import User


class AttendanceModelTests(TestCase):
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
        self.session = Session.objects.create(start_year=2024, end_year=2025)
        self.semester = Semester.objects.create(
            name="Harmattan",
            session=self.session,
            start_date=date(2024, 9, 1),
            end_date=date(2024, 12, 20),
        )
        self.timetable = Timetable.objects.create(
            department=self.department,
            level=self.level,
            semester=self.semester,
        )
        self.course = Course.objects.create(name="Algorithms", code="CS101", units=3)
        self.course.department.add(self.department)
        self.course.level.add(self.level)
        self.hall = Hall.objects.create(
            name="CST Hall",
            capacity=120,
            university=self.university,
            school=self.school,
            department=self.department,
        )
        self.lecturer_group = Group.objects.get_or_create(name="Lecturer")[0]
        self.student_group = Group.objects.get_or_create(name="Student")[0]
        self.lecturer = User.objects.create_user(
            email="lecturer@example.com",
            password="StrongPass123!",
            firstname="Ada",
            lastname="Lovelace",
            department=self.department,
            level=self.level,
        )
        self.lecturer.groups.add(self.lecturer_group)
        self.student = User.objects.create_user(
            email="student@example.com",
            password="StrongPass123!",
            firstname="Grace",
            lastname="Hopper",
            department=self.department,
            level=self.level,
            reg_number="CS-2024-001",
        )
        self.student.groups.add(self.student_group)
        self.timetable_entry = TimetableEntry.objects.create(
            course=self.course,
            day="MON",
            start_time=time(9, 0),
            end_time=time(10, 0),
            timetable=self.timetable,
        )
        self.schedule = TimetableEntrySchedule.objects.create(
            timetable_entry=self.timetable_entry,
            date=date(2024, 9, 2),
            lecturer=self.lecturer,
            hall=self.hall,
        )

    def test_mark_attendance_marks_present_when_time_falls_within_class_window(self):
        attendance = Attendance.objects.create(
            user=self.student,
            timetable_entry_schedule=self.schedule,
            time_in=time(9, 30),
            is_present=False,
        )

        self.assertTrue(attendance.mark_attendance())
        attendance.refresh_from_db()
        self.assertTrue(attendance.is_present)

    def test_list_user_attendance_returns_user_records(self):
        Attendance.objects.create(
            user=self.student,
            timetable_entry_schedule=self.schedule,
            time_in=time(9, 15),
            is_present=True,
        )

        client = APIClient()
        client.force_authenticate(user=self.student)
        response = client.get("/attendance/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["course"]["code"], "CS101")
        self.assertTrue(response.data[0]["is_present"])
