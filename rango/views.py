# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from rango.models import Category, Page
from rango.utilities import urlencoding
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    context = RequestContext(request)

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    for category in category_list:
        category.url = urlencoding(param=category.name)

    return render_to_response('rango/index.html', context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)

    category_name = urlencoding(category_name_url)

    context_dict = {
        'category_name': category_name,
        'category_name_url': category_name_url
    }

    try:
        category = Category.objects.get(name=category_name)

        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render_to_response('rango/category.html', context_dict, context)


def add_category(request):
    context = RequestContext(request)

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render_to_response('rango/add_category.html', {'form': form}, context)


def add_page(request, category_name_url):
    context = RequestContext(request)

    category_name = urlencoding(param=category_name_url)
    context_dict = {
        'category_name_url': category_name_url,
        'category_name': category_name,
    }
    try:
        categoryvalue = Category.objects.get(name=category_name)

        context_dict['category'] = categoryvalue
    except Category.DoesNotExist:
        pass

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)

            try:
                cat = Category.objects.get(name=category_name)
                page.category = cat
            except Category.DoesNotExist:
                return render_to_response('rango/add_category.html', {}, context)

            page.views = 0

            page.save()

            return category(request, category_name_url)
        else:
            print form.errors

    else:
        form = PageForm()

        context_dict['form'] = form

    return render_to_response('rango/add_page.html', context_dict, context)


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response('rango/register.html',{
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    }, context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango')
            else:
                return HttpResponse('You Rango account is disabled.')
        else:
            print 'Invalid login details: {0}, {1}'.format(username, password)
            return HttpResponse('Invalid login details supplied.')

    else:
        return render_to_response('rango/login.html', {}, context)


@login_required
def restricted(request):
    context = RequestContext(request)
    
    return render_to_response('rango/restricted.html', {}, context)


@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')