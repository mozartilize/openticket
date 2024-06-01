from django.shortcuts import render


def index(request):
	return render(request, "index.html")


def event_index(request):
	return render(request, "events/index.html")

def event_form(request):
	if request.method == "POST":
		print(request.POST)
	return render(request, "events/new.html")