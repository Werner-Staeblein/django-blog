from django.shortcuts import render
from .models import About
from .forms import CollaborateForm


def about_me(request):
    """
    Renders the About page
    """
    about = About.objects.all().order_by('-updated_on').first()
    collaborate_form = CollaborateForm()

# Die collaborate_form wurde hier mit Referenz auf forms.py hinzugefügt.
# wird zur Kontextvariablen

    return render(
        request,
        "about/about.html",
        {
            "about": about,
            "collaborate_form": collaborate_form
        },
    )