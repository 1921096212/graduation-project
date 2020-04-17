from django.urls import path

from . import views

app_name = 'index'

urlpatterns = [
    path('', views.Learn.as_view(), name='learn'),
    path('test/', views.test, name='test'),
    path('exam/', views.exam, name='exam'),
    # path('book/', views.bigFileView, name='book'),
]