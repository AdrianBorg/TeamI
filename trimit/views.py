from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'manes/testhtml.html', context=context_dict)

def results(request):
    return render(request, 'manes/results.html')
