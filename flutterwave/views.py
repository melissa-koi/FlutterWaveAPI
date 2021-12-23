import requests
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User
from .serializers import UserSerializer, ViewAllUsers
from decouple import config


# Create your views here.

class RegisterView(APIView):
    serializer_class =  UserSerializer

    def post(self, request):
        serializer = self.serializer_class( data=request.data )
        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            response = {
                'data': {
                    'user': dict(user_data),
                    'status': 'success',
                    'message': 'User created successfully'
                }
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')

        return Response({
            'status': 200,
            'message': 'Login successful',
        })


class PaymentPlanView(APIView):
    post_url = "https://api.flutterwave.com/v3/payment-plans"
    key = 'FLWSECK_TEST-f7aa44fea021168c34dc45aed1507291-X'

    def post(self, request):
        email = request.data['email']

        try:
            payload = {
                "amount": 20,
                "name": email,
                "interval": "Monthly",
                "duration": 1,
                "currency": "USD"
            }

            headers = {
                "Accept": "application/json",
                "Authorization": "Bearer "+ self.key,
                "Content-Type": "application/json"
            }

            response = requests.request("POST", self.post_url, json=payload, headers=headers)

            user = User.objects.get(email=email)
            if user.email:
                user.is_premium = True
                user.save()
            else:
                user.is_premium = False
                user.save()

            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print('Exception here')
            print(e)
        return Response({
            'status': 404,
            'error': 'Payment Failed'
        })


    def get(self, request):

        active_url =    "https://api.flutterwave.com/v3/payment-plans?from=2021-01-01&to=2022-05-05&amount=20&currency=USD&interval=monthly&status=active"
        cancelled_url = "https://api.flutterwave.com/v3/payment-plans?from=2021-01-01&to=2022-05-05&amount=20&currency=USD&interval=monthly&status=cancel"
        key = config('KEY')


        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer "+ key
        }

        #check cancelled or active users
        response1 = requests.request("GET", active_url, headers=headers)
        response2 = requests.request("GET", cancelled_url, headers=headers)

        return Response(response1, status=status.HTTP_200_OK)


class ViewUsers(APIView):
    serializer_class = ViewAllUsers

    def get(self, request):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data)

    def delete(self,request):
        users = User.objects.all()
        serializers=self.serializer_class(users, many=True)
        return Response(serializers.data)


