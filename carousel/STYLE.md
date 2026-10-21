# Addzify carousel rules

Used by the daily scheduled run when `queue.json` has no unposted spec left and a new one must be written.

## Audience
Indian factory owners, manufacturers, exporters and their sales heads (MSME). B2B only.

## Voice
- Hinglish (Roman script), short sentences, spoken tone, as in the existing specs.
- Name a concrete pain in the hook. No intro, no "Hello everyone".
- Never invent statistics, percentages, client results or testimonials. Use concrete, checkable advice instead.

## Structure (spec fields: see the docstring in `make_carousel.py`)
- Hook slide: `hook_top` (setup, under 60 chars) + `hook_main` (the sting, under 45 chars) + `pill` ("N galtiyan. Swipe").
- 3 to 5 points. Each point: title under 45 chars, box texts under 110 chars each.
- CTA slide: the keyword and the matching free PDF.
- Caption: hook line, one line of context, the 3 CTA lines (comment keyword, share with partner/sales head, follow), then 8 hashtags. Under 900 characters.

## Keywords: use ONLY these (each has a live Zorcha DM automation and a PDF in this repo)
| Keyword | PDF offered in the CTA |
|---|---|
| BUYERS | B2B Buyer Attraction Blueprint |
| TRACKER | RFQ Follow-Up Tracker |
| CATALOGUE | Product Catalogue Playbook |
| CHECKLIST | Website RFQ Audit Checklist |

Rotate keywords so the same one is not used two days in a row.

## Topic pool (for new specs)
RFQ handling, catalogue and price lists, website and Google presence, IndiaMART / TradeIndia dependence, export buyer trust, trade-fair follow-up, WhatsApp follow-up etiquette, sample requests, repeat orders, distributor/dealer onboarding, product photography, LinkedIn for factory owners.
Do not repeat a slug or the same hook as anything in `posted.json`.
