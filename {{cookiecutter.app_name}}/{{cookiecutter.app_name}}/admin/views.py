from flask import redirect, request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from {{cookiecutter.app_name}}.extensions import admin, db
from {{cookiecutter.app_name}}.user.models import User, Role


class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for("public.home", next=request.url))


class UserView(ModelView):
    can_export = True
    column_exclude_list = ["_password", ]
    inline_models = [Role, ]


admin.add_view(UserView(User, db.session))
