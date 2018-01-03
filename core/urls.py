from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from core.views.saifu import SaifuCategoryViewSet, SaifuViewSet
from core.views.credit import CreditCategoryViewSet
from core.views.income import IncomeCategoryViewSet, IncomeViewSet
from core.views.expense import ExpenseCategoryViewSet, ExpenseViewSet
from core.views.transfer import TransferBetweenSaifuViewSet

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
router.register(r'saifu_category', SaifuCategoryViewSet)
router.register(r'saifu', SaifuViewSet, base_name='saifu')
router.register(r'income_category', IncomeCategoryViewSet)
router.register(r'income', IncomeViewSet, base_name='income')
router.register(r'expense_category', ExpenseCategoryViewSet)
router.register(r'expense', ExpenseViewSet, base_name='expense')
router.register(r'credit_category', CreditCategoryViewSet)
router.register(r'transfer_between_saifu', TransferBetweenSaifuViewSet, base_name='transfer_between_saifu')
urlpatterns += router.urls
