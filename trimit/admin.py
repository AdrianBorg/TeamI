from django.contrib import admin
from trimit.models import Page, UserProfile, Review, PageImage, UserHairImage, EUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

# Register your models here.
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(PageImage)
admin.site.register(UserHairImage)


class EUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = EUser


class EUserAdmin(UserAdmin):
    model = EUser
    form = EUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('email',)}),
    )


admin.site.register(EUser, EUserAdmin)