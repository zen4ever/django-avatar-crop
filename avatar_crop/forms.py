from django import forms
from django.utils.translation import ugettext_lazy as _

from avatar.models import Avatar
from avatar_crop import AVATAR_CROP_MIN_SIZE

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ('avatar',)

class AvatarCropForm(forms.Form):
    top = forms.IntegerField(widget=forms.HiddenInput, required=False)
    left = forms.IntegerField(widget=forms.HiddenInput, required=False)
    right = forms.IntegerField(widget=forms.HiddenInput, required=False)
    bottom = forms.IntegerField(widget=forms.HiddenInput, required=False)

    def __init__(self, image=None, *args, **kwargs):
        self.image = image
        super(AvatarCropForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.cleaned_data.get('top') and \
            not self.cleaned_data.get('bottom') and \
            not self.cleaned_data.get('left')  and \
            not self.cleaned_data.get('right'):
            raise forms.ValidationError(_('You need to make a selection'))

        elif self.cleaned_data.get('right') is None or self.cleaned_data.get('left') is None or int(self.cleaned_data.get('right')) - int(self.cleaned_data.get('left')) < AVATAR_CROP_MIN_SIZE:
            raise forms.ValidationError(_("You must select a portion of the image with a minimum of %(size)dx%(size)d pixels.") % {'size': AVATAR_CROP_MIN_SIZE})

        return self.cleaned_data
