from rest_framework_simplejwt.authentication import JWTAuthentication
JWT_authenticator = JWTAuthentication()

def is_authenticate(request):
    response = JWT_authenticator.authenticate(request)
    if response is not None:
        user , token = response
        return user , token
    return None, None

def get_permission(token):
    if "permissions" not in token.payload:
        return []
    return token.payload["permissions"]
      