from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name = 'logout'),

    path('start/', views.teacher_start, name = 'start'),
    path('start/<int:id>/comment/', views.create_comment, name = 'create_comment'),

    path('student/comments/', views.student_comments, name = 'student_comments'),

]