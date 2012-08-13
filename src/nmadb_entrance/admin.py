from django.contrib import admin
from django.utils.translation import ugettext as _

from nmadb_entrance import models
from nmadb_utils import admin as utils
from nmadb_utils import actions


class BaseInfoAdmin(utils.ModelAdmin):
    """ Administration for base info.
    """

    list_display = (
            'id',
            'first_name',
            'last_name',
            'school',
            'email',
            'section',
            'school_class',
            'generated_address',
            )

    list_filter = (
            'section',
            'school_class',
            )

    search_fields = (
            'id',
            'uuid',
            'first_name',
            'last_name',
            'school__title',
            )


class PDFFileAdmin(utils.ModelAdmin):
    """ Administration for PDF files.
    """

    list_display = (
            'id',
            'base_info',
            'file_type',
            )

    list_filter = (
            'file_type',
            )

    search_fields = (
            'id',
            'base_info__uuid',
            'base_info__first_name',
            'base_info__last_name',
            )


admin.site.register(models.BaseInfo, BaseInfoAdmin)
admin.site.register(models.PDFFile, PDFFileAdmin)
