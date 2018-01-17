from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from rest_framework.routers import DefaultRouter
from core.views.saifu import SaifuCategoryViewSet, SaifuViewSet
from core.views.credit import CreditCategoryViewSet
from core.views.income import IncomeCategoryViewSet, IncomeViewSet
from core.views.expense import ExpenseCategoryViewSet, ExpenseViewSet
from core.views.transfer import TransferBetweenSaifuViewSet, \
    TransferBetweenSaifuAndAssetViewSet, TransferBetweenSaifuAndDebtViewSet
from core.views.asset import AssetCategoryViewSet, AssetViewSet, AssetEvaluateViewSet
from core.views.debt import DebtCategoryViewSet, DebtViewSet, DebtGainViewSet

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
router.register(r'transfer_between_saifu', TransferBetweenSaifuViewSet,
                base_name='transfer_between_saifu')
router.register(r'transfer_between_saifu_and_asset', TransferBetweenSaifuAndAssetViewSet,
                base_name='transfer_between_saifu_and_asset')
router.register(r'transfer_between_saifu_and_debt', TransferBetweenSaifuAndDebtViewSet,
                base_name='transfer_between_saifu_and_debt')
router.register(r'asset', AssetViewSet, base_name='asset')
router.register(r'asset_category', AssetCategoryViewSet)
router.register(r'asset_evaluate', AssetEvaluateViewSet, base_name='asset_evaluate')
router.register(r'debt', DebtViewSet, base_name='debt')
router.register(r'debt_category', DebtCategoryViewSet)
router.register(r'debt_gain', DebtGainViewSet, base_name='debt_gain')
urlpatterns += router.urls
