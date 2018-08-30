"""
Plugin definition for the odontotheme Opal plugin
"""
from opal.core import plugins

from odontotheme.urls import urlpatterns


class OdontothemePlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to our Opal application.
    """
    urls = urlpatterns
    javascripts = {
        # Add your javascripts here!
        'opal.odontotheme': [
            # 'js/odontotheme/app.js',
            # 'js/odontotheme/controllers/larry.js',
            # 'js/odontotheme/services/larry.js',
        ]
    }
    stylesheets = [
        "css/odonto.css"
    ]
