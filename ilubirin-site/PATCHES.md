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

The data check was completed on 26 September 2026 by reading the App source
directly. Findings are below. The flag stays false until the website privacy
notice is published, so that the App and the page explaining it go live
together.

The App source is not in this repository and not in Google Drive. It sits on
a local machine in a folder named `ilubirin`, and is deployed on SiteGround.
**It is not backed up anywhere.** Getting it into a private repository is
worth doing on its own merits.

### What the App does with personal data

Verified by reading `index.html`, `index_free.html` and `index_full.html` on
26 September 2026. Khafayah confirmed the deployed version differs only in
the access code.

Held in the browser's own storage, never transmitted:

| Key | Storage | Holds |
|-----|---------|-------|
| `ilubirin_tier` | sessionStorage, clears when the browser closes | which version was unlocked |
| `ilubirin_saved` | localStorage, persists | the saved Name and ayah, not free text |

The local copies on Khafayah's machine use `localStorage` for the tier. The
deployed files use `sessionStorage`. The deployed version is the authority.
Live files were last modified in April 2026, so the local copies have drifted
from what is served. Worth reconciling.

Sent off the device, only when a woman submits the optional feedback:
the rating out of five, the free text she typed, whether she ticked the
testimonial permission box, the timestamp, and which Name she was reading.
No name, email address or telephone number is asked for or collected.

Delivery is by **EmailJS**, loaded from **jsDelivr**. Both receive the
visitor's IP address as part of serving the page. Two things remain
unverified: which country EmailJS processes data in, which decides whether an
international transfer line is needed, and which inbox the template delivers
to.

The full version also offers an "email my reflection" button, which opens the
woman's own email client with the text filled in. Nothing is transmitted by
the App.

Not present anywhere in the App: third party analytics, cookies, tracking
pixels, advertising code, any Google or Meta connection, any database, any
form element, any fetch or XMLHttpRequest call.

### Verified from the live systems, 27 September 2026

Checked in SiteGround and against EmailJS published terms.

| Item | Finding |
|------|---------|
| App host | SiteGround GrowBig, data centre London, United Kingdom |
| Certificate | Let's Encrypt, valid, expires 28 November 2026 |
| Server access logs | 30 daily archives. Hold IP address, timestamp, request type, URI, status code, referrer, user agent |
| Traffic statistics | **SiteGround Traffic is switched on** for the App subdomain |
| Backups | Automated daily, retained about 30 days |
| EmailJS processing | United States, on AWS |
| EmailJS retention | Request activity and metadata, 30 days for active accounts. Can be deactivated per template |
| EmailJS DPA | Published and available. **Acceptance by this account not confirmed** |
| EmailJS recipient inbox | Not verified. Dashboard was not authenticated |

The SiteGround Traffic finding matters. An earlier draft of the notice said
"we do not use analytics" without qualification. That would have been wrong
for the App. The published notice now distinguishes the website, which uses
none, from the App, whose host produces visitor counts from its own server
logs. No cookies are set and no third party tracking is involved.

### EmailJS international transfer: unresolved

Verified against the EmailJS account and their published terms on
27 September 2026. **No UK transfer safeguard could be confirmed.** Two
problems, either of which is enough on its own.

1. **The DPA is scoped to the EU GDPR.** The Terms incorporate it "to the
   extent that EmailJS processes any personal data that is subject to the EU
   General Data Protection Regulation". Ilubirin's data is subject to the UK
   GDPR. On a plain reading the clause does not reach it.
2. **EU SCCs alone do not cover a UK restricted transfer.** The DPA relies on
   "EU approved standard contractual clauses". ICO guidance states the EU SCCs
   are not valid on their own for UK restricted transfers, and that the UK
   Addendum is what allows reliance on them. Neither an Addendum nor an IDTA
   is visible on the account.

EmailJS Pte. Ltd. is a Singapore-registered company processing in the United
States.

**The privacy notice must not name a UK transfer safeguard.** Until EmailJS
answers, the notice states the position as unresolved and offers women the
choice not to use the feedback box.

### The recommended fix

Replace EmailJS with a small form handler on SiteGround, which already hosts
the App in London. That removes the transfer, removes both EmailJS and
jsDelivr as processors, and keeps the feedback anonymous.

The alternative of a mailto link also removes the transfer but reveals the
woman's own email address, which is the wrong trade for this audience.

The feedback form carries an unticked checkbox reading "I give permission for
my words to be shared anonymously as a testimonial". That is a proper
affirmative consent mechanism and the privacy notice relies on it for that
purpose only.

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
6. **Paid access code.** Both access codes are written in plain text in the
   JavaScript of the App's gate page, so anyone who views the page source
   reads the paid code and takes the £12.99 product for nothing. A single
   shared code also means one buyer passing it on gives lifetime access to
   anyone. This is normal for a single file app, and it does mean the code is
   not protecting revenue. A code per buyer is the fix if the App grows.
   Neither code is recorded here.

   The free access code is `ilubirin`, confirmed live on 26 September 2026,
   and matches what the website publishes. An earlier local copy used a
   different value; the deployed version is the authority.
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

The quotation is on the Ilubirin App page, `/ecosystem/healing-app`, added
26 September 2026. It sits between the App description and the access terms,
so it reads as one woman's experience rather than as a line placed next to a
price. It is styled with the left accent border and display type already used
elsewhere on the site: no card, no panel, no stars, no heading such as
"Testimonial".

The rendered text was compared against the original character for character
before it went in. It is reproduced exactly, including the word "really",
which stays because altering someone's words is not ours to do.

It is the only quotation on the site.

## Carried over from the QA audit of 1 September 2026

Closed since that audit: the ecosystem dead ends, and the missing canonical
and og:url tags.

Still open from it: no og:image, so shared links preview as a blank card;
`min-h-screen` rather than `min-h-dvh`; and the mobile menu tap target
measured at 35 by 20 pixels, below the 44 by 44 guideline.
