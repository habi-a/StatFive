from user.forms.RegistrationForm import RegistrationForm as RF
from django.shortcuts import redirect
from django.shortcuts import render


def register(request):
    if request.method == "POST":
        form = RF(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/login')
    else:
        form = RF()

        args = {'form': form}
        return render(request, 'register.html', args)
