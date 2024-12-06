from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include

from maps.views import index

urlpatterns = [

                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('djeym/', include('djeym.urls', namespace='djeym')),

                  path('', index, name='homepage'),

                  path('map/', include('maps.urls')),
                  path('news/', include('news.urls')),
                  path('users/', include('users.urls')),
                  path('events/', include('events.urls')),
                  path('problems/', include('problems.urls')),
                  path('i18n/', include('django.conf.urls.i18n')),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT
                                                                                           )
