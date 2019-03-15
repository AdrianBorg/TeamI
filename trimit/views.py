from django.shortcuts import render
from trimit.forms import ReviewForm, UserRegisterForm, UserProfileForm, HairdresserPageForm, HairPageSpecialityForm, UserEditForm
from trimit.models import Page, UserProfile, Specialities, Review, Treatment, User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Avg
from django.views.decorators.cache import never_cache
import json
import TeamI.settings
from django.db.models import Count
import tagulous.forms

# Create your views here.
def index(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }

    # context_dict.update(csrf(request))
    
    return render(request, 'trimit/index.html', context=context_dict)

@csrf_exempt
def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = Page.objects.filter(name__startswith=q, city__startswith=q)
        results = []   
        # print(q)
        for page in search_qs:
            page_json = {}
            page_json['name'] = page.name
            page_json['slug'] = page.slug
            page_json['city'] = page.city
            results.append(page_json)

        data_json = json.dumps(results)
    else:
        data_json = 'fail'
    mimetype = 'application/json'

    return HttpResponse(data_json, mimetype)

@csrf_exempt
def get_names(request):
    if request.is_ajax():
        q = request.GET.get('term','')
        names = Page.objects.filter(name__startswith=q)
        results = []
        for name in names:
            name_json = {}
            name_json = name.name + "," + name.slug
            results.append(name_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


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

@never_cache
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
    context_dict['page_link_image_url'] = TeamI.settings.MEDIA_URL + "PageLink.png"
    # print(HairPageSpecialityForm)

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
        user = request.user
        if not request.user.is_anonymous():
            if UserProfile.objects.filter(user=user).exists():

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
    return render(request, 'trimit/about.html', context=context_dict)


def contact_us(request):
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }
    return render(request, 'trimit/contact_us.html', context=context_dict)


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

@never_cache
def hairdresser_page(request, hairdresser_slug):
    hairdresser = Page.objects.get(slug=hairdresser_slug)
    review_list = Review.objects.filter(page__slug=hairdresser.slug)

    a = (hairdresser.user==request.user)


    return render(request,
                  'trimit/hairdresserpage.html',
                  context={
                      'hairdresser': hairdresser,
                      'review_list': review_list,
                      'is_users_page': a,
                  }
                  )

@never_cache
def hairdresser_load(request, hairdresser_slug):
    treatment_list = Treatment.objects.filter(page__slug=hairdresser_slug)

    return render(request,
                  'trimit/hairdresserpage_load_content.html',
                  context={
                      'treatment_list': treatment_list,
                  }
                  )


    #@login_required(login_url='ajax_user_login')
    #def write_review(request, hairdresser_slug):
    hairdresser = Page.objects.get(slug=hairdresser_slug)
    if request.method == 'POST':
        review_form = ReviewForm(
            data={
                'page': hairdresser,
                'user': request.user,
                **request.POST
            },
        )

        if review_form.is_valid():
            review_form.save()
    #  else:
    #     print(request.user.errors)
    else:
        review_form = ReviewForm()
        # review_form.hairdresser

    return render(
        request,
        'trimit/review_hairdresser.html',
        context={'form': review_form, 'hairdresser': hairdresser}
    )

@login_required(login_url='ajax_user_login')
def write_review(request, hairdresser_slug):
    hairdresser = Page.objects.get(slug=hairdresser_slug)
    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.page = hairdresser
            review.user = UserProfile.objects.get(id=request.user.id)

            review.save()
        else:
            print(review_form.errors)
    else:
        review_form = ReviewForm()

    return render(
        request,
        'trimit/review_hairdresser.html',
        context={'form': review_form, 'hairdresser': hairdresser}
    )


def edit_hairdresserpage(request):
    current_user = request.user

    current_hairdresser = Page.objects.get(user=current_user)

    if request.method == 'POST':

        hairdresserpage_form = HairdresserPageForm(request.POST, instance=current_hairdresser)
        # user_form = UserEditForm(request.POST, instance=request.user)

        if hairdresserpage_form.is_valid():#and hairdresserpage_form.is_valid():
            # user = user_form.save()
            #
            # user.set_password(user.password)
            # user.save()

            profile = hairdresserpage_form.save(commit=False)
            profile.user = request.user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()
            # page_form.save()
            hairdresserpage_form.save_m2m()

            slug = current_hairdresser.slug

            return HttpResponseRedirect(reverse('hairdresser_page', args=[slug]))
        else:
            print(hairdresserpage_form.errors)
    else:
        hairdresserpage_form = HairdresserPageForm(instance=current_hairdresser)
        # user_form = UserEditForm(instance=request.user)

    return render(request,
                  'trimit/edit_hairdresserpage.html',
                  context={
                      'hairdresserpage_form': hairdresserpage_form,
                      'page_form_media': hairdresserpage_form.media,
                      #'hairdresser_form': user_form,
                  })


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


#@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

