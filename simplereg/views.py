from django.template.response import TemplateResponse
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.http import HttpResponseRedirect

from simplereg.forms import RegForm


def registration(request, template_name='auth/registration.html',
            redirect_field_name=REDIRECT_FIELD_NAME,
            form_class=RegForm, extra_context=None,
            callback=None, autologin=True):

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    form = form_class(request.POST or None)
    if form.is_valid():
        user = form.save()

        if autologin:
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            login(request, user)

        if callback:
            callback(request, user)

        return HttpResponseRedirect(redirect_to)

    context = {
        'form': form
    }
    context.update(extra_context or {})
    return TemplateResponse(request, template_name, context)
