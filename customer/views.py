from django.shortcuts import render,redirect
from rest_framework import viewsets
from .models import Customer,Review
from .serializers import CustomerSerializer,ReviewSerializer,UserLoginSerializer,RegistrationSerializer,PasswordChangeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib import messages
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
# views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters, pagination

class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__id','user__username']

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['pet__id']


class ReviewCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = Customer.objects.get(user=request.user)
            except Customer.DoesNotExist:
                return Response({"detail": "Customer not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save(reviewer=customer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserRegistrationApiView(APIView):
    serializer_class = RegistrationSerializer

    def post(self,request):
        print("inside  post") 
    
        serializer = self.serializer_class(data=request.data)
        print("register serializer",serializer)
        if serializer.is_valid():
            user = serializer.save()
            print("inside register valid",user)
            token = default_token_generator.make_token(user)
            print('token', token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print('uid',uid)
            confirm_link = f'https://exipet-drf-api.onrender.com/customer/active/{uid}/{token}'
            email_subject = "Confirmation Email"
            email_body = render_to_string('confirm_email.html',{'confirm_link':confirm_link}) 
            email = EmailMultiAlternatives(email_subject,'',to=[user.email])
            email.attach_alternative(email_body,"text/html")
            email.send()
            return Response({'error':'Check your mail for confirmation.'})
        else:
            print("Serializer errors",serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response({'error':serializer.errors})

def activate(request,uid64,token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('https://exipet.netlify.app/login.html')
    else:
        return redirect('https://exipet.netlify.app/registration.html')

class UserLoginApiView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username,password=password)

            if user:
                token,_ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request,user)
                return Response({'token':token.key,'user_id':user.id ,'error':'Logged in Successfully'})
            else:
                return Response({'error':'Invalid Credential'})
        else:
            return Response(serializer.errors)

class UserLogoutApiView(APIView):
    def get(self,request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('https://exipet.netlify.app/login.html')

class PasswordChangeView(APIView):
    # permission_classes=[IsAuthenticated]

    def post(self,request,*args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            update_session_auth_hash(request,user)
            return Response({"detail":"Password updated successfully."},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


