from django import forms 
from .models import User, UserProfile
from .validators import allow_only_images_validator

# We create a new class for our user registration model to give fields into the template
class UserForm(forms.ModelForm):
    # We create a custom form fields 
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        # name the model 
        model = User
        # name fields you want to specify inside the form
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number',  'password']

    # This method will make your data clean 
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")


# Form for UserProfile model
class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    # Customizing fields with widget attrs and custom validator
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])

    # Make latitude and longitude fields readonly
    latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude'] 


    #Another variant of making readonly fields. As a rule used for a major application
    # def __init__(self, *args, **kwargs):
    #     super(UserProfileForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         if field == 'latitude' or field == 'longitude':
    #             self.fields[field].widget.attrs['readonly'] ='readonly'


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']