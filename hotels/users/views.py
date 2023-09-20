from django.shortcuts import render
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken 
from django.db import transaction
from django.contrib.auth.models import User
from .models import CustomUser, UserPermission
from django.contrib.auth import authenticate 
from .permission import get_permission_list_string

# Create your views here.
class UserAPIView(APIView):
    def post(self, request):
        data = request.data
        if (User.objects.filter(username=data["username"]).exists()):
            return Response({"reason":"User already exits."}, status=status.HTTP_409_CONFLICT)
        with transaction.atomic():
            try: 
                user = User.objects.create_user(username=data["username"],password=data["password"])
                user.save()
                CustomUser.objects.create(user=user, user_type = data["user_type"]).save()
            except Exception as e:
                print(str(e))
                return Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({}, status=status.HTTP_201_CREATED)
    
class Authorization(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(username=data["username"], password=data["password"])
        data = {}
        if user is not None:
            # get permission list 
            customUser = CustomUser.objects.get(user=user)
            permissionList = UserPermission.objects.filter(user_type=customUser.user_type)
            permission_list_string = get_permission_list_string(permissionList)
            refresh = RefreshToken.for_user(user)
            refresh.payload["permissions"] = permission_list_string
            data={
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            status_code=status.HTTP_200_OK
        else:
            data = {
                "reason":"Invalid username or password."
            }
            status_code=status.HTTP_401_UNAUTHORIZED
        return Response(data, status=status_code)    
