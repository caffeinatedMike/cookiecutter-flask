from flask import redirect, request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField
from wtforms.validators import Required

from {{cookiecutter.app_name}}.user.models import Role, User


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("public.home", next=request.url))


class UserView(ModelView):
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


class UploadView(FileAdmin):
    allowed_extensions = ("jpg", "jpeg", "gif", "png")
