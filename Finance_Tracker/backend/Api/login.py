from ..Serials.serializer import CustomUserSerializer, UserLoginSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

#from ..Auth.secret_key import SECRET_KEY
#from ..Components.kafka_registration import KafkaUserRegistration

CustomUser = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = serializer.data

            #Publish message to the "User_Registration" topic --unused_feature
            #messager = KafkaUserRegistration()
            #messager.user_register("User_Registration", [data['username'], data['email'], data['uuid'], SECRET_KEY])
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data
        if user:
            serializer = CustomUserSerializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data['refresh'] = str(token)
            data['access'] = str(token.access_token)
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'error': 'Invalid Credentails'}, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            request_token = request.data['refresh']
            token = RefreshToken(request_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

'''
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request):
        CustomUser = get_user_model()
        user = CustomUser.objects.get(user=self.request.user)
        print("Line 68", user)
        serializer = CustomUserSerializer(data=user)
        if serializer.is_valid():
            print("Line 71", serializer.data)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)

'''