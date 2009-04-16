For those who tired of deailing with user avatar
pictures. 

Django-cropper is a simple django application
to allow users to crop upload their avatar, 
and crop it to perfect square shape right after uploading. 

It has Avatar model which stores both original version
(rescaled to width specified in CROPPER_ORIGINAL_WIDTH)
and cropped version. 
Cropped version then can be easily scaled to any size
using PIL, or excellent sorl-thumbnail application.
