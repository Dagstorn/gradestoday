from django.db import models
from django.contrib.auth.models import User, auth
import string
import random

class Teacher(models.Model):
    name = models.CharField('Teacher name', max_length=120)
    lastname = models.CharField('Last name', max_length=120)
    phone = models.CharField('Phone number', max_length=120)
    subject = models.CharField('Subject', max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User account')
    status = models.BooleanField('Status', default=False)

    def __str__(self):
        return self.name + " " + self.lastname

class Group(models.Model):
    name = models.CharField('Group name', max_length=120)

    def __str__(self):
        return self.name
    
    def getStudents(self):
        students = Student.objects.filter(group = self)
        return students
    

class Student(models.Model):
    name = models.CharField('Student name', max_length=120)
    lastname = models.CharField('Student last name', max_length=120)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Group')
    unique_code = models.CharField('Student code', max_length=11, default='1')

    def __str__(self):
        return self.name
    
    def getCommentsCount(self):
        return len(Comment.objects.filter(student=self))

    def save(self, *args, **kwargs):
        id = self.id
        digits = '123456789'
        code = str(random.choice(digits)) + str(random.choice(digits)) + str(random.choice(string.ascii_letters)) + str(random.choice(digits)) + str(random.choice(string.ascii_letters))
        self.unique_code = code

        super(Student, self).save(*args, **kwargs)


class Comment(models.Model):
    title =  models.CharField('Title', max_length=200)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date and time')
    comment = models.TextField('Comment')
    results = models.TextField('Results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def getTeacherName(self):
        return self.teacher.name + " " + self.teacher.lastname

    def getTeacherPhone(self):
        return self.teacher.phone

    def getTeachersubject(self):
        return self.teacher.subject
    