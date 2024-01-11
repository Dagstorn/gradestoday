from django.shortcuts import render, redirect
from .models import Teacher, Group, Student, Comment
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required

def index(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        username = request.POST.get('username')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            try:
                teacher = Teacher.objects.get(user=user)
            except:
                teacher = None

            if teacher:
                if teacher.status == True:
                    return redirect("start")
                else:
                    return redirect("index")
            else:
                return redirect("index")
        else:
            messages.error(request, 'Wrong credentials')
            return redirect("index")
    else:
        comments = Comment.objects.all()
        if request.user.is_authenticated:
            try:
                teacher = Teacher.objects.get(user=request.user)
            except:
                teacher = None
        else: 
            teacher = None
        students = Student.objects.all()
        teacherStatus = None

        if teacher:
            teacherStatus = teacher.status

        context = {
            'comments':comments,
            'teacher': teacher,
            'students':students,
            'teacherStatus': teacherStatus
        }
        return render(request, 'handler/index.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered!')
                return redirect('register')
            elif len(password1) < 7:
                messages.error(request, 'Password is too short!')
                return redirect('register')
            elif password1 == firstname or password1 == lastname or password1 == username or password1 == 'password':
                messages.error(request, 'Password is too simple!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=firstname, last_name=lastname)
                user.save()

                teacher = Teacher(name=firstname, lastname=lastname, phone=phone, subject=subject, user=user)
                teacher.save()
                messages.success(request, 'The account was created successfully! You can log in to your account')
                return redirect('index')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')    
    else:
        return render(request, 'handler/register.html', {})

#function logout
def logout(request):
    auth.logout(request)
    return redirect('/')

def teacher_start(request):
    if request.user.is_authenticated:
        try:
            teacher = Teacher.objects.get(user=request.user)
        except:
            teacher = None
    else: 
        teacher = None
        return redirect("index")


    groups = Group.objects.all()

    if teacher:
        if teacher.status == False:
            auth.logout(request)
            return redirect("index")
    else:
        auth.logout(request)
        return redirect("index")

    context = {
        'teacher':teacher,
        'groups':groups,

    }
    return render(request, 'handler/start_teacher.html', context)


def create_comment(request, id):
    if request.method == 'POST':
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        results = request.POST.get('results')
        user = request.user
        teacher = Teacher.objects.get(user=user)


        student = Student.objects.get(id=id)

        new_comment = Comment(title=title, comment=comment, results=results, student=student, teacher=teacher)
        new_comment.save()
        
        messages.success(request, 'Comment is saved!')
        return redirect('start')
    else:
        if request.user.is_authenticated:
            try:
                teacher = Teacher.objects.get(user=request.user)
            except:
                teacher = None
        else: 
            teacher = None
            return redirect("index")
        if teacher:
            if teacher.status != True:
                return redirect("index")
        else:
            return redirect("index")

        context = {
        }
        return render(request, 'handler/comment.html', context)


def student_comments(request):
    if request.method == "GET":
        code = request.GET.get('code')
        try:
            student = Student.objects.get(unique_code=code)
        except:
            student = None

        comments = Comment.objects.filter(student = student).order_by('-date')
        if request.user.is_authenticated:
            try:
                teacher = Teacher.objects.get(user=request.user)
            except:
                teacher = None
        else: 
            teacher = None

        context = {
            'comments':comments,
            'student':student,
            'teacher':teacher
        }
        return render(request, 'handler/student_comments.html', context)
    else:
        return redirect('index')
