import requests


def login(username, password):
    response = requests.post(
        "https://dev-bxajndxfsbt0svxe.us.auth0.com/oauth/token",
        data={
            "username": username,
            "password": password,
            "realm": "Username-Password-Authentication",
            "client_id": "0WURfZm5oOZgEAvIzvDhAPCI7777iBO0",
            "client_secret": "rbFSg8UKybtgjsHgf2P9QFCwD3j8Yh0B46co0ED7aYMhId6ESTWzd-XU4Vs__TLe",
            "audience": "https://dev-bxajndxfsbt0svxe.us.auth0.com/api/v2/",
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "scope": "offline_access",
        },
    )
    return response.status_code, response.json()


def get_user_data(token, userId):
    response = requests.get(
        f"https://dev-bxajndxfsbt0svxe.us.auth0.com/api/v2/users/{userId}",
        headers={"Authorization": f"Bearer {token}"},
    )
    return response.status_code, response.json()


def get_refresh_token(token):
    response = requests.post(
        f"https://dev-bxajndxfsbt0svxe.us.auth0.com/oauth/token",
        data={
            "grant_type": "refresh_token",
            "client_id": "0WURfZm5oOZgEAvIzvDhAPCI7777iBO0",
            "client_secret": "rbFSg8UKybtgjsHgf2P9QFCwD3j8Yh0B46co0ED7aYMhId6ESTWzd-XU4Vs__TLe",
            "refresh_token": token,
        },
    )
    return response.status_code, response.json()


def get_user_id_by_email(email):
    users = get_users_list()
    for user in users:
        if user["email"] == email:
            return user["user_id"]


def get_users_list():
    response = requests.get(
        "https://dev-bxajndxfsbt0svxe.us.auth0.com/api/v2/users",
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJnZnMtZTU4Unp5TE5xNi0yWnlaMSJ9.eyJpc3MiOiJodHRwczovL2Rldi1ieGFqbmR4ZnNidDBzdnhlLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiIwV1VSZlptNW9PWmdFQXZJenZEaEFQQ0k3Nzc3aUJPMEBjbGllbnRzIiwiYXVkIjoiaHR0cHM6Ly9kZXYtYnhham5keGZzYnQwc3Z4ZS51cy5hdXRoMC5jb20vYXBpL3YyLyIsImlhdCI6MTY3NDIwNTM0NCwiZXhwIjoxNjc0MjkxNzQ0LCJhenAiOiIwV1VSZlptNW9PWmdFQXZJenZEaEFQQ0k3Nzc3aUJPMCIsInNjb3BlIjoiY3JlYXRlOmNsaWVudF9ncmFudHMgcmVhZDp1c2VycyBjcmVhdGU6dXNlcnMiLCJndHkiOiJjbGllbnQtY3JlZGVudGlhbHMifQ.TRMccghmPDGaAjZflQq3om-aGx0YwBh2NVrY5ZTzmgOrBbwueAMuTYCd3KmTLg48uJfT0x1qII3an01HlbgP-owRdA8cJ_IB8hiKqL2Dn8jTQ65IPX10YXFsX_Srx98kadMHIu7kx47c9bAxTdNZPdmLxDb96xXFHiYFQNcLUtZceMPEZSNisW57RCNwLHSkzX42zJkKktosZZR4udlMR2MV17ohG7j94iMdMTjtvzwTuciZj6JEX_KcrXCa9pU3rgOJn4E-cLL6BGlJwKKjOEr0KqUFB4_zV6czgxNX7dwYuxGF3QOchjFHXRetC3pAlLH5PHM2QnwKeXL9jltTrA"
        },
    )
    return response.json()
