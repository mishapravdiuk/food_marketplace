from django import forms 
from .models import User

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
