from django.contrib import admin

from .models import Game, GameCard

# Register your models here.
class GameCardInline(admin.TabularInline):
    model = GameCard
    extra = 0

class GameAdmin(admin.ModelAdmin):
    list_display = ['game_id', 'wallet_number', 'bitcoin_amount', 'winner', 'test', 'created_at']
    list_filter = ['winner', 'test', 'created_at']
    search_fields = ['game_id','wallet_number']

    inlines = [
        GameCardInline,
    ]

admin.site.register(Game, GameAdmin)