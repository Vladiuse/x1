from django.utils import timezone
from django.contrib.sessions.models import Session
from users.models import CustomUser


def logout_user_sessions(user: CustomUser) -> None:
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    for session in sessions:
        data = session.get_decoded()
        if data.get('_auth_user_id') == str(user.pk):
            session.delete()