from django.views.generic import TemplateView


class InitialView(TemplateView):
    template_name = "app/index.html"
