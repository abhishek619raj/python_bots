from django.urls import path,URLPattern
from bot.views import FileView
from bot import views
from django.conf.urls import include, url

urlpatterns = [
url(r'^file-upload/(?P<file_id>[0-9]+)$',views.FileView.as_view()),
url(r'^python_ner/(?P<file_id>[0-9]+)$',views.FileView.as_view()),
path('file-upload/',views.FileView.as_view()),
]