from django.urls import path

from server.apps.dictionaries import views

urlpatterns = [
    path(
        '',
        views.DictionaryListApi.as_view(),
    ),
    path(
        '<int:dictionary_id>/elements',
        views.DictionaryElementListApi.as_view(),
    ),
    path(
        '<int:dictionary_id>/check_element',
        views.DictionaryCheckElementApi.as_view(),
    ),
]
