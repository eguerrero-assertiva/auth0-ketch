import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from feedapp.auth0_backend import Auth0Backend
from feedapp.models import Service

oauth = OAuth()
auth = Auth0Backend()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


### Intgracion con Okta

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    user = auth.authenticate(request, token=token)
    if user:
        return redirect(request.build_absolute_uri(reverse("index")))
    return HttpResponse(status=400)


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


### Intgracion con Okta

def index(request):
    response = HttpResponse("Cookie consent accepted")
    response.set_cookie('cookie_consent', 'accepted', max_age=31536000)  # 1 year
    pretty = json.dumps(request.session.get("user"), indent=4)
    if request.session.get("user") is not None:
        auth0_id = json.loads(pretty)["userinfo"]["sub"]
    else:
        auth0_id = ""
    return render(
        request,
        "bootstrap_index.html",
        context={
            "auth0_id": auth0_id,
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
            "services": Service.objects.all()
        },
    )


def detail(request, pk):
    service = Service.objects.get(pk=pk)
    pretty = json.dumps(request.session.get("user"), indent=4)
    auth0_id = json.loads(pretty)["userinfo"]["sub"]
    context = {
        "service": service,
        "sessionid": request.COOKIES.get('sessionid'),
        "auth0_id": auth0_id,
        "ketch_id": request.COOKIES.get('_swb'),
        "session": request.session.get("user"),
        "pretty": pretty,
    }
    return render(request, "detail.html", context)


def policy(request):
    return render(request, "policy.html")


def terms(request):
    return render(request, "terms.html")
