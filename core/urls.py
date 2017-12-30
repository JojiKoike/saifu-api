from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_swagger.views import get_swagger_view
from core.views.income import IncomeCategoryList, IncomeCategoryMainList, IncomeCategoryMainDetail, \
    IncomeCategorySubList, IncomeCategorySubDetail, IncomeList
from core.views.saifu import SaifuCategoryList, SaifuCategoryDetail, SaifuList, SaifuDetail
from core.views.credit import CreditCategoryList, \
    CreditCategoryMainList, CreditCategoryMainDetail, CreditCategorySubList, CreditCategorySubDetail
from core.views.expense import ExpenseCategoryList, ExpenseCategoryMainList, ExpenseCategoryMainDetail, \
    ExpenseCategorySubList, ExpenseCategorySubDetail, ExpenseList
from core.views.transfer import TransferBetweenSaifuList

schema_view = get_swagger_view(title='Saifu Core API')

urlpatterns = [
    path('', schema_view),
    re_path('income/', IncomeList.as_view()),
    re_path('income_category/main/', IncomeCategoryMainList.as_view()),
    re_path('income_category/main/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            IncomeCategoryMainDetail.as_view()),
    re_path('income_category/sub/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            IncomeCategorySubDetail.as_view()),
    re_path('income_category/sub/', IncomeCategorySubList.as_view()),
    re_path('income_category/', IncomeCategoryList.as_view()),
    re_path('expense/', ExpenseList.as_view()),
    re_path('expense_category/main/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            ExpenseCategoryMainDetail.as_view()),
    re_path('expense_category/main/', ExpenseCategoryMainList.as_view()),
    re_path('expense_category/sub/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            ExpenseCategorySubDetail.as_view()),
    re_path('expense_category/sub/', ExpenseCategorySubList.as_view()),
    re_path('expense_category/', ExpenseCategoryList.as_view()),
    re_path('saifu_category/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            SaifuCategoryDetail.as_view()),
    re_path('credit_category/', CreditCategoryList.as_view()),
    re_path('credit_category/main/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            CreditCategoryMainDetail.as_view()),
    re_path('credit_category/main/', CreditCategoryMainList.as_view()),
    re_path('credit_category/sub/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            CreditCategorySubDetail.as_view()),
    re_path('credit_category/sub/', CreditCategorySubList.as_view()),
    re_path('saifu_category/', SaifuCategoryList.as_view()),
    re_path('saifu/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/', SaifuDetail.as_view()),
    re_path('saifu/', SaifuList.as_view()),
    re_path('transfer_between_saifu/', TransferBetweenSaifuList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
