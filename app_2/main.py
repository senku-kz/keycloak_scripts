import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi_keycloak import FastAPIKeycloak, OIDCUser


# Конфигурация Keycloak
KEYCLOAK_DOMAIN = "http://localhost:8080"
REALM = "my-realm"
CLIENT_ID = "client-app-2"  # ID вашего клиента в Keycloak
CLIENT_SECRET = "123"
JWKS_URL = f"{KEYCLOAK_DOMAIN}/realms/{REALM}/protocol/openid-connect/certs"
TOKEN_URL = f"{KEYCLOAK_DOMAIN}/realms/{REALM}/protocol/openid-connect/token"
AUTHORIZATION_URL = f"{KEYCLOAK_DOMAIN}/realms/{REALM}/protocol/openid-connect/auth"
REFRESH_URL = f"{KEYCLOAK_DOMAIN}/realms/{REALM}/protocol/openid-connect/token"


app = FastAPI()
idp = FastAPIKeycloak(
    server_url="http://localhost:8080/auth",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    admin_client_secret=CLIENT_SECRET,
    realm=REALM,
    callback_uri="http://localhost:8082/callback"
)
idp.add_swagger_config(app)


@app.get("/")  # Unprotected
def root():
    return 'Hello World'


@app.get("/user")  # Requires logged in
def current_users(user: OIDCUser = Depends(idp.get_current_user())):
    return user


@app.get("/admin")  # Requires the admin role
def company_admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
    return f'Hi admin {user}'


@app.get("/login")
def login_redirect():
    return RedirectResponse(idp.login_uri)


@app.get("/callback")
def callback(session_state: str, code: str):
    return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token


if __name__ == '__main__':
    uvicorn.run('app:app', host="127.0.0.1", port=8082)
