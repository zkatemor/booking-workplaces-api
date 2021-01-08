import base64
import os

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.permissions import BasePermission


class BasicAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'basic':
            return None

        basic_auth_name = os.environ.get("BASIC_AUTH_NAME")
        basic_auth_pass = os.environ.get("BASIC_AUTH_PASS")

        basic_auth_key = base64.b64encode(bytes(f"{basic_auth_name}:{basic_auth_pass}", "utf-8"))

        if not basic_auth_key == auth[1]:
            raise exceptions.AuthenticationFailed("Authentication Failed")

        return "user", None


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user == "user"
