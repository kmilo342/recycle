from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .models import Material, Collection
from .serializers import MaterialSerializer, CollectionSerializer, MaterialNameSerializer

class MaterialList(APIView):
    """
    API endpoint que maneja la lista de materiales.
    """
    def get(self, request):
        material_set = Material.objects.all()
        serializer = MaterialSerializer(material_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class MaterialDetail(APIView):
    """
    API endpoint que maneja los detalles de un material específico.
    """
    def get_object(self, pk):
        try:
            int_obj = int(pk)
            return Material.objects.get(id=int_obj)
        except (Material.DoesNotExist, ValueError):
            raise Http404
        
    def get(self, request, pk):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        material = self.get_object(pk)
        serializer = MaterialSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionList(APIView):
    """
    API endpoint que maneja la lista de recolecciones.
    """
    def get(self, request):
        collection_set = Collection.objects.all()
        serializer = CollectionSerializer(collection_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            material_id = request.data['material']
            collected_cant = request.data['weight']

            material = Material.objects.get(pk=material_id)
            material.weight += collected_cant
            material.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectionDetail(APIView):

    """
    API endpoint que maneja los detalles de una recoleccion específica.
    """
    def get_object(self, pk):
        try:
            int_obj = int(pk)
            return Collection.objects.get(id=int_obj)
        except (Collection.DoesNotExist, ValueError):
            raise Http404
        
    def get(self, request, pk):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        material = self.get_object(pk)
        last_cant = material.weight
        serializer = CollectionSerializer(material, data=request.data)
        if serializer.is_valid():
            serializer.save()

            material_id = request.data['material']
            new_cant = request.data['weight']
            difference = new_cant - last_cant
            material = Material.objects.get(pk=material_id)
            material.weight += difference
            material.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


from recycle_bin.recycle_one.functions import optimal_materials_calculator


class RutaOptimaReciclaje(APIView):

    def get(self, request):
        material_set = Material.objects.all()
        serializer = MaterialNameSerializer(material_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        materials = request.data.get('materials', [])
        limit_weight = request.data.get('limit_weight', 0)

        optimized_materials = optimal_materials_calculator(materials, limit_weight)
        
        total_value = sum(material['value'] for material in optimized_materials)

        response_data = {
            'optimized_materials': optimized_materials,
            'total_value': total_value
        }

        return Response(response_data, status=status.HTTP_200_OK)