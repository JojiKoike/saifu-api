from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from core.views.saifu import SaifuCategoryViewSet, SaifuViewSet
from core.views.credit import CreditCategoryViewSet, \
    CreditCategoryMainViewSet, CreditCategorySubViewSet
from core.views.expense import ExpenseCategoryViewSet, \
    ExpenseCategoryMainViewSet, ExpenseCategorySubViewSet, ExpenseViewSet

"""
Swagger url configuration
"""
schema_view = get_swagger_view(title='Saifu Core API')

urlpatterns = [
    path('', schema_view),
]

"""
Saifu core api url configuration
"""
router = DefaultRouter()
router.register(r'saifu_categories', SaifuCategoryViewSet)
router.register(r'saifu', SaifuViewSet, base_name='saifu')
router.register(r'credit_categories', CreditCategoryViewSet)
router.register(r'credit_category_main', CreditCategoryMainViewSet)
router.register(r'credit_category_sub', CreditCategorySubViewSet)
router.register(r'expense_categories', ExpenseCategoryViewSet)
router.register(r'expense_category_main', ExpenseCategoryMainViewSet)
router.register(r'expense_category_sub', ExpenseCategorySubViewSet)
router.register(r'expense', ExpenseViewSet, base_name='expense')
urlpatterns += router.urls

"""
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
    #re_path('saifu_category/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
    #        SaifuCategoryDetail.as_view()),
    # re_path('saifu_category/', SaifuCategoryList.as_view()),
    re_path('credit_category/', CreditCategoryList.as_view()),
    re_path('credit_category/main/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            CreditCategoryMainDetail.as_view()),
    re_path('credit_category/main/', CreditCategoryMainList.as_view()),
    re_path('credit_category/sub/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/',
            CreditCategorySubDetail.as_view()),
    re_path('credit_category/sub/', CreditCategorySubList.as_view()),
    re_path('saifu/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/', SaifuDetail.as_view()),
    re_path('saifu/', SaifuList.as_view()),
    re_path('transfer_between_saifu/', TransferBetweenSaifuList.as_view())
]
"""
