from django.contrib import admin

from .models import Entry, Screenshot, Vote

class EntryAdmin(admin.ModelAdmin):

    pass


class ScreenshotAdmin(admin.ModelAdmin):

    pass


class VoteAdmin(admin.ModelAdmin):

    pass

admin.site.register(Entry, EntryAdmin)
admin.site.register(Screenshot, ScreenshotAdmin)
admin.site.register(Vote, VoteAdmin)
