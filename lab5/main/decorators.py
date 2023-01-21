import functools

from authlib.oauth2 import OAuth2Error
from authlib.oauth2 import ResourceProtector as _ResourceProtector
from authlib.oauth2.rfc6749 import HttpRequest, MissingAuthorizationError
from django.shortcuts import render


class CustomeResourceProtector(_ResourceProtector):
    def acquire_token(self, request, scopes=None, add_header: dict = None):
        """A method to acquire current valid token with the given scope.
        :param request: Django HTTP request instance
        :param scopes: a list of scope values
        :return: token object
        """
        url = request.build_absolute_uri()
        headers = dict(request.headers)
        headers.update(add_header)
        req = HttpRequest(
            request.method,
            url,
            None,
            headers,
        )
        req.req = request
        if isinstance(scopes, str):
            scopes = [scopes]
        token = self.validate_request(scopes, req)
        return token

    def __call__(self, scopes=None, optional=False):
        def wrapper(f):
            @functools.wraps(f)
            def decorated(request, *args, **kwargs):
                if request.method != "POST":
                    add_header = {}
                    try:
                        access_token = request.session["access_token"]
                        # access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJnZnMtZTU4Unp5TE5xNi0yWnlaMSJ91.eyJpc3MiOiJodHRwczovL2Rldi1ieGFqbmR4ZnNidDBzdnhlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2IwNjM5MGY3MWY0YzU4ZWRmOTNiZGIiLCJhdWQiOiJodHRwczovL2Rldi1ieGFqbmR4ZnNidDBzdnhlLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaWF0IjoxNjc0MjA3MjQ0LCJleHAiOjE2NzQyOTM2NDQsImF6cCI6IjBXVVJmWm01b09aZ0VBdkl6dkRoQVBDSTc3NzdpQk8wIiwic2NvcGUiOiJyZWFkOmN1cnJlbnRfdXNlciB1cGRhdGU6Y3VycmVudF91c2VyX21ldGFkYXRhIGRlbGV0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgY3JlYXRlOmN1cnJlbnRfdXNlcl9tZXRhZGF0YSBjcmVhdGU6Y3VycmVudF91c2VyX2RldmljZV9jcmVkZW50aWFscyBkZWxldGU6Y3VycmVudF91c2VyX2RldmljZV9jcmVkZW50aWFscyB1cGRhdGU6Y3VycmVudF91c2VyX2lkZW50aXRpZXMgb2ZmbGluZV9hY2Nlc3MiLCJndHkiOiJwYXNzd29yZCJ9.mVQCMcHHIeOJp_qVBSGBSoFS8Cmq3XosJ4l9t8VWACQrU5zrsTB3Y3ME6s-XXp54lTjDXlPcJHc0QOZrIg9num77rIfpTU39xolqZHB-g1buXT73QqxiJyEXZEtctzxsJDT93C6BioJ6iapRcatlIN_h0gSwTP6emI0erc1QrY4V3hv2ouYV6TWbLisUoFo_HgXgi5XZ3kb33REb8BUjlfp_aHGvdmb8e3S8qddyMVa80BexCzCHsH4zjpt1iBQm4hDFLperGqbGDW7IvnL795C9FFK7vDiYOVK2YBQ-j677MMpLhksDPsE99__xdE9PGnR7dutjHr9GGNacHsK2Tw"
                        add_header = {"Authorization": f"Bearer {access_token}"}
                    except KeyError:
                        pass
                    try:
                        token = self.acquire_token(request, scopes, add_header)
                        request.oauth_token = token
                    except MissingAuthorizationError:
                        if optional:
                            request.oauth_token = None
                            return f(request, *args, **kwargs)
                        return render(
                            request, "login.html", {"error": "You need to log in"}
                        )
                    except OAuth2Error:
                        return render(
                            request,
                            "login.html",
                            {"error": "Your token has been expired or invalid"},
                        )
                return f(request, *args, **kwargs)

            return decorated

        return wrapper
