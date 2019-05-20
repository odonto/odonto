"""
Odonto utilities
"""
def has_open_fp17(patient):
    return patient.episode_set.exclude(
        stage='New').exclude(stage='Submitted'
        ).exclude(stage='Open Orthodontic').count() > 0

def has_open_fp17o(patient):
    return patient.episode_set.filter(
        stage='Open Orthodontic').count() > 0
