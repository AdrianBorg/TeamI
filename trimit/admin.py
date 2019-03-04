from django.contrib import admin
from trimit.models import Page, UserProfile, Review, PageImage, UserHairImage#, EUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(PageImage)
admin.site.register(UserHairImage)

admin.site.unregister(User)


class MyUserAdmin(UserAdmin):

    def group(self, user):
        groups = []
        for group in user.groups.all():
            if group.name == 'hairdressers':
                return 'hairdresser'
            if group.name == 'users':
                return 'user'
        #     groups.append(group.name)
        # return ' '.join(groups)

    group.short_description = 'Account Type'

    list_display = ('username', 'email', 'group', 'is_staff')


admin.site.register(User, MyUserAdmin)



# class EUserChangeForm(UserChangeForm):
#     class Meta(UserChangeForm.Meta):
#         model = EUser
#
#
# class EUserAdmin(UserAdmin):
#     model = EUser
#     form = EUserChangeForm
#
#     fieldsets = UserAdmin.fieldsets + (
#             (None, {'fields': ('email',)}),
#     )
#
#
# admin.site.register(EUser, EUserAdmin)