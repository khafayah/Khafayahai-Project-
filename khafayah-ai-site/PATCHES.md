# Khafayah.AI launch fixes

Apply in order. Every change is small and self-contained.

---

## 1. src/lib/site.ts  — REPLACE THE WHOLE FILE

Use the copy in this folder. It adds `LAUNCHED`, `ROBOTS` and `SITE_URL`,
and derives `SHARE_IMAGE` from `SITE_URL` so the share image follows your
custom domain instead of pointing at lovable.app forever.

## 2. public/robots.txt — REPLACE THE WHOLE FILE

Use the copy in this folder.

---

## 3. src/routes/__root.tsx

Add the import at the top:

```ts
import { ROBOTS } from "@/lib/site";
```

Then swap the hardcoded robots line:

```diff
-      { name: "robots", content: "noindex, nofollow" },
+      { name: "robots", content: ROBOTS },
```

---

## 4. src/routes/privacy.tsx and src/routes/terms.tsx

In BOTH files, add `ROBOTS` to the existing import from `@/lib/site`, then:

```diff
-      { name: "robots", content: "noindex, nofollow" },
+      { name: "robots", content: ROBOTS },
```

### terms.tsx only — DELETE this block

It is an internal note that visitors currently see on the live page.

```diff
-        <div className="mt-6 rounded-2xl border border-cornflower/40 bg-powder-soft p-6 leading-relaxed">
-          These terms should be reviewed and confirmed before the site is
-          launched publicly.
-        </div>
```

---

## 5. src/styles.css — three values in the `:root` block

```diff
-  --clay-deep: oklch(0.662 0.103 38.7);
+  --clay-deep: oklch(0.560 0.108 38.7);
```
```diff
-  --border: oklch(0.889 0.019 62.4);
-  --input: oklch(0.889 0.019 62.4);
+  --border: oklch(0.845 0.022 62.4);
+  --input: oklch(0.845 0.022 62.4);
```
```diff
-  --ring: oklch(0.662 0.103 38.7);
+  --ring: oklch(0.560 0.108 38.7);
```

Why: white text on the old clay-deep measured 3.11 to 1. The button text is
16px semibold, which needs 4.5 to 1. The new value measures 4.72 to 1 and
keeps the same hue. It also reaches 4.56 to 1 as text on the page background,
which fixes the "AI Made Friendly" tagline.

Leave `--coral` as it is. It is only used for small decorative dots.

---

## 6. src/routes/index.tsx — four changes

### 6a. Imports

```diff
 import {
   COMPANY,
   EMAIL,
   EMAIL_LINK,
+  ROBOTS,
   SENSITIVE_WARNING,
   SHARE_IMAGE,
+  SITE_URL,
   WHATSAPP_LINK,
   WHATSAPP_NUMBER_DISPLAY,
 } from "@/lib/site";
```

### 6b. Route head — robots, canonical and og:url

```diff
   head: () => ({
     meta: [
       { title: TITLE },
       { name: "description", content: DESCRIPTION },
-      { name: "robots", content: "noindex, nofollow" },
+      { name: "robots", content: ROBOTS },
       { property: "og:title", content: TITLE },
       { property: "og:description", content: DESCRIPTION },
       { property: "og:type", content: "website" },
+      { property: "og:url", content: SITE_URL },
       { property: "og:image", content: SHARE_IMAGE },
       { name: "twitter:card", content: "summary_large_image" },
       { name: "twitter:image", content: SHARE_IMAGE },
     ],
+    links: [{ rel: "canonical", href: SITE_URL }],
   }),
```

### 6c. TopNav — REPLACE the whole function

Use `TopNav.tsx` in this folder. It adds a menu button below 1024px, keeps
the enquiry button reachable on every screen size, and shows the tagline at
all widths. `useState` is already imported in this file.

### 6d. Problems section — the numerals fail contrast

```diff
-                <span className="font-serif shrink-0 text-sm font-semibold text-seaglass">
+                <span className="font-serif shrink-0 text-sm font-semibold text-clay-deep">
```

Old: 2.57 to 1. New: 4.72 to 1.

### 6e. FAQ — keep closed answers in the page

Search engines and browser find-in-page cannot read the current version
because the answer is removed from the page when the item is closed.

```diff
-              {open === i && (
-                <p
-                  id={`faq-panel-${i}`}
-                  role="region"
-                  aria-labelledby={`faq-button-${i}`}
-                  className="px-4 pb-6 leading-relaxed text-muted-foreground"
-                >
-                  {f.a}
-                </p>
-              )}
+              <p
+                id={`faq-panel-${i}`}
+                role="region"
+                aria-labelledby={`faq-button-${i}`}
+                hidden={open !== i}
+                className="px-4 pb-6 leading-relaxed text-muted-foreground"
+              >
+                {f.a}
+              </p>
```

---

## 7. Optional, but worth doing before launch

- `src/styles.css` still carries a `.dark` block in default slate blue.
  Nothing sets the `dark` class, so it never renders. Delete it, or theme it.
- Fifteen colour token names cover four actual colours. `seaglass` and `mint`
  are warm peach tones, not greens, and `accent`, `clay` and `seaglass` are
  the same value. Renaming these is safe but touches many lines, so it is
  best done as its own change with a build running.

## 8. On launch day

1. `src/lib/site.ts` — set `LAUNCHED = true`.
2. `public/robots.txt` — swap the blocking lines for the allow lines.
3. `src/lib/site.ts` — set `SITE_URL` to the custom domain.

Nothing else needs to change.

---

## 9. src/routes/index.tsx — real sample pages

Replaces the two abstract wireframe drawings with real pages a visitor is
able to open. Use `Samples.tsx` in this folder. It replaces the `samples`
array and the `Samples` component.

After pasting it in, delete `SampleComposition` from index.tsx. Delete
`BrowserFrame` and `Bar` as well if nothing else uses them.

Add `SHOW_PRACTICE_SAMPLE` to the import from `@/lib/site`.

### What ships now

- Ilubirin, Return to Self. You built it and you own it, so it goes live
  with no further permission needed.

### What is gated

- The private practice page at my-practice-space.lovable.app is held behind
  `SHOW_PRACTICE_SAMPLE = false` in site.ts.

Two reasons, both from your own terms:

1. The page was built from another practitioner's Instagram and represents
   her real practice. Publishing it as a public sample needs her written
   permission.
2. Her reply was sent privately and about a free concept page, not a paid
   project. Quoting it publicly needs her permission and honest framing.

Ask her for both in one message. Once she agrees in writing, set
`SHOW_PRACTICE_SAMPLE = true`.

### On the testimonial

Her words describe a concept page you gave her, not work she bought. Label
it that way. "On a concept page created as an example" is accurate.
"Client testimonial" is not, and your terms hold you to accuracy.
