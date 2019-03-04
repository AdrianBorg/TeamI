from django.shortcuts import render
from trimit.forms import UserRegisterForm, UserProfileForm, HairdresserPageForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/base.html', context=context_dict)


def about(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/base.html', context=context_dict)


def contact_us(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/base.html', context=context_dict)


def popupTest(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/popup.html', context_dict)


def ajax_user_login(request):
    context_dict = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return JsonResponse({'login': True})
            else:
                context_dict['error'] = "Account is inactive."
                return JsonResponse({'login': False,
                                     'error': context_dict['error']})

        else:
            context_dict['error'] = "Username and password credentials do not match."
            print("Invalid login details: {0}, {1}".format(username, password))
            return JsonResponse({'login': False,
                                 'error': context_dict['error']})

    else:
        context_dict['action'] = 'login'
        return render(request, 'rango/index.html', context_dict)


def hairdresser_register(request):
    registered = False
    context_dict = {}
    profile_form = UserProfileForm()
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        hair_form = HairdresserPageForm(data=request.POST)

        if request.POST.get('redir') != '':
            context_dict['redir'] = request.POST.get('redir')
            context_dict['redir_name'] = resolve(context_dict['redir']).url_name

        if user_form.is_valid() and hair_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = hair_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, hair_form.errors)

    else:
        user_form = UserRegisterForm()
        hair_form = HairdresserPageForm()

    context_dict.update({'user_form': user_form,
                         'profile_form': profile_form,
                         'hair_form': hair_form,
                         'registered': registered})

    return render(request,
                  'trimit/hairdresser_register.html',
                  context_dict)


def user_register(request):
    registered = False
    context_dict = {}
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if request.POST.get('redir') != '':
            context_dict['redir'] = request.POST.get('redir')
            context_dict['redir_name'] = resolve(context_dict['redir']).url_name

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
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()

    context_dict.update({'user_form': user_form,
                         'profile_form': profile_form,
                         'registered': registered})

    return render(request,
                  'trimit/user_register.html',
                  context_dict)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
