from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .yasg import doc_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("src.account.urls")),
    path("", include("src.search.urls")),
    path("", include("src.main.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    # path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += doc_urlpatterns
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
