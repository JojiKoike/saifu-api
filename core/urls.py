from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from core.views.incomecategory import IncomeCategoryList, IncomeCategoryMainList, \
    IncomeCategoryMainDetail, IncomeCategorySubList, IncomeCategorySubDetail

urlpatterns = [
    path('income_category/', IncomeCategoryList.as_view()),
    path('income_category/main/', IncomeCategoryMainList.as_view()),
    path('income_category/main/<uuid:pk>/', IncomeCategoryMainDetail.as_view()),
    path('income_category/sub/', IncomeCategorySubList.as_view()),
    path('income_category/sub/<uuid:pk>', IncomeCategorySubDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
