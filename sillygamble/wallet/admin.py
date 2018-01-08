from django.contrib import admin

# Register your models here.
from .models import Wallet, Transaction
from .services.wallet import WalletImportTransaction

# Register your models here.
# class DepositInline(admin.TabularInline):
#     model = Deposit
#     extra = 0

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0

def import_transactions(modeladmin, request, queryset):
    importTransctions = WalletImportTransaction(request, queryset)
    importTransctions.run()
import_transactions.short_description = "Import new transactions"

class WalletAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'active', 'created_at']
    list_filter = ['active', 'created_at']
    search_fields = ['wallet_id', 'label']

    inlines = [
        TransactionInline,
    ]

    actions = [import_transactions]

class DepositAdmin(admin.ModelAdmin):
    list_display = ['deposit_id', 'from_wallet', 'to_wallet', 'bitcoin_amount', 'spent', 'created_at']
    list_filter = ['spent', 'created_at']
    search_fields = ['deposit_id', 'from_wallet', 'to_wallet']

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'from_wallet', 'to_wallet', 'amount_out', 'amount', 'created_at']
    list_filter = ['spent', 'created_at']
    search_fields = ['__str__', 'transaction_id', 'from_wallet', 'to_wallet']

admin.site.register(Wallet, WalletAdmin)
# admin.site.register(Deposit, DepositAdmin)
admin.site.register(Transaction, TransactionAdmin)