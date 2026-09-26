# Ilubirin website — status record

Lovable project **Ilubirin Return**, `9c904fba-1187-4ffe-9468-3d785f1f7457`.

The live Lovable project is the source of truth. This file records what was
changed, why, and what is still open. It holds no copies of the code.

**The site is not launched.** Search engines are blocked and the noindex tag
is in place.

## Identity and domains

Three brands, kept deliberately separate. Do not merge their websites,
domains or positioning.

| Brand | Domain |
|-------|--------|
| Ilubirin | `ilubirin.com` |
| Khafayah Counselling | `khafayahconsultancyltd.com` |
| Khafayah.AI | `khafayah.ai` |

`ilubirin.com` was bought at Namecheap and is registered. As at 26 September
2026 its DNS is not pointed anywhere and it still shows the registrar holding
page. It is not yet connected to the Lovable project.

Data controller for the website: Khafayah Consultancy Limited, company
10977938, ICO registration ZB074804, Belmont Suite, Paragon Business Park,
Chorley New Road, Horwich, Bolton, BL6 6HG.

## Applied on 26 September 2026

| Change | Commit |
|--------|--------|
| Launch switch, sitemap, robots instructions, contact page, 404 and error copy | `90ddbdc4` |
| Em dash and contraction sweep, 27 replacements across 13 files | `86fd5c99` |
| Webfonts self-hosted, all Google font requests removed | `0499a630` |
| Ilubirin App link gated off | `d19ee374` |
| App address corrected to the free version | `dc1ebc45` |
| App access terms added to the App page | `3783e48c` |

### Launch switch

`src/lib/site.ts` holds `LAUNCHED`, `ROBOTS`, `SITE_URL`, `COMPANY` and
`BUSINESS_EMAIL`. `LAUNCHED` drives the robots meta tag in
`src/routes/__root.tsx`. `public/robots.txt` is a static file and cannot read
it, so both must be changed together on launch day. The steps are written in
the robots.txt comment.

Canonical and og:url are absolute on all nine routes, built from `SITE_URL`.
`public/sitemap.xml` lists the eleven public URLs.

### Contact page

WhatsApp is the primary enquiry route. The business email is shown second,
only because an email address is required. No contact form, and no stated
response time, because neither was true.

`hello@ilubirin.com` is the intended address but it does not exist yet. It
must not appear anywhere on the site until the mailbox has been created and
a test message sent and received. This was an explicit instruction.

### Fonts

Cormorant Garamond and Karla are served from `public/fonts/` as woff2 with
`font-display: swap`. The SIL Open Font License text for both families ships
alongside them.

Reason: every page previously requested fonts from `fonts.googleapis.com`,
which sent each visitor's IP address to Google before the page rendered. The
site is used by women who may not be safe at home, and the privacy notice
will state that the site uses no analytics and no non-essential cookies.

Verified on 26 September 2026: all six files carry the `wOF2` signature and
real sizes; a repository search for `googleapis.com` and `gstatic.com`
returns no matches.

### The Ilubirin App link

`SHOW_APP_LINK` in `src/lib/links.ts` is **false**. The App is described on
its page but the page does not open it.

Reason: the App's data handling has not been confirmed. What it collects,
stores or sends is unverified, and it has no privacy information of its own.
The website must not route anyone to a service whose data handling is
unknown.

Before setting the flag back to true:

1. Establish what the free version collects, stores or sends. Check analytics,
   cookies, localStorage, sessionStorage, IndexedDB, form submissions,
   outbound requests and any server or database connection.
2. Publish privacy information for the App itself.
3. Write the App section of the website privacy notice from the findings.

The App source is not in this repository and not in Google Drive. It sits on
a local machine in a folder named `ilubirin`. **It is not backed up anywhere.**
Getting it into a private repository is worth doing on its own merits.

### App access terms

The App page states, in normal body text rather than small print:

> The first ten Names are free to explore. Use the access code ilubirin.
>
> Lifetime access to the full App is £12.99.

Reason: the page previously described the App warmly and offered a button
with no mention of cost or limits. A reader could reasonably assume the whole
thing was free, then meet a paywall after ten Names.

Verified in Kit on 26 September 2026: product 269220, "Ilubirin Healing App,
Lifetime Access", £12.99 GBP, type download, published.

## Open items

1. **App data check.** Run against the free version, not the paid one. Blocks
   the App button and the App section of the privacy notice.
2. **Privacy notice and terms.** Drafted and corrected, awaiting sign-off.
   Neither is on the site. Both routes still show placeholder text, which is
   a launch blocker.
3. **`hello@ilubirin.com`.** To be created as a free alias on the existing
   Google Workspace licence, with a secondary domain and MX records. Set Gmail
   to reply from the address the message was sent to, so replies do not go out
   under another brand.
4. **Connect `ilubirin.com`** to the Lovable project.
5. **App checkout crosses brands.** The Kit purchase page sits on
   `khafayahcounselling.com`. That cuts across the separation set out above.
   Easier to change before the link is in circulation.
6. **Paid access code.** A single shared code unlocks the paid App. One buyer
   passing it on gives lifetime access for nothing. The current code is also
   no longer private and should be changed. A code per buyer is the fix if the
   App grows. The code itself is deliberately not recorded here.
7. **Launch.** Set `LAUNCHED = true` and swap the two lines in
   `public/robots.txt`, together.

## Permissions held

**Quotation from a woman who used the App.** Agreed by the person who wrote
it, sent to Khafayah by WhatsApp. She is content for her words to be used.
The WhatsApp message is the evidence and should be kept.

Date of agreement: Tuesday 15 September 2026. Khafayah described it as "last
week Tuesday" on Saturday 26 September 2026, which reads as the Tuesday of
the previous week. If the WhatsApp thread shows Tuesday 22 September 2026
instead, correct this line.

**She must not be named.** This was confirmed directly by Khafayah on
26 September 2026. The quotation is attributed only as "a sister", and that
applies everywhere it is used: the website, social media, printed material,
and anything shared privately. Her name is not recorded in this repository
and must not be added to it. If anyone asks who said it, the answer is that
she asked not to be named.

The quotation is not on the website as at 26 September 2026. It appears only
in copy written for sharing elsewhere.

## Carried over from the QA audit of 1 September 2026

Closed since that audit: the ecosystem dead ends, and the missing canonical
and og:url tags.

Still open from it: no og:image, so shared links preview as a blank card;
`min-h-screen` rather than `min-h-dvh`; and the mobile menu tap target
measured at 35 by 20 pixels, below the 44 by 44 guideline.
