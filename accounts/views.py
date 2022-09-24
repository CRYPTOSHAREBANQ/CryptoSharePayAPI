from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.views import View

from accounts.models import Account, Country
from businesses.models import Business
from api_keys.models import Api_Key

# from rest_framework import Response
from rest_framework.response  import Response
from rest_framework import status

import secrets

# Create your views here.

class CreateAccount(View):
    def post(self, request):
        data = request.data
        customer_info = data["customer_info"]
        business_info = data.get("business_info", None)

        if User.objects.filter(email = customer_info["email"]).exists():
            return Response({'error': 'Email already exists'}, status=400)

        new_user = User.objects.create_user(
            username = data['email'], 
            password = data['password'], 
            email = data['email'],
            first_name = data['first_name'],
            last_name = data['last_name']
            )


        if Country.objects.filter(country_id=data['country_id']).exists():
            return Response({'error': 'Country Code does not exist'}, status=400)

        new_account = Account.objects.create(
            type = "CUSTOMER", 
            email = new_user, 
            first_name = data['first_name'], 
            last_name = data['last_name'], 
            country_id = Country.objects.get(
                country_id=data['country_id']
                )
            )

        if business_info:
            new_business = Business.objects.create(
                user_id = new_account, 
                name = business_info['name'], 
                description = business_info['description']
                )

        new_generated_key = secrets.token_hex(16)

        new_api_key = Api_Key.objects.create(
            api_key = "tsk_" + new_generated_key,
            user_id = new_account,
            business_id = new_business if business_info else None,
            type = "TEST",
            status = "ACTIVE"
            )

        
        response_object = {
            "status": "SUCCESS",
            "message": "Customer created successfully",
            "data": {
                "api_key": new_api_key.api_key,
                "account_id": new_account.user_id,
                "business_id": new_business.business_id if business_info else None
            }
        }

        return Response(response_object, status=status.HTTP_200_OK)

