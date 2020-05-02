from rest_framework import routers

from .views import NomenclatureViewSet, ProductViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('nomenclature', NomenclatureViewSet, basename='nomenclature')
router.register('product', ProductViewSet, basename='product')

urlpatterns = router.urls
