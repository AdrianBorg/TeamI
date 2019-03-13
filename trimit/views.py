from django.shortcuts import render
from trimit.forms import UserRegisterForm, UserProfileForm, HairdresserPageForm, HairPageSpecialityForm
from trimit.models import Page, UserProfile, Specialities, Review
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.safestring import mark_safe
import json
from django.db.models import Avg
import tagulous.forms


# Create your views here.


def index(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/base.html', context=context_dict)


@login_required()
def user_profile(request):

    user_form = UserRegisterForm()

    profile_form = UserProfileForm()

    profile = UserProfile.objects.filter(user=request.user)[0]
    # sends information for reviews
    reviews = Review.objects.filter(user=profile)
    # sends information of a users favourite hairdressers
    hairdressers = profile.favourites.all()
    print(hairdressers[0].profile_picture)


    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'reviews': reviews,
                    'user_profile': profile,
                    'hairdressers': hairdressers,
                    }
    return render(request, 'trimit/user_profile.html', context_dict)

def results(request):
    q = request.GET.get('q')
    print(q)
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }

    resultset = Page.objects.filter(city__iexact=q)

    context_dict['search_location'] = q
    context_dict['number_of_results'] = resultset.count()
    context_dict['resultset'] = mark_safe(serializers.serialize('json', resultset))
    context_dict['speciality_field_form'] = HairPageSpecialityForm
    print(HairPageSpecialityForm)

    return render(request, 'trimit/results.html', context_dict)


def ajax_search_filter(request):
    if request.method == 'POST':
        favourites = None
        #Commented for testing ##################################
        # types = request.POST.get('types')
        # value = request.POST.get('value')
        # rating = request.POST.get('rating')
        # service = request.POST.get('service')
        # atmosphere = request.POST.get('atmosphere')
        lat_bounds = [request.POST.get('latMin'), request.POST.get('latMax')]
        lng_bounds = [request.POST.get('lngMin'), request.POST.get('lngMax')]
        # city = request.POST.get('city')
        #
        specialities = json.loads(request.POST.get('specialityTags'))
        # print(type(specialities))
        map_filtered_results = Page.objects.filter(latitude__gte=lat_bounds[0],
                                                   latitude__lte=lat_bounds[1],
                                                   longitude__gte=lng_bounds[0],
                                                   longitude__lte=lng_bounds[1])
        #
        # annotated_results = map_filtered_results.reviews.annotate(avgv=Avg('price_rating'),
        #                                                           avgr=Avg('overall_rating'),
        #                                                           avgs=Avg('service_rating'),
        #                                                           avga=Avg('atmosphere_rating'))
        #
        # rating_filtered_results = annotated_results.filter(avgv__gte=value,
        #                                                    avgr__gte=rating,
        #                                                    avgs__gte=service,
        #                                                    avga__gte=atmosphere)

        rating_filtered_results = map_filtered_results#.filter(city__iexact=city)
        resultset = mark_safe(serializers.serialize('json', rating_filtered_results))

        if not request.user.is_anonymous():
            user = request.user
            # print(UserProfile.objects.filter(user=user).first().favourites.all())
            favourites = UserProfile.objects.filter(user=user).first().favourites.all()
            # print(favourites, "111")
            favourite_usernames = [fav.user.pk for fav in favourites]
            # print(favourite_usernames, "222")
            favourites_json = str(favourite_usernames) #serializers.serialize('json', favourite_usernames)

            return JsonResponse({'results': resultset,
                                 'favourites': favourites_json})

        else:
            return JsonResponse({'results': resultset})


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
    user_form = UserRegisterForm()
    if request.method == 'POST':
        hairdresser_form = UserRegisterForm(data=request.POST)
        page_form = HairdresserPageForm(data=request.POST)

        if request.POST.get('redir') != '':
            context_dict['redir'] = request.POST.get('redir')
            context_dict['redir_name'] = resolve(context_dict['redir']).url_name

        if hairdresser_form.is_valid() and page_form.is_valid():

            user = hairdresser_form.save()

            user.set_password(user.password)
            user.save()

            profile = page_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()
            page_form.save_m2m()

            registered = True

        else:
            print(hairdresser_form.errors, page_form.errors)

    else:
        hairdresser_form = UserRegisterForm()
        page_form = HairdresserPageForm()

    context_dict.update({'user_form': user_form,
                         'hairdresser_form': hairdresser_form,
                         'profile_form': profile_form,
                         'page_form': page_form,
                         'page_form_media': page_form.media,
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
