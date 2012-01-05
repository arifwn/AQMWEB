from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse

@login_required
def view_profile(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404
    
    t = get_template('user_profile/view-profile.html')
    html = t.render(RequestContext(request, {'section': 'profile'}))
    return HttpResponse(html)
    