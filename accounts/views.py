from django.shortcuts import redirect, render
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.


def registerUser(request):
    # We need to check if the method is POST and all values are valid
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # we take password from filled data form
            password = form.cleaned_data['password']
            # It means that the form is ready to save and is stored in the user variable 
            user = form.save(commit = False)
            # We define the user role before making a commit to db
            user.role = User.CUSTOMER
            # This row store user password in hash format
            user.set_password(password)
            user.save()
            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else: 
            pass
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


