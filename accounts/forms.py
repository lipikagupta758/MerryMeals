from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator

class UserRegisterationForm(forms.ModelForm):
    password= forms.CharField(widget=forms.PasswordInput()) 
    confirm_password= forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model= User
        fields= ['first_name', 'last_name', 'username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data= super(UserRegisterationForm, self).clean()
        password= cleaned_data.get('password')
        confirm_passowrd= cleaned_data.get('confirm_password')

        if password!= confirm_passowrd:
            raise forms.ValidationError(
                "Password does not match!"
            )

class UserProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start typing.. ', 'required': 'required'}))
    profile_picture= forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator], required=False)
    cover_photo= forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator], required=False)
    latitude= forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    longitude= forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
        model= UserProfile
        fields=['profile_picture', 'cover_photo', 'address', 'city', 'state', 'country', 'pin_code', 'longitude', 'latitude']

    # To make some fields read only
    # def __init__(self, *args, ** kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field =='latitude' or field=='longitude':
    #             self.fields[field].widget.attrs['readonly']= True