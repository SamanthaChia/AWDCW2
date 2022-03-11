from django.shortcuts import render, redirect

# Create your views here.
def home_screen(request):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("status:timeline")
	else:
		return render(request, "base/home.html", context)