from rest_framework import routers
from .views import WarehouseViewSet, CellViewSet

router = routers.DefaultRouter()
router.register('', WarehouseViewSet, basename='warehouse')
router.register('cells', CellViewSet, basename='cells')

urlpatterns = router.urls
