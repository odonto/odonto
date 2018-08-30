"""
Constants for "Part 4 Exemptions and remissions"
------------------------------------------------
"""


class PATIENT_UNDER_18(object):
    """
    Patient under 18 at start of treatment.
    """

    NO_EVIDENCE_SEEN = 27
    EVIDENCE_SEEN = 28


class FULL_REMISSION(object):
    """
    Patient or partner is named on a current HC2 NHS charges certificate.
    """

    NO_EVIDENCE_SEEN = 13
    EVIDENCE_SEEN = 14


class PARTIAL_REMISSION(object):
    """
    Patient or partner is named on a current HC3 NHS charges certificate.
    """

    NO_EVIDENCE_SEEN = 15
    EVIDENCE_SEEN = 16


class EXPECTANT_MOTHER(object):
    """
    Patient is pregnant.
    """

    NO_EVIDENCE_SEEN = 3
    EVIDENCE_SEEN = 4


class NURSING_MOTHER(object):
    """
    Patient had a baby in the last 12 months.
    """

    NO_EVIDENCE_SEEN = 5
    EVIDENCE_SEEN = 6


class AGED_18_IN_FULL_TIME_EDUCATION(object):
    """
    Patient aged 18 and under 19 in full time education.
    """

    NO_EVIDENCE_SEEN = 1
    EVIDENCE_SEEN = 2


class INCOME_SUPPORT(object):
    """
    Patient or partner receive income support.
    """

    NO_EVIDENCE_SEEN = 17
    EVIDENCE_SEEN = 18


class JOBSEEKERS_ALLOWANCE(object):
    """
    Patient or partner receive income-based job seeker's allowance.
    """

    NO_EVIDENCE_SEEN = 25
    EVIDENCE_SEEN = 26


class PENSION_CREDIT_GUARANTEE_CREDIT(object):
    """
    Patient or partner receive Pension Credit guarantee credit.
    """

    NO_EVIDENCE_SEEN = 33
    EVIDENCE_SEEN = 34


# Patient is currently in prison or a young offender's insitution
PRISONER = 35


class INCOME_RELATED_EMPLOYMENT_AND_SUPPORT_ALLOWANCE(object):
    """
    Patient or partner receive Income Related Employment and Support Allowance
    (ESA).
    """

    NO_EVIDENCE_SEEN = 83
    EVIDENCE_SEEN = 84


class UNIVERSAL_CREDIT(object):
    """
    Patient or partner receive Universal Credit. Only applicable to courses of
    treatment with date of accepance on or after 1 April 2016.
    """

    NO_EVIDENCE_SEEN = 38
    EVIDENCE_SEEN = 39
