from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
import random
import string
from .serializers import RegisterSerializer, VerifyEmailSerializer
from .models import CustomUser


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Tasdiqlash kodi yaratish
            verification_code = ''.join(random.choices(string.digits, k=6))
            user.verification_code = verification_code
            user.save()

            # Emailga tasdiqlash kodi yuborish
            send_mail(
                'Tasdiqlash kodi',
                f'Sizning tasdiqlash kodingiz: {verification_code}',
                'no-reply@yourdomain.com',
                [user.email],
                fail_silently=False,
            )

            return Response({
                "message": "Ro'yxatdan o'tdingiz. Emailga tasdiqlash kodi yuborildi."
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            verification_code = serializer.validated_data['verification_code']

            try:
                user = CustomUser.objects.get(email=email)
                if user.verification_code == verification_code:
                    user.is_email_verified = True
                    user.is_active = True  # Tasdiqlangach faol bo'ladi
                    user.verification_code = None  # Kodni o'chirish
                    user.save()
                    return Response({"message": "Email tasdiqlandi!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Tasdiqlash kodi noto'g'ri!"}, status=status.HTTP_400_BAD_REQUEST)
            except CustomUser.DoesNotExist:
                return Response({"message": "Foydalanuvchi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
