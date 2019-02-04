from django.shortcuts import render, HttpResponse

# Create your views here.


def support(request):
    if request.POST:
        # send api post request to main server
        pass
    else:
        return render(request, 'support.html')