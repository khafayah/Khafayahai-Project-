/**
 * Replacement for the `samples` array and the `Samples` component in
 * src/routes/index.tsx.
 *
 * This removes the two abstract wireframe drawings and shows real pages
 * instead. Delete `SampleComposition` from index.tsx once this is in, and
 * delete `BrowserFrame` and `Bar` too if nothing else uses them.
 *
 * Add to the import from "@/lib/site":  SHOW_PRACTICE_SAMPLE
 */

type Sample = {
  title: string;
  label: string;
  text: string;
  href: string;
  linkText: string;
};

const ownedSamples: Sample[] = [
  {
    title: "Ilubirin, Return to Self",
    label: "Built and owned by Khafayah.AI",
    text: "A faith-rooted healing space for Muslim women. It shows how a sensitive service can explain who it is for, how it works and what to do next, without losing its warmth.",
    href: "https://ilubirin-return-to-self.lovable.app",
    linkText: "View the Ilubirin page",
  },
];

/**
 * Shown only once the practitioner has confirmed in writing that the page
 * and her words may be used publicly. See SHOW_PRACTICE_SAMPLE in site.ts.
 */
const practiceSample: Sample = {
  title: "A private counselling practice",
  label: "Concept page, shared with permission",
  text: "A concept page created as an example for a counsellor whose work lived on Instagram. It gathers the introduction, the approach and one clear next step into a single space.",
  href: "https://my-practice-space.lovable.app",
  linkText: "View the practice page",
};

function ArrowIcon() {
  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
      focusable="false"
    >
      <path d="M5 12h14" />
      <path d="M13 6l6 6-6 6" />
    </svg>
  );
}

function SampleCard({ sample }: { sample: Sample }) {
  return (
    <article className="flex flex-col rounded-3xl border border-cornflower/30 bg-card p-7 shadow-sm">
      <h3 className="font-serif text-2xl font-semibold text-primary">
        {sample.title}
      </h3>
      <p className="mt-3 inline-block self-start rounded-full bg-secondary px-3 py-1 text-xs font-semibold tracking-wide text-muted-foreground">
        {sample.label}
      </p>
      <p className="mt-4 flex-1 leading-relaxed text-muted-foreground">
        {sample.text}
      </p>
      <a
        href={sample.href}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-6 inline-flex min-h-12 items-center gap-2 self-start rounded-full border-2 border-primary/70 px-6 text-base font-semibold text-primary transition-colors hover:bg-secondary"
      >
        {sample.linkText}
        <ArrowIcon />
      </a>
    </article>
  );
}

function Samples() {
  const samples = SHOW_PRACTICE_SAMPLE
    ? [...ownedSamples, practiceSample]
    : ownedSamples;

  return (
    <section id="samples" className="relative overflow-hidden bg-background">
      <div
        aria-hidden
        className="pointer-events-none absolute -top-12 -right-10 hidden h-56 w-44 opacity-40 xl:block"
      >
        <ArchLeafMotif className="h-full w-full" />
      </div>

      <div className="relative mx-auto max-w-6xl px-5 py-20 sm:py-24">
        <div className="max-w-2xl">
          <p className="text-xs font-semibold tracking-[0.16em] text-muted-foreground uppercase">
            Sample pages
          </p>
          <h2 className="font-serif mt-4 text-3xl font-semibold sm:text-4xl lg:text-5xl">
            The kind of pages I build
          </h2>
          <p className="mt-4 leading-relaxed text-muted-foreground">
            Real pages you are able to open and read, rather than drawings of
            pages.
          </p>
        </div>

        <div className="mt-14 grid gap-8 lg:grid-cols-2">
          {samples.map((s) => (
            <SampleCard key={s.title} sample={s} />
          ))}
        </div>
      </div>
    </section>
  );
}
