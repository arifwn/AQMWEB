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
        profile = user.get_profile()
    except:
        raise Http404
    
    t = get_template('user_profile/view-profile.html')
    html = t.render(RequestContext(request, {'section': 'profile',
                                             'target_user': user,
                                             'target_profile': profile}))
    return HttpResponse(html)

@login_required
def edit_avatar(request):
    profile = request.user.get_profile()
    
    t = get_template('user_profile/edit-avatar.html')
    html = t.render(RequestContext(request, {'section': 'profile',
                                             'profile': profile}))
    return HttpResponse(html)

@login_required
def edit_profile(request):
    profile = request.user.get_profile()
    
    t = get_template('user_profile/edit-profile.html')
    html = t.render(RequestContext(request, {'section': 'profile',
                                             'profile': profile}))
    return HttpResponse(html)
