# Khafayah.AI site — APPLIED

Everything in this folder has been applied to the Lovable project
`real-reach-builder` (a67dc871-2862-4fca-ae67-3f7b74fbac9c).

**Do not paste these files into the project.** The colour tokens were
renamed after these were written, so the old names would silently break
the styling. The live project is the source of truth.

Renames that happened after this folder was written:

| old name              | new name            |
|-----------------------|---------------------|
| `clay-deep`           | `terracotta-deep`   |
| `clay`                | `terracotta-mid`    |
| `cornflower`          | `lavender`          |
| `powder-soft`         | `lavender-soft`     |
| `seaglass` / `mint`   | `terracotta` / `peach` |

`TopNav.tsx` and `Samples.tsx` were removed from this folder for that
reason. Both are live in the project.

## Applied

- Launch switch (`LAUNCHED`, `ROBOTS`) driving robots meta on every route
- `SITE_URL`, canonical link, `og:url`, domain-following share image
- Contrast fix: button text 4.72:1, was 3.11:1
- Mobile menu below 1024px, enquiry route at every width
- FAQ answers stay in the document when collapsed
- Internal reviewer note removed from the terms page
- Real sample pages, with the third-party page behind a permission gate
- Colour tokens renamed so the names match the actual colours
- Dark theme rebranded to plum and terracotta (every pairing passes)
- "Working test price" and the validation-offer wording removed
- Nav label changed to "Sample pages"

## Still open

1. Permission from the practitioner for the practice page and her words.
   Then set `SHOW_PRACTICE_SAMPLE = true` in `src/lib/site.ts`.
2. ~~Consumer cancellation position in the terms.~~ CLOSED 21 September 2026.
   Clause 9 now splits Business Customers from Consumers, states the 14 day
   period, the express early-start request, loss of the right on full
   performance, proportionate payment, and the 14 day refund deadline with
   the same-payment-method rule. A Schedule 3 Model Cancellation Form is
   published. The operating process is recorded in Notion as
   "SOP: Khafayah.AI Consumer Cancellation & Durable Medium" under KAOS HQ,
   with a per-contract "Consumer Contract Record - Schedule 2 Checklist"
   template beneath it. Terms clause 3 also states that £300 is the total
   price and no VAT is charged. Workstream closed 21 September 2026.
3. Confirm Lovable injects no analytics, since the privacy notice states
   publicly that there are none.
4. Dark theme is themed but unreachable. Nothing sets the `dark` class.
   Add a toggle, or delete the block.
5. The samples grid is `lg:grid-cols-2` with one card in it.
6. Launch day: set `LAUNCHED = true`, update `public/robots.txt`, and set
   `SITE_URL` to the custom domain.
