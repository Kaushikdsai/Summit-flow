from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from .models import User

class CustomAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_id = request.session.get('user_id')
        print(f"Session user_id: {user_id}")

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                request.user = user
                print(f"User attached: {user.email}")
            except User.DoesNotExist:
                request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
