from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import login


@receiver(user_logged_in)
def custom_session_on_login(sender, request, user, **kwargs):
    # Salva os dados da sessão após o login
    request.session.save()
