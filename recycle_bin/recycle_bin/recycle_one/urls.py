from django.urls import path
from recycle_bin.recycle_one import views



urlpatterns = [
    path('material/', views.MaterialList.as_view(), name='material-list'),
    path('material/<int:pk>/', views.MaterialDetail.as_view(), name='material-detail'),
    path('collection/', views.CollectionList.as_view(), name= 'collection-list'),
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection-detail'),
    path('optimalroute', views.RutaOptimaReciclaje.as_view(), name= 'ruta-optima')
]