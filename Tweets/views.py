from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import modelform_factory, Textarea
from django.core.exceptions import ObjectDoesNotExist
from .models import *

def index(request):
    return render(request, "Tweets/index.html")

def profile(request, pid):
    prof = get_object_or_404(Profile, pk=pid)
    return render(request, "Tweets/profile.html", {"profile": prof})

ProfileForm = modelform_factory(Profile, fields=("nickname", "about"), widgets={"about": Textarea()})

@login_required
def myprofile(request):
    try:
        prof = request.user.profile
    except ObjectDoesNotExist:
        return redirect("Tweets:profile_settings")
    return render(request, "Tweets/profile.html", {"profile": prof})


@login_required
def profile_settings(request):
    if request.method == 'POST':
        try:
            mock_prof = request.user.profile
        except ObjectDoesNotExist:
            mock_prof = Profile(user = request.user)
        form = ProfileForm(request.POST, instance = mock_prof)
        # check whether it's valid:
        if form.is_valid():
            prof = form.save()
            return redirect("Tweets:myprofile")
    else:
        try:
            form = ProfileForm(instance = request.user.profile)
        except ObjectDoesNotExist:
            form = ProfileForm()

    return render(request, "Tweets/profile_settings.html", {'form': form})
