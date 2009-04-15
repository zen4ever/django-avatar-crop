#views for uploading avatar and image cropping
#inspired by django-profile
import os.path
from django.conf import settings
from PIL import Image
from django.contrib.auth.decorators import login_required

from profiles.forms import AvatarForm, AvatarCropForm
from profiles.models import Profile
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

@login_required
def avatar_upload(request):
    """
    Avatar choose
    """
    profile, created = Profile.objects.get_or_create(user = request.user)

    if request.method == "POST":
        form = AvatarForm()
        form = AvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save()
            image = Image.open(profile.photo.path)
            image.thumbnail((480, 480), Image.ANTIALIAS)
            image_name = os.path.basename(profile.photo.path)
            newdir_name = os.path.join(settings.MEDIA_ROOT, profile.avatar.field.upload_to)
            if not os.path.exists(newdir_name):
                os.mkdir(newdir_name)
            new_name = os.path.join(profile.avatar.field.upload_to, image_name)
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)
            image.convert("RGB").save(new_path, "JPEG")
            profile.avatar = new_name
            profile.save()
            return HttpResponseRedirect(reverse("profiles_avatar_crop"))
    else:
        form = AvatarForm()

    return render_to_response("profiles/avatar_upload.html", { 'form': form }, context_instance=RequestContext(request))

@login_required
def avatar_crop(request):
    """
    Avatar management
    """
    profile = get_object_or_404(Profile, user=request.user)
    if not request.method == "POST":
        form = AvatarCropForm()
    else:
        image = Image.open(profile.avatar.path)
        form = AvatarCropForm(image, request.POST)
        if form.is_valid():
            top = int(form.cleaned_data.get('top'))
            left = int(form.cleaned_data.get('left'))
            right = int(form.cleaned_data.get('right'))
            bottom = int(form.cleaned_data.get('bottom'))

            box = [ left, top, right, bottom ]
            image = image.crop(box)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')

            image.save(profile.avatar.path)
            request.user.message_set.create(message="Your new avatar has been saved successfully.")
            return HttpResponseRedirect(reverse("profiles_avatar_upload"))

    return render_to_response("profiles/avatar_crop.html", {'profile': profile, 'form': form}, context_instance=RequestContext(request))

