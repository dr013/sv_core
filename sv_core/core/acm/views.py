import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as internal_login
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.template.context import RequestContext
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

# apps
from .models import Empl

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
