from django.urls import path

from students import views

app_name = 'students'
urlpatterns = [
    path('', views.StudentListView.as_view(), name='list'),
    path('new/', views.StudentCreateView.as_view(), name='create'),
]
