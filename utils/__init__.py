from django.shortcuts import render_to_response
from django.template import RequestContext

class BasicView(object):
    """
    Almost every view I write in django follows this structure:

        def view(request):
            ...
            template_name = "template/name.html"
            context = {'value': variable'}
            return render_to_response(template_name, context,
                context_instance = RequestContext(request))

    If you use this BasicView decorator, you can save a lot of typing

        @BasicView
        def view(request):
            ...
            template_name = "template/name.html"
            context = {'value': variable'}
            return (template_name, context)
    """

    def __init__(self, view):
        self.view = view

    def __call__(self, *args, **kwargs):
        request = args[0]
        template_name, context = self.view(*args, **kwargs)
        return render_to_response(template_name, context,
            context_instance = RequestContext(request))
