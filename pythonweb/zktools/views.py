from django.shortcuts import render
from django.shortcuts import HttpResponse
# Create your views here.
user_list = [
    {'user': 'abc', 'pwd': '123'}
]


def index(request):
    # return HttpResponse('Hello world')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        temp = {'user': username, 'pwd': password}
        user_list.append(temp)
    return render(request, 'index.html', {'data': user_list})
