===========
XSD schemas
===========


Schema files
============

This directory contains the following files.


Interchange Envelope Schema (xml_envelope.xsd)
----------------------------------------------

Defines the structure of data items associated with the interchange as a whole
rather than any single message.


BCDS1 Message Schema (xml_bcds1.xsd)
------------------------------------

Defines the structure of the inbound BCDS1 message, containing the contents of
a BCDS1 form submitted by a dental practice.


Transmission Response (CONTRL) Message Schema (xml_contrl.xsd)
--------------------------------------------------------------

Defines the structure of the outbound transmission response message, containing
a response to a transmission sent to the DPB.


Claim Response (RESPCE) Message Schema (xml_respce.xsd)
-------------------------------------------------------

Defines the structure of the claim response message, containing validation
rejection codes and other responses to specific claims that cannot immediately
be paid.


Payment Schedule (SCHEDL) Message Schema (xml_schedl.xsd)
---------------------------------------------------------

Defines the structure of the payment schedule message, containing item of
service payments for electronically transmitted claims included in the
dentists’ payment schedule.


Daily Response (DAILYS) Message Schema (xml_dailys.xsd)
-------------------------------------------------------

Defines the structure of the daily response message, containing details of
claims processed on the previous working day.


General Information (BRDCST) Message Schema (xml_brdcst.xsd)
------------------------------------------------------------

Defines the structure of "broadcast" message used by the NHSDS to pass general
information to practices.  Note that this XML message does not contain
information used to update standard response messages (RMU segments).


Interchange Receipt Schema (xml_receipt.xsd)
--------------------------------------------

Defines the structure of the XML receipt to be returned by the NHSDS web server
to the PMS software as an acknowledgement of the claims data sent.

The receipt provides information about what the web server received (a byte
count) and when the server received it (date and time).  If the interchange is
invalid then an error string will be returned.

It is also possible that individual messages within an interchange may be
rejected.  Each invalid message will be represented by a <msg> element,
containing identifying details for that message and an error description.  If
messages are rejected but the interchange as a whole is accepted, then <msg>
elements will appear but the error string for the interchange will be empty or
not present.


Terms
=====

envelope
  Data belonging not to any one message but to an interchange as a whole. In
  XML, this data is contained as attributes of the interchange tag.
  Interchange Envelope Schema.

interchange
  In the EDI interface specification, corresponds to a "file" or single
  transmission of data to or from a practice.

message
  A single claim from a dentist, or a discrete data response from the DPB.

segment
  Section of a message, used to group data items logically according to
  purpose.

