from flask import redirect, request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask_wtf.form import Form
from wtforms.fields import PasswordField, TextAreaField
from wtforms.validators import Required

from {{cookiecutter.app_name}}.user.models import Role, User


class SecureMixin:
    """Abstracted security methods for easy application to Flask-Admin views."""
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("public.home", next=request.url))


class TinyMCEditorMixin:
    """Injects TinyMCE js files to convert any textarea fields into editors."""
    def render(self, template, **kwargs):
        """Override render to provide url_for-built urls to extra_js
        Source: https://stackoverflow.com/a/50965247/2962937"""
        self.extra_js = [  # noqa
            url_for("static", filename="js/tinymce.min.js"),
            url_for("static", filename="js/tinymce_instance.js")
        ]
        return super().render(template, **kwargs)


class SecureAdminIndexView(SecureMixin, AdminIndexView):
    pass


class SecureFileAdmin(SecureMixin, FileAdmin):
    # flask_wtf.form.Form used to prevent auto-csrf-validation on POSTs
    # see: https://github.com/flask-admin/flask-admin/issues/366#issuecomment-28130576
    form_base_class = Form
    allowed_extensions = ("jpg", "jpeg", "gif", "png")


class SecureModelView(ModelView):
    pass


class UserView(SecureModelView):
    column_exclude_list = ("_password",)
    form_columns = (
        "username",
        "email",
        "new_password",
        "first_name",
        "last_name",
        "active",
        "is_admin",
    )
    form_extra_fields = {"new_password": PasswordField("Password")}
    inline_models = (Role,)
    can_export = True

    def create_form(self, obj=None):
        form = super().create_form(obj=obj)
        if obj is None:
            # require password when creating a new user
            form.new_password.validators = [Required()]
        return form

    def on_model_change(self, form, user, is_created):
        if form.new_password.data:
            # trigger password.setter to properly encrypt new password
            user.password = form.new_password.data
        elif is_created is False:
            # updating a model whose password hasn't been changed
            del form.new_password


"""
class SamplePostView(TinyMCEditorMixin, SecureModelView):
    form_columns = ("title", "body", "tags")
    form_overrides = {"body": TextAreaField}
"""
