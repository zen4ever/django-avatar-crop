#views for uploading avatar and image cropping
#inspired by django-profile
import os.path
from django.conf import settings
from PIL import Image
from django.contrib.auth.decorators import login_required

from cropper.forms import AvatarForm, AvatarCropForm
from cropper.models import Avatar
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
    avatar, created = Avatar.objects.get_or_create(user = request.user)

    if request.method == "POST":
        form = AvatarForm()
        form = AvatarForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            avatar = form.save()
            image = Image.open(avatar.photo.path)
            image.thumbnail((settings.CROPPER_ORIGINAL_WIDTH, settings.CROPPER_ORIGINAL_WIDTH), Image.ANTIALIAS)
            width, height = image.size
            new_height = settings.CROPPER_ORIGINAL_WIDTH*height/width
            image = image.resize((settings.CROPPER_ORIGINAL_WIDTH, new_height), Image.ANTIALIAS)
            image.convert("RGB").save(avatar.photo.path, "JPEG")
            return HttpResponseRedirect(reverse("cropper_avatar_crop"))
    else:
        form = AvatarForm()

    return render_to_response("cropper/avatar_upload.html", { 'form': form, 'avatar':avatar }, context_instance=RequestContext(request))

@login_required
def avatar_crop(request):
    """
    Avatar management
    """
    avatar = get_object_or_404(Avatar, user=request.user)
    if not request.method == "POST":
        form = AvatarCropForm()
    else:
        image = Image.open(avatar.photo.path)
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
            image_name = os.path.basename(avatar.photo.path)
            newdir_name = os.path.join(settings.MEDIA_ROOT, avatar.cropped.field.upload_to)
            if not os.path.exists(newdir_name):
                os.mkdir(newdir_name)
            new_name = os.path.join(avatar.cropped.field.upload_to, image_name)
            new_path = os.path.join(settings.MEDIA_ROOT, new_name)
            image.save(new_path)
            avatar.cropped = new_name
            avatar.save()
            request.user.message_set.create(message="Your new avatar has been saved successfully.")
            return HttpResponseRedirect(reverse("cropper_avatar_upload"))
    if (avatar.photo.width<=avatar.photo.height):
        result = "width"
    else:
        result = "height"
    return render_to_response("cropper/avatar_crop.html", {'dim':result, 'avatar': avatar, 'form': form}, context_instance=RequestContext(request))

