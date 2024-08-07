from django.test import TestCase
from .models import Employee, Position, Department, Status
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .serializers import EmployeeSerializer, PositionSerializer, DepartmentSerializer, StatusSerializer

class StatusModelTest(TestCase):

    def setUp(self):
        self.status = Status.objects.create(name="Active")

    def test_status_creation(self):
        self.assertEqual(self.status.name, "Active")

class DepartmentModelTest(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name="HR")

    def test_department_creation(self):
        self.assertEqual(self.department.name, "HR")

class PositionModelTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Manager", salary=60000)

    def test_position_creation(self):
        self.assertEqual(self.position.name, "Manager")
        self.assertEqual(self.position.salary, 60000)

class EmployeeModelTest(TestCase):

    def setUp(self):
        self.status = Status.objects.create(name="Active")
        self.department = Department.objects.create(name="HR")
        self.position = Position.objects.create(name="Manager", salary=60000)
        self.employee = Employee.objects.create(
            name="Armonrat Song",
            address="484/4 Moo6 Suranaree road",
            manager=True,
            status=self.status,
            department=self.department,
            position=self.position
        )

    def test_employee_creation(self):
        self.assertEqual(self.employee.name, "Armonrat Song")
        self.assertEqual(self.employee.address, "484/4 Moo6 Suranaree road")
        self.assertTrue(self.employee.manager)
        self.assertEqual(self.employee.status.name, "Active")
        self.assertEqual(self.employee.department.name, "HR")
        self.assertEqual(self.employee.position.name, "Manager")



class EmployeeAPITestCase(APITestCase):

    def setUp(self):
        self.status = Status.objects.create(name="Active")
        self.department = Department.objects.create(name="HR")
        self.position = Position.objects.create(name="Manager", salary=60000)
        self.employee = Employee.objects.create(
            name="Pongsakorn Dur",
            address="484/4 Moo6 Suranaree road",
            manager=True,
            status=self.status,
            department=self.department,
            position=self.position
        )
        self.employee_url = reverse('employee-detail', kwargs={'pk': self.employee.pk})
        self.employee_list_url = reverse('employee-list')

    def test_employee_list(self):
        response = self.client.get(self.employee_list_url)
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_employee_detail(self):
        response = self.client.get(self.employee_url)
        employee = Employee.objects.get(pk=self.employee.pk)
        serializer = EmployeeSerializer(employee)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_employee_create(self):
        data = {
            "name": "Armonrat S",
            "address": "484/4 Moo 6",
            "manager": False,
            "status": self.status.pk,
            "department": self.department.pk,
            "position": self.position.pk
        }
        response = self.client.post(self.employee_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)
        self.assertEqual(Employee.objects.last().name, "Armonrat S")

    def test_employee_update(self):
        data = {
            "name": "Pongsakorn Durongdumrongchai",
            "address": "484/4 Moo 6",
            "manager": True,
            "status": self.status.pk,
            "department": self.department.pk,
            "position": self.position.pk
        }
        response = self.client.put(self.employee_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, "Pongsakorn Durongdumrongchai")
        self.assertEqual(self.employee.address, "484/4 Moo 6")

    def test_employee_delete(self):
        response = self.client.delete(self.employee_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)
