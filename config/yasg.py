from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='HIT TRAVEL',
        default_version='v1',
        description='API for HIT TRAVEL',
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
    url="https://hit-travel.org"
)

doc_urlpatterns = [
    path('api/docs.json/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
