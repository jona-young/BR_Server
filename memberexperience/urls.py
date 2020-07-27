from django.urls import path
from . import views
from .views import (
    MEListView,
    MEDetailView,
    MEUpdateView,
    MEDeleteView,
)

urlpatterns = [
    path('summary/', MEListView.as_view(), name='ME-summary'),
    path('record/<int:pk>/', MEDetailView.as_view(), name='ME-record'),
    path('record/new/', views.MECreateView, name='ME-new'),
    path('record/<int:pk>/update', MEUpdateView.as_view(), name='ME-update'),
    path('record/<int:pk>/delete', MEDeleteView.as_view(), name='ME-delete'),
]