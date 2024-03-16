from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    peoples = [
        {'name': 'Ashutosh', 'age': 22},
        {'name': 'Tanushree', 'age': 17},
        {'name': 'Lucky', 'age': 24},
        {'name': 'Tisha', 'age': 23},
        {'name': 'Ashu', 'age': 15},
        {'name': 'Tishu', 'age': 27}
    ]

    text = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Quo, quos nesciunt asperiores quod animi reprehenderit illo dicta recusandae eligendi laborum, placeat, consequatur numquam dolore assumenda repudiandae! Iste quos quia eum.'
    #if user.is_authenticated
    return render(request, "index.html", context= {'page': 'Django Home', 'peoples': peoples, 'text': text})

def about_us(request):
    return HttpResponse("It is another page response :)")

def about(request):
    context = {'page': 'About'}
    return render(request, 'about.html', context)

def contact(request):
    context = {'page': 'Contact'}
    return render(request, 'contact.html', context)