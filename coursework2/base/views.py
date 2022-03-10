from django.shortcuts import render

# Create your views here.
def home_screen(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return render(request, "base/home.html", context)
    else:
        return render(request, "accounts/login.html", context)