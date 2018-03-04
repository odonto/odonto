"""
odonto - Our Opal Application
"""
from opal.core import application, menus
from odonto import episode_categories


class Application(application.OpalApplication):
    default_episode_category = episode_categories.DentalCareEpisodeCategory.display_name

    javascripts  = [
        'js/openodonto/routes.js',
        'js/opal/controllers/discharge.js',
        # Uncomment this if you want to implement custom dynamic flows.
        # 'js/openodonto/flow.js',
    ]

    @classmethod
    def get_menu_items(cls, user=None):
        from odonto import pathways
        menu_items = [
            pathways.AddPatientPathway.as_menuitem()
        ]
        return menu_items
