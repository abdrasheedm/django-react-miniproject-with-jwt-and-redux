from rest_framework.views import APIView
from rest_framework.permissions import  AllowAny
from rest_framework.request import Request
from django.contrib.auth import authenticate,login
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed


# from rest_framework.response import Response
from rest_framework import permissions, status
# from .serializers import UserCreateSerializer, UserSerializer


# class RegisterView(APIView):
#     def post(self, request):
#         data = request.data

#         serializer = UserCreateSerializer(data=data)

#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         user = serializer.create(serializer.validated_data)
#         user = UserSerializer(user)

#         return Response(user.data, status=status.HTTP_201_CREATED)


# class RetrieveUserView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         user = UserSerializer(user)

#         return Response(user.data, status=status.HTTP_200_OK)

from django.shortcuts import render
from .serializers import UserCreateSerializer, LoginSerializer
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .token import create_jwt_tokens
User = get_user_model()


class RegisterView(viewsets.ModelViewSet):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


class LoginView(APIView):
    permission_classes = [AllowAny]
    # permission_classes = [permissions.IsAuthenticated]


    def post(self, request:Request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password = password)
        if user is not None:
            
            Fname = user.first_name
            Lname = user.last_name
            email = user.email
            date_joined = user.date_joined

            context = {"Fname": Fname, "Lname" : Lname, "email" : email, "join_date" : date_joined}

            if user.is_admin:
                admin = True
            else:
                admin = False


            token = create_jwt_tokens(user)
            user.user_token = token['access']
            user.save()

            response = Response()

            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = {
                'jwt' : token,
                "message": "Login successful",
                 "admin" : admin, 
                 "login":True, 
                 "user": context
            }

            
            # return Response(data={"message": "Login successful", "admin" : admin, "login":True, "user": context, 'jwt':token})
            return response
        else:
            return Response(data={"message": "Invalid email or password"})



class UserView(APIView):
    def post(self, request:Request):
        token = request.data.get('token')
        email = request.data.get('email')
        print(email)
        user = User.objects.get(email=email)
        user_token = user.user_token

        
        print(user_token)
        print('-----------------------')
        print(token)

        name = user.first_name +" "+ user.last_name

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        if not token == user_token:
            raise AuthenticationFailed('Unauthenticated')

        return Response(data={"name":name})
    

class UpdateUserView(APIView):
    def post(self, requst:Request):
        first_name = requst.data.get('first_name')
        last_name = requst.data.get('last_name')
        email = requst.data.get('email')
        old_mail = requst.data.get('oldMail')
        print(old_mail, email)
        user = User.objects.get(email=old_mail)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return Response(data={"message": "user updated successfully"})



class DeleteView(APIView):
    permission_classes = [AllowAny]

    def post(self, requst:Request):
        email = requst.data.get('email')
        user = User.objects.get(email=email)
        user.delete()
        return Response(data={"message": "user deleted successfully"})



