from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework import viewsets
from recycle_bin.recycle_one.models import *
from recycle_bin.recycle_one.serializers import *


class CustomTokenObtainPairView(TokenObtainPairView):
    pass


