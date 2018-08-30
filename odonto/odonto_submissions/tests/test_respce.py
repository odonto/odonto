from opal.core.test import OpalTestCase


class RespceTestCase(OpalTestCase):
    def setUp(self):
        super().setUp()

        self.respce = """
        <?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>
        <ic schvn="1.0" synv="1" ori="1234" dest="01009" datrel="180319" tim="1236" seq="000286" xmcat="1">
            <contrl schvn="1.0" ori="01009" dest="1234" seq="160900" accd="1"/>
            <respce schvn="1.0">
                <rsp cno="2371750001" perf="237175" loc="008023" clrn="069802">
                    <mstxt rspty="@312">No significant treatment on an EDI claim</mstxt>
                </rsp>
                <rsp cno="2371750001" perf="237175" loc="008023" clrn="069810">
                    <mstxt rspty="898">Advanced Mandatory Services after 01/04/2014</mstxt>
                </rsp>
                <rsp cno="2371750001" perf="237175" loc="008023" clrn="069822">
                    <mstxt rspty="898">Advanced Mandatory Services after 01/04/2014</mstxt>
                </rsp>
                <rsp cno="2371750001" perf="237175" loc="008023" clrn="069826">
                    <mstxt rspty="898">Advanced Mandatory Services after 01/04/2014</mstxt>
                </rsp>
                <rsp cno="2371750001" perf="237175" loc="008023" clrn="069831">
                    <mstxt rspty="898">Advanced Mandatory Services after 01/04/2014</mstxt>
                </rsp>
            </respce>
        </ic>
        """.strip()
