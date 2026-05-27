from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ManufacturerViewSet, MedicineViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'manufacturers', ManufacturerViewSet, basename='manufacturer')
router.register(r'medicines', MedicineViewSet, basename='medicine')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]