from django.db import models
from django.contrib.auth.models import User, auth
import string
import random

class Teacher(models.Model):
    name = models.CharField('Имя учителя', max_length=120)
    lastname = models.CharField('Фамилия учителя', max_length=120)
    phone = models.CharField('Номер учителя', max_length=120)
    subject = models.CharField('Предмет', max_length=120)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Аккаунт пользователя на сайте')
    status = models.BooleanField('Статус', default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Учителя"
        verbose_name_plural = "Учителя"


class Group(models.Model):
    name = models.CharField('Имя группы', max_length=120)

    def __str__(self):
        return self.name
    
    def getStudents(self):
        students = Student.objects.filter(group = self)
        return students
    
    class Meta:
        verbose_name = "Группу"
        verbose_name_plural = "Группы"

class Student(models.Model):
    name = models.CharField('Имя ученика', max_length=120)
    lastname = models.CharField('Фамилия ученика', max_length=120)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, verbose_name='Группа')
    unique_code = models.CharField('Код студента', max_length=11, default='1')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Ученика"
        verbose_name_plural = "Ученики"
    
    def getCommentsCount(self):
        return len(Comment.objects.filter(student=self))

    def save(self, *args, **kwargs):
        id = self.id
        digits = '123456789'
        code = str(random.choice(digits)) + str(random.choice(digits)) + str(random.choice(string.ascii_letters)) + str(random.choice(digits)) + str(random.choice(string.ascii_letters))
        self.unique_code = code

        super(Student, self).save(*args, **kwargs)


class Comment(models.Model):
    title =  models.CharField('Заголовок', max_length=200)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время')
    comment = models.TextField('Комментарий')
    results = models.TextField('Результаты')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Ученик')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='Учитель')


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
    
    def getTeacherName(self):
        return self.teacher.name + " " + self.teacher.lastname

    def getTeacherPhone(self):
        return self.teacher.phone

    def getTeachersubject(self):
        return self.teacher.subject
    