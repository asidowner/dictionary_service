from django.urls import path

from server.apps.dictionaries import views

urlpatterns = [
    path(
        '',
        views.DictionaryListAPI.as_view(),
    ),
    path(
        '<int:dictionary_id>/elements',
        views.DictionaryElementListAPI.as_view(),
    ),
    path(
        '<int:dictionary_id>/check_element',
        views.DictionaryCheckElementAPI.as_view(),
    ),
]
