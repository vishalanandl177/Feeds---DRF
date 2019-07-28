from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.documentation import include_docs_urls
from config import settings
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')
'''
docs/ - Django APIs schema docs
swagger-docs - Swagger APIs schema docs
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'user/', include(('user.urls', 'user'), namespace='user')),
    url(r'feed/', include(('feed.urls', 'feed'), namespace='feed')),
    url(r'^docs/',
        include_docs_urls(title='API Documentation', public=settings.DEBUG)),
    url(r'^swagger-docs/$', schema_view),

]

# Enable debug toolbar only if DEBUG is True
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
