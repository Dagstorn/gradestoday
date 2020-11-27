from django.shortcuts import render, redirect
from .models import Teacher, Group, Student, Comment
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
# from .forms import CommentForm

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
            messages.error(request, 'Неверные данные')
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

        context = {
            'comments':comments,
            'teacher': teacher,
            'students':students
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
                messages.error(request, 'Логин недоступен. Попробуйте другой')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Пользователь с таким email адресом уже зарегестрирован!')
                return redirect('register')
            elif len(password1) < 7:
                messages.error(request, 'Пароль слишком короткий!')
                return redirect('register')
            elif password1 == firstname or password1 == lastname or password1 == username or password1 == 'password':
                messages.error(request, 'Пароль слишком простой!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=firstname, last_name=lastname)
                user.save()

                teacher = Teacher(name=firstname, lastname=lastname, phone=phone, subject=subject, user=user)
                teacher.save()
                messages.success(request, 'Пользователь создан успешно! Вы можете войти в аккаунт')
                return redirect('index')

        else:
            messages.error(request, 'Пароли не совпадают!')
            return redirect('register')           
        return redirect('index')
    else:
        context = {}
        return render(request, 'handler/register.html', context)

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
        positive = request.POST.get('positive')
        negative = request.POST.get('positive')
        user = request.user
        teacher = Teacher.objects.get(user=user)


        student = Student.objects.get(id=id)

        new_comment = Comment(title=title, positive=positive, negative=negative, student=student, teacher=teacher)
        new_comment.save()
        
        messages.success(request, 'Комментарий сохранен!')
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
            # 'form': CommentForm
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
