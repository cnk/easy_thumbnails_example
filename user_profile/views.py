from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http.response import HttpResponseNotAllowed
from .forms import AvatarForm
from .models import UserProfile

def home(request):
    return TemplateResponse(request, 'user_profile/home.html', {'user': request.user})

def login(request):
    auth_logout(request)
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None and user.is_active:
            auth_login(request, user)
            return redirect(request.REQUEST.get('next', '/'))
        else:
            return render(request, 'login.html', {
                'message': 'Username or password is incorrect.',
                'next': request.REQUEST.get('next', '/'),
                'username': request.POST['username'],
            })
    elif request.method == 'GET':
        return render(request, 'user_profile/login.html', {'next': request.REQUEST.get('next', '/'), 'username': ''})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


@login_required
def profile(request):
    try:
        profile = UserProfile.objects.get(user_id=request.user.id)
    except ObjectDoesNotExist:
        profile = None

    return TemplateResponse(request, 'user_profile/profile.html', {'user': request.user, 'profile': profile})


@login_required
def upload_avatar(request):
    """
    Form to add/edit a user's avatar image.
    """

    if request.method == "GET":
        form = AvatarForm()
    else:
        profile = UserProfile.objects.filter(user_id=request.user.id)
        if profile:
            form = AvatarForm(request.POST, request.FILES, instance=profile[0])
        else:
            form = AvatarForm(request.POST, request.FILES, instance=UserProfile(user=request.user))
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))

    return TemplateResponse(request, 'user_profile/avatar.html',
                            {'user': request.user, 'avatar_form': form, })
