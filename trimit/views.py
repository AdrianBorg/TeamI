from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'trimit/base.html', context=context_dict)


def hairdresserpage(request):
    return render(request, 'trimit/hairdresserpage.html')
