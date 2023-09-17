from django.shortcuts import render,redirect
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from  rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from .models import customrole,CustomUser
from django.http import HttpResponse,JsonResponse

from django.contrib.auth.decorators import user_passes_test
import json
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate,login
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt

#create a view for home page
def Home(request):
    return render(request,'Home.html')

#view for Register a user on SEM
# @csrf_exempt
@api_view(['POST'])
def Register(request):
            #create a instance of userserializer for request
            serializer = UserSerializer(data=request.data)
            # print(request.data)
            # import pdb; pdb.set_trace()

            #check for validations
            if serializer.is_valid():
                    #if valid then save the credentials of register user
                    user = serializer.save()
                    
                    #Send the Response
                    return Response({"message":"Succesfully Register at SES",
                                     "status":"success" ,
                                      'user': {
                                        'id': user.id,
                                        'username': user.username,
                                        'email': user.email}
                                        } 
                                     ,status=status.HTTP_201_CREATED) 
            
            #If serializer is invalid the send the response with serializers errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                   
#view for Login user
@api_view(['POST'])
@csrf_exempt
def Login(request):
    if request.method  =='POST':
        try: 
            # print(request)
            #collect email and password from request
            email = request.data.get("email")
            password = request.data.get("password")
            # print(email,password)

            #authenticate user email and password 
            user = authenticate(request,email=email,password=password)
            # import pdb;pdb.set_trace()
            
            #check for user
            if user is not None:

                #login user
                login(request,user)

                #creating token for a user
                token , _ = Token.objects.get_or_create(user = user)
                
                #set the token Authorization in headers
                headers = {'Authorization': f'Token {token.key}'}
                # print(headers)

                #create a userSerializer instance
                users = UserSerializer(user)

                #return a successfull jsonResponse
                return JsonResponse({"message":"Succesfully Login at SES",
                                            "status":"success",
                                            "data":users.data ,"token":token.key }
                                            ,status=status.HTTP_200_OK, headers = headers)
        
        except json.JSONDecodeError as e:
                print('Invalid JSON data in request body',e)
    # return a response with error
    return Response({"message":"Something Went Wrong in Register"}, status=status.HTTP_400_BAD_REQUEST)

#view for Get all user details only access by admin
@api_view(['GET'])
#Token authentication
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getuser(request):
    #fetching data from request
    user = request.user
    if user.is_admin:
        #get all user data from the CustomUser model
        Users = CustomUser.objects.all()
        #create userSerializer instace for json Data
        serializer = UserSerializer(Users, many=True)  
        user_data = serializer.data
        #sends success Response
        return Response({'message': "Success. Get users", 'users': user_data} , status=200)
    # sends failure Response
    return Response({'message': "Unauthorized"}, status=403) 


# create a view for get apps created in project
@api_view(['GET'])
def getapp(request): 
    #fetching data from req
    user = request.user
    if user.is_admin:
        #collecting installedapps from the setting
        installed_apps = [app.name for app in apps.get_app_configs()  if 'site-packages' not in app.path]
        
        #send success response
        return Response({'apps':installed_apps}) 
    #sends failed Response
    return HttpResponse("You are not authorized person to access it")
     

#view for create a Role
@api_view(['POST'])
@csrf_exempt
def create_role(request):
    if request.method == 'POST':
        # fetching data from request
        role_name = request.data.get('name')

        if role_name:  
            #create a role and save it to customrole
            customrole.objects.create(name=role_name)
            #return successfull response  
            return HttpResponse("succesfully")
        else:
            #return failure response
            return HttpResponse("failed")