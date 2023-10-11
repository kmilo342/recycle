from rest_framework import serializers
from django.contrib.auth.models import Group, User
from .models import Material, Collection
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'url', 'username', 'email', 'groups' ]


# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']



class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class MaterialNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['name']