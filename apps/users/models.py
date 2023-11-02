from django.contrib.auth.models import AbstractUser
from django.db import models

# Modelo de Usuario
class User(AbstractUser):
    
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    
    # Proceso para poder loguearse con el email y no con el username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'TASKER_user'
        managed = True
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['id']
    
    def __str__(self):
        return f'{self.username} - {self.email}'