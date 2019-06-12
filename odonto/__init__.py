"""
odonto - Our Opal Application
"""
from opal.core import application, menus
from odonto import episode_categories


class Application(application.OpalApplication):
    default_episode_category = episode_categories.DentalCareEpisodeCategory.display_name

    javascripts = [
        'js/openodonto/routes.js',
        'js/opal/controllers/discharge.js',
        'js/openodonto/controllers/careprovider.step.controller.js',
        'js/openodonto/controllers/fp17treatment.step.controller.js',
        'js/openodonto/controllers/complete_fp17_other_dental_services.controller.step.js',
        'js/openodonto/controllers/display_summary.step.controller.js',
        'js/openodonto/controllers/summary.controller.js',
        'js/openodonto/services/validators/exemptions_and_remissions.js',
    ]
