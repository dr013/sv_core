import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.context import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# apps
from .forms import UserForm, ProfileForm

# Set logger
logger = logging.getLogger(__name__)


def tofirstdayinisoweek(year, week):
    max_week = datetime.date(year, 12, 31).isocalendar()[1]
    if week > max_week:
        week = 1
        year += 1
    if week < 1:
        year -= 1
        week = datetime.date(year, 12, 31).isocalendar()[1]

    ret = datetime.datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if datetime.date(year, 1, 4).isoweekday() > 4:
        ret -= datetime.timedelta(days=7)
    return ret, week


def auth(request):
    """Login"""

    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:

                login(request, user)

                logger.debug(_('User %s is authtentificated on site ' % username))

                if 'next' in request.GET:
                    next_page = request.GET['next']
                else:
                    next_page = reverse('start')

                return HttpResponseRedirect(next_page)
            else:
                messages.error(request, 'User %s is not active.' % username)
                logging.info('Authorizations error on %s/%s' % (username, password))
                return render(request, 'login.html', context=RequestContext(request, locals()))
        else:
            messages.error(request, _('Either your username or password are incorrect.'))
            logging.info(_('Authorizations error'))
            return render(request, 'login.html', context=RequestContext(request, locals()))
    else:
        if 'next' in request.GET:
            next_page = request.GET['next']
        return render(request, 'login.html', context=RequestContext(request))


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, _('Your password was successfully updated!'))
            return redirect('accounts:change_password')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
