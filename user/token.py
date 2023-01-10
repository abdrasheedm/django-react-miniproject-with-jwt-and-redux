from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

User = get_user_model()
def create_jwt_tokens(user:User):
    

    refresh = RefreshToken.for_user(user)
    name = user.first_name + " " + user.last_name
    refresh['Fullname'] = name
    refresh['email'] = user.email

    tokens = {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }

    return tokens 