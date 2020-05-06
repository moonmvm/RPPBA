from rest_framework import routers

from .views import ClienteleViewSet, WaybillViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('clientele', ClienteleViewSet, basename='clientele')
router.register('waybill', WaybillViewSet, basename='waybill')

urlpatterns = router.urls
