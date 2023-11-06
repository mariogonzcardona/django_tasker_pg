from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.tasks.models import Task
from apps.users.models import User

class TaskViewSetTestCase(TestCase):
    def setUp(self):
        
        self.user = User.objects.create(
            username="TestUser",
            email="Test@test.com",
            first_name="Test",
            last_name="User",
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        
        self.task = Task.objects.create(
            title="Test Task",
            description="Test Description",
            completed=False,
            date_to_finish="2023-01-01",
            user=self.user
        )
        
    
    def test_create_task(self):
        # Asumiendo que tienes un campo 'title', 'description' y 'date_to_finish' en tu modelo Task
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'date_to_finish': '2023-01-01'
        }
        response = self.client.post('/api/v1/tasks/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
    
    def test_update_task(self):
        # Obtener el id de la tarea creada en setUp
        task_id = self.task.id
        data = {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'date_to_finish': '2023-01-01',
            'completed': True
        }
        response = self.client.put(f'/api/v1/tasks/{task_id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)
    
    def test_delete_task(self):
        # Obtener el id de la tarea creada en setUp
        task_id = self.task.id
        response = self.client.delete(f'/api/v1/tasks/{task_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertFalse(self.task.status)  # Asumiendo que el campo status indica si la tarea está activa
    
    def test_list_tasks(self):
        response = self.client.get('/api/v1/tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.task.title, response.data)