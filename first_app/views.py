from django.http import HttpResponse

def django_greetings(request) -> HttpResponse:
    return HttpResponse(
        "<h1>THIS IS SPARTA!!! WELCOME!!!</h1>"
    )


