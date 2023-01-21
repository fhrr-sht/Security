import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.shortcuts import redirect, render
from django.urls import reverse

oauth = OAuth()

oauth.register(
    "auth0",
    client_id="0WURfZm5oOZgEAvIzvDhAPCI7777iBO0",
    client_secret="rbFSg8UKybtgjsHgf2P9QFCwD3j8Yh0B46co0ED7aYMhId6ESTWzd-XU4Vs__TLe",
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://dev-bxajndxfsbt0svxe.us.auth0.com/.well-known/openid-configuration",
)


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


def logout(request):
    request.session.clear()

    return redirect(
        f"https://dev-bxajndxfsbt0svxe.us.auth0.com/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": "0WURfZm5oOZgEAvIzvDhAPCI7777iBO0",
            },
            quote_via=quote_plus,
        ),
    )


def index(request):
    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "user": json.dumps(request.session.get("user"), indent=4),
        },
    )
