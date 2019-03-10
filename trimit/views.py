from django.shortcuts import render
from trimit.forms import UserRegisterForm, UserProfileForm, HairdresserPageForm, HairPageSpecialityForm
from trimit.models import Page, UserProfile, Specialities
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.safestring import mark_safe
import json
from django.db.models import Count
import tagulous.forms


# Create your views here.


def index(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/base.html', context=context_dict)
def user_profile(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,}
    return render(request, 'trimit/user_profile.html', context_dict)

def results(request):
    q = request.GET.get('q')
    # print(q)
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }

    resultset = Page.objects.filter(city__iexact=q)

    profile_picture_urls = {}
    overall_ratings = {}

    for page in resultset:
        profile_picture_urls.update({page.user.id: page.profile_picture.url})
        if page.avgo is None:
            overall_ratings.update({page.user.id: 'none'})
        else:
            overall_ratings.update({page.user.id: round(page.avgo, 1)})

    context_dict['search_location'] = q
    context_dict['number_of_results'] = resultset.count()
    context_dict['resultset'] = mark_safe(serializers.serialize('json', resultset))
    context_dict['speciality_field_form'] = HairPageSpecialityForm
    context_dict['profile_picture_urls'] = profile_picture_urls
    context_dict['ratings'] = overall_ratings
    # print(HairPageSpecialityForm)

    print(type(context_dict['ratings']))

    return render(request, 'trimit/results.html', context_dict)


def ajax_search_filter(request):
    if request.method == 'POST':
        newPages = []
        profile_picture_urls = {}
        overall_ratings = {}
        price = float(request.POST.get('value'))
        overall = float(request.POST.get('overall'))
        service = float(request.POST.get('service'))
        atmosphere = float(request.POST.get('atmosphere'))
        lat_bounds = [request.POST.get('latMin'), request.POST.get('latMax')]
        lng_bounds = [request.POST.get('lngMin'), request.POST.get('lngMax')]
        specialities = json.loads(request.POST.get('specialityTags'))

        # print(price, service, atmosphere, overall, specialities)
        # city = request.POST.get('city')
        # print(type(specialities[0]))
        map_filtered_results = Page.objects.filter(latitude__gte=lat_bounds[0],
                                                   latitude__lte=lat_bounds[1],
                                                   longitude__gte=lng_bounds[0],
                                                   longitude__lte=lng_bounds[1])
        # if len(specialities) > 0:
        #     map_filtered_results = map_filtered_results.\
        #                             filter(specialities__in=specialities).\
        #                             annotate(num_specs=Count('specialities')).\
        #                             filter(num_specs__gte=len(specialities))

        for speciality in specialities:
            map_filtered_results = map_filtered_results.filter(specialities=speciality)

        # filtering out based on average review score
        for page in map_filtered_results:
            # print(page.avgp, page.avgs, page.avga, page.avgo)
            if page.avgp is not None:
                if page.avgp < price:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)
                    continue
            else:
                if price > 1:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)

            if page.avgs is not None:
                if page.avgs < service and page.avgs is not None:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)
                    continue
            else:
                if service > 1:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)

            if page.avga is not None:
                if page.avga < atmosphere and page.avga is not None:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)
                    continue
            else:
                if atmosphere > 1:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)

            if page.avgo is not None:
                if page.avgo < overall and page.avgo is not None:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)
                    continue
            else:
                if overall > 1:
                    map_filtered_results = map_filtered_results.exclude(id=page.id)
                else:
                    newPages.append(page)

            # if page is not removed, save its image url
            profile_picture_urls.update({page.user.id: page.profile_picture.url})

            if page.avgo is None:
                overall_ratings.update({page.user.id: 'none'})
            else:
                overall_ratings.update({page.user.id: round(page.avgo, 1)})

        rating_filtered_results = map_filtered_results   #.filter(city__iexact=city)

        resultset = mark_safe(serializers.serialize('json', rating_filtered_results))
        new_pages = mark_safe(serializers.serialize('json', newPages))

        # print(profile_picture_urls)

        if not request.user.is_anonymous():
            user = request.user
            # print(UserProfile.objects.filter(user=user).first().favourites.all())
            favourites = UserProfile.objects.filter(user=user).first().favourites.all()
            # print(favourites, "111")
            favourite_usernames = [fav.user.pk for fav in favourites]
            # print(favourite_usernames, "222")
            favourites_json = str(favourite_usernames) #serializers.serialize('json', favourite_usernames)

            return JsonResponse({'results': resultset,
                                 'profile_picture_urls': profile_picture_urls,
                                 'ratings': overall_ratings,
                                 'new_pages': new_pages,
                                 'favourites': favourites_json})

        else:
            return JsonResponse({'results': resultset,
                                 'profile_picture_urls': profile_picture_urls,
                                 'ratings': overall_ratings,
                                 'new_pages': new_pages})


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
