from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import UserViewSet, AnexoViewSet, planilha
from django.conf.urls.static import static

from configuracao import settings

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'anexo', AnexoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path('planilha/', planilha)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
