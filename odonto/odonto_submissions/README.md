# Glossary

`envelope` The wrapper to a claim about an episode
`bdcs1` An episode translated into the fp17/fp17O claim

`transmission_id` the id of specific transmission that we sent to a compass, on the envelope, their term is the `serial number`

`submission_id` is the id of an episode and the id sent in a bdcs1 as the `message reference  number` (their term). Previously it was transmission id. However given the case where we send a single episode multiple times it makes more sense to use episode id.

