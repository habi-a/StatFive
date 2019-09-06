from user.forms import RegistrationForm
from django.shortcuts import redirect
from django.shortcuts import render


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/user/login')
    else:
        form = RegistrationForm()

        args = {'form': form}
        return render(request, 'register.html', args)
