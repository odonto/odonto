from .bcds1 import Treatment


TREATMENT_CATEGORY_BAND_1 = Treatment(code=9150, instance_count=1)
TREATMENT_CATEGORY_BAND_2 = Treatment(code=9150, instance_count=2)
TREATMENT_CATEGORY_BAND_3 = Treatment(code=9150, instance_count=3)
TREATMENT_CATEGORY_URGENT_TREATMENT = Treatment(code=9150, instance_count=4)
TREATMENT_CATEGORY_CONTRACT_PILOT_INTERIM_CARE_APPOINTMENT = \
    Treatment(code=9150, instance_count=5)

EXAMINATION = Treatment(code=9317)

class RECALL_INTERVAL(Treatment):
    """
    The number of months recommended recall period [..] between 1 - 24.
    """

    def __init__(self, months):
        super().__init__(code=9172, instance_count=months)

SCALE_AND_POLISH = Treatment(code=9301)

ETHNIC_ORIGIN_WHITE_BRITISH = Treatment(code=9025, instance_count=1)
ETHNIC_ORIGIN_WHITE_IRISH = Treatment(code=9025, instance_count=2)
ETHNIC_ORIGIN_WHITE_OTHER = Treatment(code=9025, instance_count=3)
ETHNIC_ORIGIN_WHITE_AND_BLACK_CARIBBEAN = Treatment(code=9025, instance_count=4)
ETHNIC_ORIGIN_WHITE_AND_BLACK_AFRICAN = Treatment(code=9025, instance_count=5)
ETHNIC_ORIGIN_WHITE_AND_ASIAN = Treatment(code=9025, instance_count=6)
ETHNIC_ORIGIN_OTHER_MIXED_BACKGROUND = Treatment(code=9025, instance_count=7)
ETHNIC_ORIGIN_ASIAN_OR_ASIAN_BRITISH_INDIAN = Treatment(code=9025, instance_count=8)
ETHNIC_ORIGIN_ASIAN_OR_ASIAN_BRITISH_PAKISTANI = Treatment(code=9025, instance_count=9)
ETHNIC_ORIGIN_ASIAN_OR_ASIAN_BRITISH_BANGLADESHI = Treatment(code=9025, instance_count=10)
ETHNIC_ORIGIN_OTHER_ASIAN_BACKGROUND = Treatment(code=9025, instance_count=11)
ETHNIC_ORIGIN_BLACK_OR_BLACK_BRITISH_CARIBBEAN = Treatment(code=9025, instance_count=12)
ETHNIC_ORIGIN_BLACK_OR_BLACK_BRITISH_AFRICAN = Treatment(code=9025, instance_count=13)
ETHNIC_ORIGIN_OTHER_BLACK_BACKGROUND = Treatment(code=9025, instance_count=14)
ETHNIC_ORIGIN_CHINESE = Treatment(code=9025, instance_count=15)
ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP = Treatment(code=9025, instance_count=16)
ETHNIC_ORIGIN_PATIENT_DECLINED = Treatment(code=9025, instance_count=99)
