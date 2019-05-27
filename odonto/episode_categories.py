from opal.core import episodes


class DentalCareEpisodeCategory(episodes.EpisodeCategory):
    display_name = "Dental Care"
    detail_template = "detail/dental_care.html"


class FP17Episode(episodes.EpisodeCategory):
    display_name = 'FP17'
    detail_template = 'n/a'


class FP17OEpisode(episodes.EpisodeCategory):
    display_name = 'FP17O'
    detail_template = 'n/a'
