from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit


@ratelimit(key='user_or_ip', rate=lambda req: '10/m' if req.user.is_authenticated else '5/m', method='POST', block=True)
def login_view(request):
    # Placeholder for actual login logic
    return HttpResponse("Login processed successfully")