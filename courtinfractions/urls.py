from django.urls import path
from .views import (
    CIListView,
    CIDetailView,
    CICreateView,
    CIUpdateView,
    CIDeleteView,
    CIMemberListView,
    CIDateListView,
)
#The '.' represents the root file directory
from . import views

urlpatterns = [
    # The URL is created to 'about/', it pulls from the views.py file's about function, named 'CI-about'
    path('summary/', CIListView.as_view(), name='CI-summary'),
    path('table/', views.CITableView, name='CI-table'),
    #The slug <str:name_id> is passed to CIMemberListView as the value searched for in self.kwargs.get(...)
    path('summary/name/<str:name_id>', CIMemberListView.as_view(), name='CI-member'),
    path('summary/date/<str:date>', CIDateListView.as_view(), name='CI-date'),
    path('record/<int:pk>/', CIDetailView.as_view(), name='CI-record'),
    path('record/new/', CICreateView.as_view(), name='CI-new'),
    path('record/<int:pk>/update', CIUpdateView.as_view(), name='CI-update'),
    path('record/<int:pk>/delete', CIDeleteView.as_view(), name='CI-delete'),
    #path([NAME OF URL], [VIEWS FILE.FUNCTION OF VIEWS FILE], [NAME OF PATH TO CALL FOR LATER USE])
    path('record/multinew/', views.CIFormsetView, name='CI-multinew'),
    path('email/', views.CIEmailFormView, name='CI-email'),
]
