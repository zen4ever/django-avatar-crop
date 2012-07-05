import os

from django.conf import settings
from django.core.files.base import ContentFile
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from django.contrib import messages

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

try:
    from PIL import Image
except ImportError:
    import Image

from avatar_crop.forms import AvatarForm, AvatarCropForm
from avatar.models import Avatar

from avatar_crop import AVATAR_CROP_MAX_SIZE
from avatar.settings import AVATAR_STORAGE_DIR, AVATAR_THUMB_QUALITY, AVATAR_THUMB_FORMAT

@login_required
def avatar_crop(request, id=None):
    """
    Avatar management, creates a new avatar and makes it default
    """
    if id:
        avatar = get_object_or_404(Avatar, id=id, user=request.user)
    else:
        avatar = get_object_or_404(Avatar, user=request.user, primary=True)

    if (avatar.avatar.width<=avatar.avatar.height):
        result = "width"
    else:
        result = "height"

    if not request.method == "POST":
        form = AvatarCropForm()
    else:
        try:
            orig = avatar.avatar.storage.open(avatar.avatar.name, 'rb').read()
            image = Image.open(StringIO(orig))
        except IOError:
            return
        form = AvatarCropForm(image, request.POST)

        if form.is_valid():
            top = int(form.cleaned_data.get('top'))
            left = int(form.cleaned_data.get('left'))
            right = int(form.cleaned_data.get('right'))
            bottom = int(form.cleaned_data.get('bottom'))

            box = [ left, top, right, bottom ]
            (w, h) = image.size
            if result=="width":
                box = map(lambda x: x*h/AVATAR_CROP_MAX_SIZE, box)
            else:
                box = map(lambda x: x*w/AVATAR_CROP_MAX_SIZE, box)

            image = image.crop(box)
            if image.mode != 'RGB':
                image = image.convert('RGB')

            thumb = StringIO()
            image.save(thumb, AVATAR_THUMB_FORMAT, quality=AVATAR_THUMB_QUALITY)
            thumb_file = ContentFile(thumb.getvalue())

            base_name, ext = os.path.splitext(avatar.avatar.name)
            thumb = avatar.avatar.storage.save("%s_cropped%s" % (base_name, ext), thumb_file)
            Avatar.objects.filter(id=avatar.id).update(primary=False)
            new_avatar = Avatar(user=request.user, primary=True, avatar=thumb)
            new_avatar.save()
            messages.add_message(request, messages.INFO, _("Your new avatar has been saved successfully."))
            return HttpResponseRedirect(reverse("avatar_change"))

    return render_to_response("avatar_crop/crop.html", {
        'AVATAR_CROP_MAX_SIZE': AVATAR_CROP_MAX_SIZE,
        'dim': result,
        'avatar': avatar,
        'form': form
    }, context_instance=RequestContext(request))
