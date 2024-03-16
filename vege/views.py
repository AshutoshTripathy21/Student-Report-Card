from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum

from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.

@login_required(login_url='/login/')
def receipies(request):
    if request.method == "POST":
        data = request.POST
        r_name = data.get('name')
        r_description = data.get('description')
        r_image = request.FILES.get('image')
        
        Receipe.objects.create(
            name = r_name,
            description = r_description,
            image=r_image
        )
        return redirect('/receipies/')
    
    queryset = Receipe.objects.all()
    if request.GET.get('search'):
        #print(request.GET.get('search'))
        queryset = queryset.filter(name__icontains = request.GET.get('search'))
        
    context={'receipies':queryset}
    return render(request, 'receipies.html', context)


def delete_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipies/')


def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        description = data.get('description')
        image = request.FILES.get('image')

        queryset.name = name
        queryset.description = description
        if image:
            queryset.image = image
        
        queryset.save()
        return redirect('/receipies/')
    context = {'receipe': queryset}
    return render(request, 'update_receipe.html', context)

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username)

        if user.exists():
            messages.info(request,"Username already exists.")
            return redirect('/register/')

        user = User.objects.create(
            first_name=first_name,
            last_name = last_name,
            username = username
        )
        user.set_password(password)
        user.save()
        messages.success(request, "Account created successfully.")
        return redirect('/register/')
    return render(request, 'register.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid username')
            return redirect('/login/')
        
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Invalid credentials')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/receipies/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def get_students(request):
    students = Student.objects.all()
    ranks = Student.objects.annotate(marks = Sum('studentname__marks')).order_by('-marks')
    print(ranks)
    if request.GET.get('search'):
        search = request.GET.get('search')
        students = students.filter(
            Q(student_name__icontains = search) | 
            Q(department__department__icontains = search),
        )
    paginator = Paginator(students, 20)  # Show 25 contacts per page.

    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'report/student.html', {'students': page_obj})

from .seed import generate_report_card
def see_marks(request, student_id):
    #generate_report_card()
    queryset = SubjectMarks.objects.filter(student__student_id__student_id = student_id)
    total_marks = queryset.aggregate(total_marks = Sum('marks'))
    
    return render(request, 'report/see_marks.html', {'queryset': queryset, 'total_marks': total_marks})