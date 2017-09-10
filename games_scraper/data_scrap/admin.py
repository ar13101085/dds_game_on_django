from django.contrib import admin

# Register your models here.
from data_scrap.models import Game, Genre, GameUser, Play, Review

admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(GameUser)
admin.site.register(Play)
admin.site.register(Review)
