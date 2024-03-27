from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


from .models import User, Phone
from .serialize import UserSerializer, PhoneSerializer, UserLoginSerializer

class ListCreatePhoneView(ListCreateAPIView):
    model = Phone
    serializer_class = PhoneSerializer

    def get_queryset(self):
        return Phone.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = PhoneSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Create a new Phone successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Phone unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateDeletePhoneView(RetrieveUpdateDestroyAPIView):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    lookup_field = 'name'

    def put(self, request, *args, **kwargs):
        phones = Phone.objects.filter(name=kwargs.get('name'))  # Lấy tất cả các đối tượng có giá trị name giống với giá trị được truyền từ URL
        if phones.exists():  # Kiểm tra xem có đối tượng nào không
            phone = phones.first()  # Lấy đối tượng đầu tiên
            serializer = PhoneSerializer(phone, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'message': 'Update Phone successful!'
                }, status=status.HTTP_200_OK)
            return JsonResponse({
                'message': 'Update Phone unsuccessful!'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({
                'message': 'Phone not found!'
            }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        phones = Phone.objects.filter(name=kwargs.get('name'))  # Lấy tất cả các đối tượng có giá trị name giống với giá trị được truyền từ URL
        if phones.exists():  # Kiểm tra xem có đối tượng nào không
            phone = phones.first()  # Lấy đối tượng đầu tiên
            phone.delete()
            return JsonResponse({
                'message': 'Delete Phone successful!'
            }, status=status.HTTP_200_OK)
        else:
            return JsonResponse({
                'message': 'Phone not found!'
            }, status=status.HTTP_404_NOT_FOUND)
    
class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Register successful!'
            }, status=status.HTTP_201_CREATED)

        else:
            return JsonResponse({
                'error_message': 'This name has already exist!',
                'errors_code': 400,
            }, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(username=username)
                print(user.username)
            except User.DoesNotExist:
                return Response({
                    'error_message': 'Tên người dùng không tồn tại!',
                    'error_code': 400
                }, status=status.HTTP_400_BAD_REQUEST)
            

            if user.password != password:
                return Response({
                    'error_message': 'Mật khẩu không chính xác!',
                    'error_code': 400
                }, status=status.HTTP_400_BAD_REQUEST)


            user_data = {
                'id': user.id,
                'username': user.username,

            }
            return Response(user_data, status=status.HTTP_200_OK)

        return Response({
            'error_messages': serializer.errors,
            'error_code': 400
        }, status=status.HTTP_400_BAD_REQUEST)
    

class ListUserView(ListCreateAPIView):
    model = User
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()