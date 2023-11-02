# Generated by Django 4.2.3 on 2023-11-02 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Titulo')),
                ('description', models.CharField(max_length=250, verbose_name='Descripcion')),
                ('completed', models.BooleanField(default=False, verbose_name='Completado')),
                ('date_to_finish', models.DateField(blank=True, null=True, verbose_name='Fecha de finalizacion')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualizacion')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('status', models.BooleanField(default=True, verbose_name='Estatus')),
            ],
            options={
                'verbose_name': 'Tarea',
                'verbose_name_plural': 'Tareas',
                'db_table': 'TASKER_task',
                'ordering': ['id'],
                'managed': True,
            },
        ),
    ]