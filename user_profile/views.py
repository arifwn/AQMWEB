from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from django.shortcuts import redirect
from django.conf import settings

@login_required
def view_profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = user.get_profile()
    except User.DoesNotExist:
        raise Http404
    
    t = get_template('user_profile/view-profile.html')
    html = t.render(RequestContext(request, {'section': 'profile',
                                             'target_user': user,
                                             'target_profile': profile
                                             }))
    return HttpResponse(html)

@login_required
def edit_avatar(request):
    from user_profile.forms import AvatarEditForm
    
    profile = request.user.get_profile()
    
    if request.method == 'POST':
        form = AvatarEditForm(request.POST, request.FILES)
        if form.is_valid(): 
            fd = form.cleaned_data['avatar']
            profile.avatar.save(fd.name, fd, True)
            return redirect('view-profile', request.user.username)
    else:
        form = AvatarEditForm()

    t = get_template('user_profile/edit-avatar.html')
    html = t.render(RequestContext(request, {'section': 'profile',
                                             'profile': profile,
                                             'form': form
                                             }))
    return HttpResponse(html)


@login_required
def edit_profile(request):
    from user_profile.forms import ProfileEditForm
    
    profile = request.user.get_profile()
    
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid(): 
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            return redirect('view-profile', request.user.username)
    else:
        form = ProfileEditForm(initial={'first_name': request.user.first_name,
                                        'last_name': request.user.last_name,
                                        'email': request.user.email 
                                        })

    t = get_template('user_profile/edit-profile.html')
    html = t.render(RequestContext(request, {'section': 'profile',
                                             'profile': profile,
                                             'form': form
                                             }))
    return HttpResponse(html)


def avatar_t32x32(request, username=None):
    ''' Redirect to 32x32 avatar icon. Create one if not available '''
    from filebrowser.functions import version_generator
    from filebrowser.sites import get_default_site
    
    if username is None:
        anon_path = version_generator('image/profile/anon.png', 't32x32', site=get_default_site())
        anon_url = '%s%s' %(settings.MEDIA_URL, anon_path)
        return redirect(anon_url)
    
    try:
        user = User.objects.get(username=username)
        profile = user.get_profile()
    except User.DoesNotExist:
        anon_path = version_generator('image/profile/anon.png', 't32x32', site=get_default_site())
        anon_url = '%s%s' %(settings.MEDIA_URL, anon_path)
        return redirect(anon_url)
    
    avatar_path = version_generator(profile.avatar.__unicode__(), 't32x32', site=get_default_site())
    avatar_url = '%s%s' %(settings.MEDIA_URL, avatar_path)
    return redirect(avatar_url)
    
    