from django.http import HttpResponse

def django_greetings(request) -> HttpResponse:
    return HttpResponse(
        "<h1>THIS IS SPARTA!!! WELCOME!!!</h1>"
    )

def django_greetings_2(request, name) -> HttpResponse:
    return HttpResponse(
        f"<h1>Hello, {name}</h1>"
    )




