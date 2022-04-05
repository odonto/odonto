"""
Treatment types
---------------
"""

import datetime

from .bcds1 import Treatment


class FLEXIBLE_COMMISSIONING_FLAG(Treatment):
    def __init__(self, commissioning_flag):
        super().__init__(code=9181, instance_count=commissioning_flag)


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
REMOVAL_OF_SUTURES = Treatment(code=9156)

EXAMINATION = Treatment(code=9317)


class INCOMPLETE_TREATMENT(Treatment):
    """
    Charge Band for actual treatment provided
    """
    def __init__(self, num_units):
        super().__init__(code=9164, instance_count=num_units)


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
        super().__init__(code=9314, instance_count=num_teeth)


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

# Delivering Better Oral Health (DBOH),
# clarification that DBOH should only be entered by the dental practice
# when this has been provided to the patient, and that this must be a
# manual entry and must not be pre-populated.
BEST_PRACTICE_PREVENTION = Treatment(code=9173)


class FISSURE_SEALANTS(Treatment):
    """
    Provide the number of permanent teeth where sealant material has been
    applied to the pit and fissure systems as a primary preventive measure.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9303, instance_count=num_teeth)

class TREATMENT_TYPE(Treatment):
    """
    Treatment Type
    instance count `1` for Proposed
    incstance count `2` for Completed / Abandoned / Discontinued Treatment
    """
    def __init__(self, instance_count):
        super().__init__(code=9415, instance_count=instance_count)

PROPOSED_TREATMENT = TREATMENT_TYPE(instance_count=1)
COMPLETED_TREATMENT = TREATMENT_TYPE(instance_count=2)

class RADIOGRAPHS(Treatment):
    def __init__(self, num_radiographs):
        super().__init__(code=9304, instance_count=num_radiographs)


class ENDODONTIC_TREATMENT(Treatment):
    def __init__(self, num_teeth):
        super().__init__(code=9305, instance_count=num_teeth)


class PERMANENT_FILLINGS(Treatment):
    """
    The number of teeth (not the total number of individual restorations) that
    have been therapeutically treated by the placement of directly applied
    permanent restorations, namely:

    Permanent fillings in amalgam, composite resin, synthetic resin, glass
    ionomer, compomers, silicate or silico-phosphate materials (includes any
    acid-etch or pin retention.
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

CUSTOM_MADE_OCCLUSAL_APPLIANCE_HARD_BITE = Treatment(code=9376)
CUSTOM_MADE_OCCLUSAL_APPLIANCE_SOFT_BITE = Treatment(code=9377)
DENTURE_ADDITIONS_RELINE_REBASE = Treatment(code=9353)
PHASED_TREATMENT = Treatment(code=9375)


class ADVANCED_PERIO_ROOT_SURFACE_DEBRIDEMENT(Treatment):
    """
    If present, the code must be accompanied by a quantity of 1-6 (number of sextants)
    """
    def __init__(self, sextants):
        super().__init__(code=9325, instance_count=sextants)


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


class PREFORMED_CROWNS(Treatment):
    """
    If present, the code must be accompanied by a
    quantity representing the number of teeth.
    """

    def __init__(self, num_teeth):
        super().__init__(code=9338, instance_count=num_teeth)


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

EMAIL_DECLINED = Treatment(code=9175)
PHONE_NUMBER_DECLINED = Treatment(code=9176)

# "Part 6 Other Services"
DOMICILIARY_SERVICES = Treatment(code=9152)
SEDATION_SERVICES = Treatment(code=9166)


# FP17O exclusive treatments


# Orthodontic Data Set
COMMISSIONER_APPROVAL = Treatment(code=9177)
REMOVABLE_UPPER_APPLIANCE = Treatment(code=9401)
REMOVABLE_LOWER_APPLIANCE = Treatment(code=9402)
FUNCTIONAL_APPLIANCE = Treatment(code=9403)
FIXED_UPPER_APPLIANCE = Treatment(code=9404)
FIXED_LOWER_APPLIANCE = Treatment(code=9405)
RETAINER_UPPER = Treatment(code=9406)
RETAINER_LOWER = Treatment(code=9407)


class ORTHODONTIC_EXTRACTIONS(Treatment):
    """
    Code plus tooth notation.
    Two digit code used to specify unique tooth.
    1st digit – quadrant clockwise from upper right 1-4 for permanent teeth
    and 5-8 for deciduous teeth
    2nd digit – tooth in quadrant counting out from midline 1-8 for permanent
    teeth, 1-5 for deciduous teeth.
    Supernumerary teeth identified as 9
    Enter the tooth notation(s) for extractions proposed/performed.
    """

    def __init__(self, teeth_quadrant):
        super().__init__(code=9408, teeth=teeth_quadrant)


# Orthodontic Assessment
ASSESS_AND_REVIEW = Treatment(code=9012)
ASSESS_AND_REFUSE = Treatment(code=9013)
ASSESS_AND_APPLIANCE_FITTED = Treatment(code=9014)


class IOTN(Treatment):
    """
    Numeric value 00-05
    Can occur with Assess and Review, Assess and Refuse or Assess and
    Appliance Fitted
    If a value of 03 is present then the aesthetic component (9165)
    with a numeric value 01-10 must be present

    A valid IOTN score is between 01-05.

    If ‘IOTN not applicable’ (e.g not possible to calculate because the
    patient has transferred mid treatment to a new Provider contract)
    a value of 0 (zero) should be entered

    Must be present on both assessment forms and the completion of active
    treatment
    """
    def __init__(self, iotn):
        super().__init__(code=9015, instance_count=iotn)


class AESTHETIC_COMPONENT(Treatment):
    """
    Numeric value 01-10

    Can occur with Assess and Review,
    Assess and Refuse or Assess and Appliance Fitted

    Must be present if IOTN (9015) value is 03
    """
    def __init__(self, numeric_value):
        super().__init__(code=9165, instance_count=numeric_value)


# Date of referral is weirdly multiple field
# Assess and Review, Assess and Refuse or Assess and Appliance
# Fitted must be present
# 9017 Numeric value 01-31
# 9018 Numeric value 01-12
# 9019 Numeric value 00-99
# Ignored if entered on a final ortho claim
# Must be on or before the Date of Assessment
# Cannot be a future date
class DAY_OF_REFERRAL(Treatment):
    def __init__(self, day_num):
        super().__init__(code=9017, instance_count=day_num)


class MONTH_OF_REFERRAL(Treatment):
    def __init__(self, month_num):
        super().__init__(code=9018, instance_count=month_num)


class YEAR_OF_REFERRAL(Treatment):
    def __init__(self, year_num):
        super().__init__(code=9019, instance_count=year_num)


# Assess and Appliance Fitted and Date of assessment must be present
# 9169 Numeric value 01-31
# 9170 Numeric value 01-12
# 9171 Numeric value 00-99
# The Date Appliance Fitted must be on or after the Date of Assessment.
# Cannot be a future date
class DAY_APPLIANCE_FITTED(Treatment):
    def __init__(self, day_num):
        super().__init__(code=9169, instance_count=day_num)


class MONTH_APPLIANCE_FITTED(Treatment):
    def __init__(self, month_num):
        super().__init__(code=9170, instance_count=month_num)


class YEAR_APPLIANCE_FITTED(Treatment):
    def __init__(self, year_num):
        super().__init__(code=9171, instance_count=year_num)


# Orthodontic Completion
TREATMENT_ABANDONED = Treatment(
    code=9161, instance_count=1
)

# the 2 reasons for treatment being abandoned
PATIENT_FAILED_TO_RETURN = Treatment(code=9409)
PATIENT_REQUESTED = Treatment(code=9410)


TREATMENT_DISCONTINUED = Treatment(
    code=9161, instance_count=2
)

TREATMENT_COMPLETED = Treatment(
    code=9161, instance_count=3
)

PAR_SCORES_CALCULATED = Treatment(
    code=9411
)


REPAIR_TO_APPLIANCE_FITTED_BY_ANOTHER_DENTIST = Treatment(code=9159)
REGULATION_11_REPLACEMENT_APPLIANCE = Treatment(code=9167)


# With effect from 1 July 2020, NHSE&I are introducing a change to include an
# additional CDS data item provided as an additional number box
# (new CDS data item code 9340 plus number).
# The new AGP field is to record the number of AGP appointments provided as part
# of the course of treatment.
#
# For example, a patient has 3 fillings and a crown and AGP is used at two of the
# appointments so the value submitted will be <reptrtty trtcd="9340" noins="02" />
class AEROSOL_GENERATING_PROCEDURE(Treatment):
    def __init__(self, day_num):
        super().__init__(code=9340, instance_count=day_num)


# Covid status
class SHIELDING_PATIENT(Treatment):
    # Number of calls to a patient who are shielding
    # from COVID
    def __init__(self, call_count):
        super().__init__(code=9615, instance_count=call_count)


class INCREASED_RISK(Treatment):
    # Number of calls to a
    # patient at increased risk of COVID
    def __init__(self, call_count):
        super().__init__(code=9616, instance_count=call_count)


class POSSIBLE_COVID(Treatment):
    # Number of calls to a possible/confirmed COVID-19 patient
    # or to an individual in the same household as a
    # possible/confirmed COVID-19 patient
    def __init__(self, call_count):
        super().__init__(code=9617, instance_count=call_count)


class SYMPTOM_FREE(Treatment):
    # calls to a patient who is COVID-19 symptom free at present
    def __init__(self, call_count):
        super().__init__(code=9618, instance_count=call_count)


class OTHER_COVID_STATUS(Treatment):
    # calls to a patient that has a different covid status
    def __init__(self, call_count):
        super().__init__(code=9619, instance_count=call_count)
# end covid status treatments


# covid triage treatments
DENTAL_CARE_PROFESSIONAL = Treatment(code=9600)
TRIAGE_VIA_VIDEO = Treatment(code=9601)
ADVICE_GIVEN = Treatment(code=9602)
ADVISED_ANALGESICS = Treatment(code=9603)
REMOTE_PRESCRIPTION_ANALGESICS = Treatment(code=9604)
REMOTE_PRESCRIPTION_ANTIBIOTICS = Treatment(code=9605)
FOLLOW_UP_CALL_REQUIRED = Treatment(code=9606)
CALL_BACK_IF_SYMPTOMS_WORSEN = Treatment(code=9607)


class REFERRERED_TO_LOCAL_UDC_REASON(Treatment):
    def __init__(self, reason_code):
        super().__init__(code=9609, instance_count=reason_code)


class PATIENT_GROUP(Treatment):
    # On the model this is the covid_status field
    def __init__(self, status_code):
        super().__init__(code=9610, instance_count=status_code)


class PRIMARY_REASON(Treatment):
    def __init__(self, reason_code):
        super().__init__(code=9611, instance_count=reason_code)


class HOUR_OF_CONTACT(Treatment):
    def __init__(self, hour_number):
        # hour number is 24 hour
        super().__init__(code=9612, instance_count=hour_number)


class MINUTE_OF_CONTACT(Treatment):
    # the time the call ended
    def __init__(self, minute_number):
        super().__init__(code=9613, instance_count=minute_number)


FACE_TO_FACE_ARRANGED_BUT_NOT_ATTENDED = Treatment(code=9614)


COVID_19_TREATMENT_CATEGORY = Treatment(code=9150, instance_count=6)
# end covid triage treatments
