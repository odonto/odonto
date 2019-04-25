from django.core.management.base import BaseCommand
import requests

XML = """
<icset>
    <ic schvn="1.0" synv="1" ori="site_number" dest=“fake” datrel=“fake” tim="0917" seq="000001" swname="pythonfp17" swver="unknown" pmsno=“fake” teind="1">\n  <bcds1 schvn="1.0" clrn="000007" perf="100000" pin="100000" cno="1000000000" loc="000004" resct="01" noseg="6">\n    <pat sex="F" dob="19580123" ptfn="SALLY" ptsur="BARLASTON">\n      <adrdet>\n        <adrln>1 HIGH STREET</adrln>\n      </adrdet>\n    </pat>\n    <tda>\n      <trtdatgrp datacc="170401" datcp="170401"/>\n    </tda>\n    <chx ptchg="2060" curcd="gbp"/>\n    <tst>\n      <reptrtty trtcd="9150" noins="01"/>\n      <reptrtty trtcd="9317"/>\n      <reptrtty trtcd="9301"/>\n      <reptrtty trtcd="9172" noins="09"/>\n      <reptrtty trtcd="9025" noins="01"/>\n    </tst>\n  </bcds1>\n</ic>'
    <ic schvn="1.0" synv="1" ori="site_number" dest="1234" datrel="190424" tim="0917" seq="000001" swname="pythonfp17" swver="unknown" pmsno="00000001" teind="1">
    <bcds1 schvn="1.0" clrn="000007" perf="100000" pin="100000" cno="1000000000" loc="000004" resct="01" noseg="6">
        <pat sex="F" dob="19580123" ptfn=“TEST” ptsur=“TEST”>
        <adrdet>
            <adrln>1 TEST STREET</adrln>
        </adrdet>
        </pat>
        <tda>
        <trtdatgrp datacc="170401" datcp="170401"/>
        </tda>
        <chx ptchg="2060" curcd="gbp"/>
        <tst>
        <reptrtty trtcd="9150" noins="01"/>
        <reptrtty trtcd="9317"/>
        <reptrtty trtcd="9301"/>
        <reptrtty trtcd="9172" noins="09"/>
        <reptrtty trtcd="9025" noins="01"/>
        </tst>
    </bcds1>
    </ic>
</icset>
"""

URL = "https://ebusiness.dpb.nhs.uk/claimsrequests.asp"


class Command(BaseCommand):
    def handle(self, *args, **options):
        result = requests.post(URL, data="test")
        print("{} {}".format(result.status_code, result.content))

