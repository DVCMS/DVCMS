from django.urls import path

from lectures import views

app_name = 'lectures'
urlpatterns = [
    path('', views.LectureListView.as_view(), name='list'),
    path('new/', views.LectureCreateView.as_view(), name='create'),
]
