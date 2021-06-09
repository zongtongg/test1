from django.utils.html import format_html


def get_mptt_indented_menu(cls, mtpp_model_admin):
    return format_html(
        '<div style="text-indent:{}px">{}</div>',
        mtpp_model_admin._mpttfield('level') * cls.mptt_level_indent,
        mtpp_model_admin.name,
    )
