"""
Treatment types
---------------
"""

import datetime

from .bcds1 import Treatment


class TREATMENT_CATEGORY(Treatment):
    def __init__(self, band):
        super().__init__(code=9150, instance_count=band)


TREATMENT_CATEGORY_URGENT = Treatment(code=9150, instance_count=4)
TREATMENT_CATEGORY_CONTRACT_PILOT_INTERIM_CARE_APPOINTMENT = Treatment(
    code=9150, instance_count=5
)

REGULATION_11_APPLIANCE = Treatment(code=9162)
PRESCRIPTION = Treatment(code=9158)
FREE_REPAIR_REPLACEMENT = Treatment(code=9153)
FURTHER_TREATMENT_WITHIN_TWO_MONTHS = Treatment(code=9163)
DENTURE_REPAIRS = Treatment(code=9154)
BRIDGE_REPAIRS = Treatment(code=9157)
ARREST_OF_BLEEDING = Treatment(code=9155)
REMOVAL_OF_SUTURES = Treatment(code=9155)

EXAMINATION = Treatment(code=9317)


class BRIDGES_FITTED(Treatment):
    """
    When a bridge or more than one bridge is fitted. The number provided is the
    total number of units that the bridge(s) spans (i.e. include the number of

    Adhesive bridges are provided in a similar manner and the total number of
    units includes the pontic(s) and any associated 'wings'.
    """

    def __init__(self, num_units):
        super().__init__(code=9315, instance_count=num_units)


class VENEERS_APPLIED(Treatment):
    """
    This is the number of teeth that have been provided with laboratory
    fabricated veneers in any permanent material. They may be on either the
    labial or palatal surface.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9313, instance_count=num_teeth)


class INLAYS(Treatment):
    """
    The number of teeth provided with inlays, pinlays or onlays, using
    an indirect technique and permanent material.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9313, instance_count=num_teeth)


class RECALL_INTERVAL(Treatment):
    """
        "I have given preventative advice and recommended a recall interval,
        taking into account NICE guidance, that I regard as appropriate to the
        patient's oral health."

    The number of months recommended recall period [..] between 1 - 24 should
    be provided.
    """

    def __init__(self, num_months):
        super().__init__(code=9172, instance_count=num_months)


BEST_PRACTICE_PREVENTION = Treatment(code=9173)


class FISSURE_SEALANTS(Treatment):
    """
    Provide the number of permanent teeth where sealant material has been
    applied to the pit and fissure systems as a primary preventive measure.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9303, instance_count=num_teeth)


class RADIOGRAPHS(Treatment):
    def __init__(self, num_radiographs):
        super().__init__(code=9304, instance_count=num_radiographs)


class ENDODONTIC_TREATMENT(Treatment):
    def __init__(self, num_teeth):
        super().__init__(code=9305, instance_count=num_teeth)


class PERMANENT_FILLINGS_AND_SEALANT_RESTORATIONS(Treatment):
    """
    The number of teeth (not the total number of individual restorations) that
    have been therapeutically treated by the placement of directly applied
    permanent restorations, namely:

    Permanent fillings in amalgam, composite resin, synthetic resin, glass
    ionomer, compomers, silicate or silico-phosphate materials (includes any
    acid-etch or pin retention.

    Sealant restorations involving the placement of composite resin, glass
    ionomer or compomer material.
    """

    def __init__(self, num_fillings):
        super().__init__(code=9306, instance_count=num_fillings)


class EXTRACTION(Treatment):
    """
    The number of teeth extracted should provided. This also includes surgical
    removal of a buried root, unerupted tooth, impacted tooth or exostosed
    tooth.
    """

    def __init__(self, num_extractions):
        super().__init__(code=9307, instance_count=num_extractions)


class CROWN(Treatment):
    def __init__(self, num_crowns):
        super().__init__(code=9308, instance_count=num_crowns)


class FILLED_TEETH_DECIDUOUS(Treatment):
    """
    A count of deciduous teeth where any direct or indirect restoration is
    present [..] between 0 - 20.

    Any tooth should only be counted once.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9325, instance_count=num_teeth)


SCALE_AND_POLISH = Treatment(code=9301)
FLUORIDE_VARNISH = Treatment(code=9302)


OTHER_TREATMENT = Treatment(code=9399)


# For date of acceptance prior to 1 April 2014 for England and 1 May 2014 for
# Wales. Isle of Man will continue to use this code.
class REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES_LEGACY(Treatment):
    def __init__(self):
        super().__init__(code=9316)

    def validate(self, document):
        if document["date_of_acceptance"] >= datetime.date(2014, 4, 1):
            yield "Legacy Advanced Mandatory Services used after 01/04/2014"


class REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES(Treatment):
    """
    For date of acceptance on or after 1 April 2014 for England and 1 May 2014
    for Wales (see `REFERRAL_FOR_ADVANCED_MANDATORY_SERVICES_LEGACY`).

    The treatment band for treatment should be provided under referral for
    advanced mandatory services.

    Value must be band 1, 2 or 3 presented by 01, 02 or 03. Code 9150
    (`TREATMENT_CATEGORY_CONTRACT_PILOT_INTERIM_CARE_APPOINTMENT`) must also be
    present representing the band of treatment provided by referring dentist.
    """

    def __init__(self, treatment_band):
        super().__init__(code=9319, instance_count=treatment_band)


class ANTIBIOTIC_ITEMS(Treatment):
    def __init__(self, num_prescribed):
        super().__init__(code=9318, instance_count=num_prescribed)


class DECAYED_PERMANENT(Treatment):
    """
    Permanent teeth where established caries is charted on any surface (between
    0 and 32).
    """

    def __init__(self, num_teeth):
        super().__init__(code=9320, instance_count=num_teeth)


class MISSING_PERMANENT(Treatment):
    """
    Permanent teeth charted as missing including those replaced by bridge
    pontics and dentures but excluding teeth charted as unerupted (between 0
    and 32).
    """

    def __init__(self, num_teeth):
        super().__init__(code=9321, instance_count=num_teeth)


class FILLED_PERMANENT(Treatment):
    """
    Permanent teeth charted as restored on any surface with direct restorations
    (fillings) or with indirect restorations of the following types: crowns,
    inlays, bridge retainers (between 0 and 32).
    """

    def __init__(self, num_teeth):
        super().__init__(code=9322, instance_count=num_teeth)


class DECAYED_DECIDUOUS(Treatment):
    """
    Deciduous teeth where established caries is charted on any surface (between
    0 and 20).
    """

    def __init__(self, num_teeth):
        super().__init__(code=9323, instance_count=num_teeth)


class MISSING_DECIDUOUS(Treatment):
    """
    Missing deciduous teeth, where "missing" means where a tooth has been
    extracted (between 0 and 12). ULA, ULB, URA, URB, LLA, LLB, LRA, LRB should
    be excluded from the count.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9324, instance_count=num_teeth)


class FILLED_DECIDUOUS(Treatment):
    """
    Deciduous teeth where any direct or indirect restoration is present
    extracted (between 0 and 20). Any tooth should only be counted once.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9324, instance_count=num_teeth)


class UPPER_DENTURE_ACRYLIC(Treatment):
    """
    An acrylic or resin based denture was provided (i.e. full or partial
    denture). The number of teeth present on the denture should be provided.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9309, instance_count=num_teeth)


class LOWER_DENTURE_ACRYLIC(Treatment):
    """
    An acrylic or resin based denture was provided (i.e. full or partial
    denture). The number of teeth present on the denture should be provided.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9310, instance_count=num_teeth)


class UPPER_DENTURE_METAL(Treatment):
    """
    A metal based denture was provided (i.e. full or partial denture). The
    number of teeth present on the denture should be provided.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9311, instance_count=num_teeth)


class LOWER_DENTURE_METAL(Treatment):
    """
    A metal based denture was provided (i.e. full or partial denture). The
    number of teeth present on the denture should be provided.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9312, instance_count=num_teeth)


ETHNIC_ORIGIN_1_WHITE_BRITISH = Treatment(code=9025, instance_count=1)
ETHNIC_ORIGIN_2_WHITE_IRISH = Treatment(code=9025, instance_count=2)
ETHNIC_ORIGIN_3_WHITE_OTHER = Treatment(code=9025, instance_count=3)
ETHNIC_ORIGIN_4_WHITE_AND_BLACK_CARIBBEAN = Treatment(
    code=9025, instance_count=4
)
ETHNIC_ORIGIN_5_WHITE_AND_BLACK_AFRICAN = Treatment(
    code=9025, instance_count=5
)
ETHNIC_ORIGIN_6_WHITE_AND_ASIAN = Treatment(code=9025, instance_count=6)
ETHNIC_ORIGIN_7_OTHER_MIXED_BACKGROUND = Treatment(code=9025, instance_count=7)
ETHNIC_ORIGIN_8_ASIAN_OR_ASIAN_BRITISH_INDIAN = Treatment(
    code=9025, instance_count=8
)
ETHNIC_ORIGIN_9_ASIAN_OR_ASIAN_BRITISH_PAKISTANI = Treatment(
    code=9025, instance_count=9
)
ETHNIC_ORIGIN_10_ASIAN_OR_ASIAN_BRITISH_BANGLADESHI = Treatment(
    code=9025, instance_count=10
)
ETHNIC_ORIGIN_11_OTHER_ASIAN_BACKGROUND = Treatment(
    code=9025, instance_count=11
)
ETHNIC_ORIGIN_12_BLACK_OR_BLACK_BRITISH_CARIBBEAN = Treatment(
    code=9025, instance_count=12
)
ETHNIC_ORIGIN_13_BLACK_OR_BLACK_BRITISH_AFRICAN = Treatment(
    code=9025, instance_count=13
)
ETHNIC_ORIGIN_14_OTHER_BLACK_BACKGROUND = Treatment(
    code=9025, instance_count=14
)
ETHNIC_ORIGIN_15_CHINESE = Treatment(code=9025, instance_count=15)
ETHNIC_ORIGIN_ANY_OTHER_ETHNIC_GROUP = Treatment(code=9025, instance_count=16)
ETHNIC_ORIGIN_PATIENT_DECLINED = Treatment(code=9025, instance_count=99)

# "Part 6 Other Services"
DOMICILIARY_SERVICES = Treatment(code=9152)
SEDATION_SERVICES = Treatment(code=9166)
