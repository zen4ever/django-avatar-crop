from django import forms
from cropper.models import Avatar

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ('photo',)

class AvatarCropForm(forms.Form):
    top = forms.IntegerField(widget=forms.HiddenInput)
    left = forms.IntegerField(widget=forms.HiddenInput)
    right = forms.IntegerField(widget=forms.HiddenInput)
    bottom = forms.IntegerField(widget=forms.HiddenInput)

    def __init__(self, image=None, *args, **kwargs):
        self.image = image
        super(AvatarCropForm, self).__init__(*args, **kwargs)

    def clean(self):
        if not self.cleaned_data.get('top') and \
            not self.cleaned_data.get('bottom') and \
            not self.cleaned_data.get('left')  and \
            not self.cleaned_data.get('right') and \
            self.image:
                size = self.image.size
                self.cleaned_data['top'] = 0
                self.cleaned_data['bottom'] = size[1]
                self.cleaned_data['left'] = 0
                self.cleaned_data['right'] = size[0]

        elif self.cleaned_data.get('right') is None or self.cleaned_data.get('left') is None or int(self.cleaned_data.get('right')) - int(self.cleaned_data.get('left')) < 49:
            raise forms.ValidationError("You must select a portion of the image with a minimum of 49x49 pixels.")

        return self.cleaned_data
