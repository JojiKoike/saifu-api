from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from core.views.income import IncomeCategoryList, IncomeCategoryMainList, IncomeCategoryMainDetail, \
    IncomeCategorySubList, IncomeCategorySubDetail, IncomeList
from core.views.saifu import SaifuCategoryList, SaifuCategoryDetail, SaifuList, SaifuDetail
from core.views.credit import CreditCategoryList, \
    CreditCategoryMainList, CreditCategoryMainDetail, CreditCategorySubList, CreditCategorySubDetail
from core.views.expense import ExpenseCategoryList, ExpenseCategoryMainList, ExpenseCategoryMainDetail, \
    ExpenseCategorySubList, ExpenseCategorySubDetail, ExpenseList

schema_view = get_swagger_view(title='Saifu Core API')

urlpatterns = [
    path('', schema_view),
    path('income', IncomeList.as_view()),
    path('income_category/', IncomeCategoryList.as_view()),
    path('income_category/main/', IncomeCategoryMainList.as_view()),
    path('income_category/main/<uuid:pk>/', IncomeCategoryMainDetail.as_view()),
    path('income_category/sub/', IncomeCategorySubList.as_view()),
    path('income_category/sub/<uuid:pk>', IncomeCategorySubDetail.as_view()),
    path('saifu_category/', SaifuCategoryList.as_view()),
    path('saifu_category/<uuid:pk>', SaifuCategoryDetail.as_view()),
    path('saifu/', SaifuList.as_view()),
    path('saifu/<uuid:pk>', SaifuDetail.as_view()),
    path('credit_category/', CreditCategoryList.as_view()),
    path('credit_category/main/', CreditCategoryMainList.as_view()),
    path('credit_category/main/<uuid:pk>', CreditCategoryMainDetail.as_view()),
    path('credit_category/sub/', CreditCategorySubList.as_view()),
    path('credit_category/sub/<uuid:pk>', CreditCategorySubDetail.as_view()),
    path('expense/', ExpenseList.as_view()),
    path('expense_category/', ExpenseCategoryList.as_view()),
    path('expense_category/main/', ExpenseCategoryMainList.as_view()),
    path('expense_category/main/<uuid:pk>/', ExpenseCategoryMainDetail.as_view()),
    path('expense_category/sub/', ExpenseCategorySubList.as_view()),
    path('expense_category/sub/<uuid:pk>/', ExpenseCategorySubDetail.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
