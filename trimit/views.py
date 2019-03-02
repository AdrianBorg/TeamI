from django.shortcuts import render
from trimit.forms import EUserForm, UserProfileForm
from django.urls import reverse, resolve
from django.http import HttpResponse, JsonResponse

# Create your views here.


def index(request):
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(request, 'trimit/base.html', context=context_dict)


def popupTest(request):
    user_form = EUserForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/popup.html', context_dict)


def user_register(request):
    registered = False
    context_dict = {}
    if request.method == 'POST':
        user_form = EUserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if request.POST.get('redir') != '':
            context_dict['redir'] = request.POST.get('redir')
            context_dict['redir_name'] = resolve(context_dict['redir']).url_name
        print(context_dict)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = EUserForm()
        profile_form = UserProfileForm()

    context_dict.update({'user_form': user_form,
                         'profile_form': profile_form,
                         'registered': registered})
    # if context_dict['next'] and registered:
    #     print(context_dict)
    #     return render(request,
    #                   'trimit/' + resolve(context_dict['next']).url_name + '.html',
    #                   context_dict)
    # else:
    return render(request,
                  'trimit/user_register.html',
                  context_dict)
