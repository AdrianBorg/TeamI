from django.shortcuts import render
from trimit.forms import ReviewForm, UserRegisterForm, UserProfileForm, HairdresserPageForm, HairPageSpecialityForm, UserEditForm
from trimit.models import Page, UserProfile, Review, Treatment
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, resolve
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.safestring import mark_safe
from django.views.decorators.cache import never_cache
import json
import TeamI.settings

# Create your views here.


def index(request):
    # request.user = None
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    user_account = None
    hairdresser_account = None
    slug = None

    if not request.user.is_anonymous:
        user_account = UserProfile.objects.filter(user=request.user).exists()
        # user = UserProfile.objects.filter(id=request.user.id).exists()
        hairdresser_account = Page.objects.filter(user=request.user).exists()
    
    if hairdresser_account:
        slug = Page.objects.filter(user=request.user)[0].slug
        
    
    
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'check_hairdresser': hairdresser_account,
                    'check_user': user_account,
                    'slug': slug,}
                    
    return render(request, 'trimit/index.html', context=context_dict)


@login_required()
def user_profile(request):
    # sets the form to register from
    user_form = UserRegisterForm()

    profile_form = UserProfileForm()

    profile = UserProfile.objects.filter(user=request.user)[0]
    # sends information for reviews
    reviews = Review.objects.filter(user=profile)
    # sends information of a users favourite hairdressers
    hairdressers = profile.favourites.all()
    # sets what will be rendered
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'reviews': reviews,
                    'user_profile': profile,
                    'hairdressers': hairdressers,
                    }
    return render(request, 'trimit/user_profile.html', context_dict)


def search_input(request):
    # if request.method == "POST":
    #     search_text = request.POST['search_text']
    # else:
    #     search_text = ""
    #
    # search_results = Page.objects.filter(name__contains=search_text) # might be title__contains if it doesn't work.
    # return render_to_response('ajax_search_input.html', {'search_results': search_results}) #!
    if request.is_ajax():
        q = request.GET.get('term', '')
        qs1 = Page.objects.filter(name__icontains=q)
        qs2 = Page.objects.filter(city__icontains=q)
        results = []

        for page in qs2:
            temp = {'value': page.city,
                    'label': 'City: ' + page.city,
                    'type': 'city',
                    'img': TeamI.settings.STATIC_URL + 'images/search_city_32.png',}
            if temp not in results:
                results.append(temp)

        for page in qs1:
            results.append({'value': page.name,
                            'label': 'Page: ' + page.name,
                            'type': 'page',
                            'slug': page.slug,
                            'img': TeamI.settings.STATIC_URL + 'images/search_hairdresser_32.png',})

        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@never_cache
def results(request):
    q = request.GET.get('q')
    # create the forms for the modals
    user_form = UserRegisterForm()
    profile_form = UserProfileForm()
    context_dict = {'user_form': user_form,
                    'profile_form': profile_form, }

    # get all hairdressers in the city searched
    resultset = Page.objects.filter(city__iexact=q)

    profile_picture_urls = {}
    overall_ratings = {}

    for page in resultset: # for each hairdresser in the resultset, add the relevant info to be sent to the page
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
    # ajax function to provide search updates on the search results page
    if request.method == 'POST':
        newPages = []
        profile_picture_urls = {}
        overall_ratings = {}

        # get all the filter parameters from the request
        price = float(request.POST.get('value'))
        overall = float(request.POST.get('overall'))
        service = float(request.POST.get('service'))
        atmosphere = float(request.POST.get('atmosphere'))
        lat_bounds = [request.POST.get('latMin'), request.POST.get('latMax')]
        lng_bounds = [request.POST.get('lngMin'), request.POST.get('lngMax')]
        specialities = json.loads(request.POST.get('specialityTags'))

        # filter based on map bounds
        map_filtered_results = Page.objects.filter(latitude__gte=lat_bounds[0],
                                                   latitude__lte=lat_bounds[1],
                                                   longitude__gte=lng_bounds[0],
                                                   longitude__lte=lng_bounds[1])

        # filter based on each speciality
        for speciality in specialities:
            map_filtered_results = map_filtered_results.filter(specialities=speciality)

        # filtering out based on average review score for each rating type
        for page in map_filtered_results:
            if page.avgp is not None:
                if page.avgp < price:  # if hairdresser is excluded continue to filter next page
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

            # if hairdresser has no reviews yet, save the rating value as none
            if page.avgo is None:
                overall_ratings.update({page.user.id: 'none'})
            else:  # otherwise round the average overall rating to 1 decimal place
                overall_ratings.update({page.user.id: round(page.avgo, 1)})

        rating_filtered_results = map_filtered_results

        # serialise the results to json
        resultset = mark_safe(serializers.serialize('json', rating_filtered_results))
        new_pages = mark_safe(serializers.serialize('json', newPages))

        # check if user is logged in to find their favourites
        user = request.user
        if not request.user.is_anonymous():  # if user is logged in
            if UserProfile.objects.filter(user=user).exists():  # if user is not a hairdresser

                # get the user's favourite pages
                favourites = UserProfile.objects.filter(user=user).first().favourites.all()
                favourite_usernames = [fav.user.pk for fav in favourites]  # create a list of the page pks

                # save the list of favourite pages as a string ready to send to the client
                favourites_json = str(favourite_usernames)

                # return a json response with all the required information
                return JsonResponse({'results': resultset,
                                     'profile_picture_urls': profile_picture_urls,
                                     'ratings': overall_ratings,
                                     'new_pages': new_pages,
                                     'favourites': favourites_json})

        else:
            # if user is not logged in return a json response without the favourites
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


def ajax_user_login(request):
    # ajax function to let user log in wihtout going to a new page
    context_dict = {}
    if request.method == 'POST':
        # get credentials from request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # user info validation
        user = authenticate(username=username, password=password)

        # return the appropriate response to the user
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
    user = request.user #UserProfile.objects.get(id=request.user.id)
    hairdresser = Page.objects.get(slug=hairdresser_slug)
    has_user_page = UserProfile.objects.filter(user=request.user).exists()
    review_list = Review.objects.filter(page__slug=hairdresser.slug)
    a = (hairdresser.user==request.user)
    
    if has_user_page:
        hsp = 'true'
    else:
        hsp = None
    return render(request,
                  'trimit/hairdresserpage.html',
                  context={
                      'hairdresser': hairdresser,
                      'review_list': review_list,
                      'is_users_page': a,
                      'has_user_profile' : hsp,
                      
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
@never_cache
@login_required
def add_to_favourites(request, hairdresser_slug):
    
    user = UserProfile.objects.get(user=request.user)
    if user.favourites.filter(slug= hairdresser_slug).exists():
        
        user.favourites.remove(Page.objects.get(slug=hairdresser_slug))
        return JsonResponse({'exists': False})
    else:
    
        user.favourites.add(Page.objects.get(slug=hairdresser_slug))
        
        return JsonResponse({'exists': True})

@never_cache
def check_favourites(request, hairdresser_slug):
    user = UserProfile.objects.get(user=request.user)
    if user.favourites.filter(slug=hairdresser_slug).exists():
        return JsonResponse({'is_favourite': True }) 
    else:
        return JsonResponse({'is_favourite': False})
       




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

@login_required
def edit_hairdresserpage(request):
    current_user = request.user

    current_hairdresser = Page.objects.get(user=current_user)

    if request.method == 'POST':

        hairdresserpage_form = HairdresserPageForm(request.POST, instance=current_hairdresser)
     

        if hairdresserpage_form.is_valid():
           

            profile = hairdresserpage_form.save(commit=False)
            profile.user = request.user

            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            profile.save()
           
            hairdresserpage_form.save_m2m()

            slug = current_hairdresser.slug

            return HttpResponseRedirect(reverse('hairdresser_page', args=[slug]))
        else:
            print(hairdresserpage_form.errors)
    else:
        hairdresserpage_form = HairdresserPageForm(instance=current_hairdresser)
       

    return render(request,
                  'trimit/edit_hairdresserpage.html',
                  context={
                      'hairdresserpage_form': hairdresserpage_form,
                      'page_form_media': hairdresserpage_form.media,
                      #'hairdresser_form': user_form,
                  })


def edit_user_profile(request):
    # defines that this user will make the request to edit his profile and not another one
    current_user = request.user

    current_user_profile = UserProfile.objects.get(user=current_user)
    # Handles file upload
    if request.method == 'POST':

        user_profile_form = UserProfileForm(request.POST, instance=current_user)

        if user_profile_form.is_valid():

            profile = user_profile_form.save(commit=False)
            profile.user = request.user
            if 'profile_picture' in request.FILES:
                pic = request.FILES['profile_picture']
                user_profile = UserProfile.objects.get(user=request.user)
                user_profile.profile_picture = pic
                user_profile.save()

            # redirect to the document after the POST request
            return HttpResponseRedirect(reverse('user_profile'))
        else:
            print(user_profile_form.errors)
    else:
        user_profile_form = UserProfileForm(instance=current_user_profile)

    return render(request,
                  'trimit/edit_user_profile.html',
                  context={
                      'user_profile_form': user_profile_form,
                      'page_form_media': user_profile_form.media,
                  })


def hairdresser_register(request):
    # function to register a hairdresser user
    registered = False
    context_dict = {}
    profile_form = UserProfileForm()
    user_form = UserRegisterForm()
    if request.method == 'POST':
        # get form data from the response
        hairdresser_form = UserRegisterForm(data=request.POST)
        page_form = HairdresserPageForm(data=request.POST)

        # if user came from a specific webpage, keep sending this through to be able to redirect back to it
        if request.POST.get('redir') != '':
            context_dict['redir'] = request.POST.get('redir')
            context_dict['redir_name'] = resolve(context_dict['redir']).url_name

        if hairdresser_form.is_valid() and page_form.is_valid():  # if everything is valid

            user = hairdresser_form.save()

            # set the password and save the form
            user.set_password(user.password)
            user.save()

            profile = page_form.save(commit=False)
            profile.user = user

            # saving the picture
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # save the page info
            profile.save()
            # need to save the m2m fields (the specialities)
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
    # function to register a user
    registered = False
    context_dict = {}
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if user came from a specific webpage, keep sending this through to be able to redirect back to it
        if request.POST.get('redir') != '':
            context_dict['redir'] = request.POST.get('redir')
            context_dict['redir_name'] = resolve(context_dict['redir']).url_name

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            # set the password and save the form
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            # saving the picture
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']

            # save the profile info
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
    # logs out the user
    logout(request)
    return HttpResponseRedirect(reverse('index'))

