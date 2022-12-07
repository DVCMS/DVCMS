from django.urls import path

from students import views

app_name = 'students'
urlpatterns = [
    path('', views.StudentListView.as_view(), name='student_list'),
]
