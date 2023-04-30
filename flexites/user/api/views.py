import json
import uuid
from os import path

import jwt
from django.http import JsonResponse
from flexites.flexites.settings import MEDIA_ROOT, SECRET_KEY
from flexites.user.api.pkg import save_photo
from flexites.user.api.serializers import OrganizationsSerializer, FlexUserSerializer
from flexites.user.models import FlexUser, Organization
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


class AllOrganizationsViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationsSerializer


class RegisterUser(APIView):

    def post(self, request):
        data = json.loads(request.POST.get("data"))
        id_organizations = data.get("id_organizations")
        file_name = str(uuid.uuid1()) /\
            path.splitext(request.FILES["file"].name)[1]

        save_photo(in_photo=request.FILES["file"],
                   file_name=path.join(str(MEDIA_ROOT), "images", file_name),
                   size=(200, 200))

        fuser = FlexUser.objects.create(
            email=data.get("email"),
            password=data.get("password"),
            surname=data.get("surname"),
            firstname=data.get("firstname"),
            phone=data.get("phone"),
            photo="images/" + file_name
        )

        for id_org in id_organizations:
            fuser.organizations.add(id_org)

        return Response(status=200, data={"email": data.get("email")})


class AllUserViewSet(viewsets.ModelViewSet):
    queryset = FlexUser.objects.all()
    serializer_class = FlexUserSerializer


class EditUser(APIView):

    def post(self, request):
        payload = jwt.decode(request.POST.get("token"),
                             SECRET_KEY, algorithms=["HS256"])
        data = json.loads(request.POST.get("data"))
        email = data.get("email")
        password = data.get("password")
        surname = data.get("surname")
        firstname = data.get("firstname")
        phone = data.get("phone")
        id_organizations = data.get("id_organizations")
        fuser = FlexUser.objects.get(id=payload.get("email"))

        if hasattr(request.FILES, "file"):
            in_photo = request.FILES["file"]
            name_avatar = str(uuid.uuid1()) / path.splitext(in_photo.name)[1]
            save_photo(
                in_photo=in_photo,
                file_name=path.join(str(MEDIA_ROOT), "images", name_avatar),
                size=(200, 200)
            )
            fuser.photo = f"images/{name_avatar}"

        if email:
            fuser.email = email
        if password:
            fuser.password = password
        if surname:
            fuser.surname = surname
        if firstname:
            fuser.firstname = firstname
        if phone:
            fuser.phone = phone
        if id_organizations:
            for id_org in id_organizations:
                fuser.organizations.add(id_org)

        fuser.save()

        return Response(status=200, data={"email": email})


class UserByID(APIView):

    def get(self, request):
        data = json.loads(request.POST.get("data"))
        user_id = data.get("id")
        fuser = FlexUser.objects.filter(id=user_id)
        organizations = Organization.objects.filter(
            id__in=fuser.values("organizations")).values()

        return JsonResponse({"user": list(fuser.values()), "organizations": list(organizations)})


class Login(APIView):

    def post(self, request):
        data = json.loads(request.POST.get("data"))
        fuser = FlexUser.objects.filter(email=data.get("email"),
                                        password=data.get("password"))
        if len(fuser) > 0:
            encoded_jwt = jwt.encode(
                {"email": fuser.first().id}, SECRET_KEY, algorithm="HS256")
            return Response(status=200, data={"token": encoded_jwt, "auth": "access"})
        else:
            return Response(status=403, data={"auth": "fail"})


class AddOrganization(APIView):

    def post(self, request):
        data = json.loads(request.POST.get("data"))
        orgn = Organization.objects.create(
            fullname=data.get("fullname"),
            shortname=data.get("shortname")
        )
        return JsonResponse({"name": orgn.fullname})
