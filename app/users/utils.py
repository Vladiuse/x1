import random

from django.contrib.sessions.models import Session
from django.utils import timezone

def logout_user_sessions(user: 'CustomUser') -> None:
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.pk):
            session.delete()


def generate_reset_password_code() -> str:
    return str(random.randint(100000, 999999))
