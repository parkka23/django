from tabnanny import verbose
from django.db import models

# Create your models here.
# Языковая школа 

class Teacher(models.Model):
    name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    number=models.CharField(max_length=30)
    language=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.last_name}'
    
class Student(models.Model):
    name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.name} {self.last_name}'
    
class Group(models.Model):
    title=models.CharField(max_length=30)
    # set null - усли удалить, установится null
    # null=True  можно не заполнять
    # blank=True
    teacher_id=models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.title}'

# many to  many
class GroupStudents(models.Model):
    # удалить студента - удаляется и связь
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    group_id=models.ForeignKey(Group,on_delete=models.CASCADE)

    class Meta:
        verbose_name='Group student'
        verbose_name_plural='Group students'

    def __str__(self):
        return f'{self.student_id} {self.group_id}'
    

