from django.urls import path

from content.apps import ContentConfig
from content.views import ContentListView, ContentCreateView, ContentDeleteView, ContentDetailView, \
                           ContentUpdateView, MainView, ReaderListView

app_name = ContentConfig.name

urlpatterns = [
    path('', MainView.as_view(), name='main'),

    path('list/', ContentListView.as_view(), name='list'),
    path('create/', ContentCreateView.as_view(), name='create'),
    path('content/<int:pk>', ContentDetailView.as_view(), name='view'),
    path('edit/<int:pk>', ContentUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', ContentDeleteView.as_view(), name='delete'),

    path('reader-list/', ReaderListView.as_view(), name='reader_list'),
]
