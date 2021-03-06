# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging
import sys
import os

from flask import Flask, render_template

from {{cookiecutter.app_name}} import commands, public, user
from {{cookiecutter.app_name}}.extensions import (
    admin,
    bcrypt,
    cache,
    csrf_protect,
    db,
    debug_toolbar,
    login_manager,
    migrate,
)
from {{cookiecutter.app_name}}.admin.views import (
    SecureAdminIndexView,
    SecureFileAdmin,
    UserView,
)


def create_app(config_object="{{cookiecutter.app_name}}.settings"):
    """Create application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split(".")[0])
    app.config.from_object(config_object)
    register_extensions(app)
    register_admin_components()
    register_blueprints(app)
    register_errorhandlers(app)
    register_shellcontext(app)
    register_commands(app)
    configure_logger(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    admin.init_app(app, index_view=SecureAdminIndexView())
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_admin_components():
    uploads_folder = os.path.join(os.path.dirname(__file__), "static", "uploads")
    if not os.path.exists(uploads_folder):
        os.mkdir(uploads_folder)
    admin.add_view(UserView(User, db.session, name="Users", endpoint="users"))
    admin.add_view(SecureFileAdmin(uploads_folder, name="Uploads", endpoint="uploads"))


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, "code", 500)
        return render_template(f"{error_code}.html"), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"db": db, "User": user.models.User}

    app.shell_context_processor(shell_context)


def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.create_admin)
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.lint)


def configure_logger(app):
    """Configure loggers."""
    handler = logging.StreamHandler(sys.stdout)
    if not app.logger.handlers:
        app.logger.addHandler(handler)
