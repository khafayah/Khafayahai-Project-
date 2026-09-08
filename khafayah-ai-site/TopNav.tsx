/**
 * Replacement for the TopNav function in src/routes/index.tsx.
 *
 * Fixes: below 1024px there was no navigation at all, and below 640px there
 * was no enquiry button either, so a phone visitor saw only the logo.
 *
 * `useState`, `nav` and `WHATSAPP_LINK` already exist in index.tsx.
 */
function TopNav() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 border-b border-cornflower/25 bg-background/90 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-5 py-3.5">
        <a href="#top" className="min-w-0" onClick={() => setMenuOpen(false)}>
          <span className="font-serif block text-lg font-semibold tracking-tight whitespace-nowrap text-primary sm:text-xl">
            Khafayah.AI
          </span>
          <span className="block truncate text-[0.68rem] font-semibold tracking-[0.18em] text-clay-deep uppercase">
            AI Made Friendly
          </span>
        </a>

        <nav aria-label="Main" className="hidden items-center gap-7 lg:flex">
          {nav.map((n) => (
            <a
              key={n.href}
              href={n.href}
              className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
            >
              {n.label}
            </a>
          ))}
        </nav>

        <div className="flex shrink-0 items-center gap-2">
          <a
            href={WHATSAPP_LINK}
            className="hidden min-h-11 items-center rounded-full bg-clay-deep px-5 text-sm font-semibold text-clay-deep-foreground transition-colors hover:bg-clay-deep/90 sm:flex"
          >
            Enquire about a Clear Offer Page
          </a>

          <button
            type="button"
            onClick={() => setMenuOpen((open) => !open)}
            aria-expanded={menuOpen}
            aria-controls="mobile-menu"
            className="flex h-11 w-11 items-center justify-center rounded-full border border-cornflower/40 text-primary transition-colors hover:bg-secondary lg:hidden"
          >
            <span className="sr-only">
              {menuOpen ? "Close menu" : "Open menu"}
            </span>
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              aria-hidden
              focusable="false"
            >
              {menuOpen ? (
                <>
                  <path d="M5 5l14 14" />
                  <path d="M19 5L5 19" />
                </>
              ) : (
                <>
                  <path d="M3 6h18" />
                  <path d="M3 12h18" />
                  <path d="M3 18h18" />
                </>
              )}
            </svg>
          </button>
        </div>
      </div>

      <div
        id="mobile-menu"
        hidden={!menuOpen}
        className="border-t border-cornflower/25 bg-background lg:hidden"
      >
        <nav
          aria-label="Mobile"
          className="mx-auto flex max-w-6xl flex-col px-5 pb-4"
        >
          {nav.map((n) => (
            <a
              key={n.href}
              href={n.href}
              onClick={() => setMenuOpen(false)}
              className="flex min-h-12 items-center border-b border-border text-base font-medium text-primary"
            >
              {n.label}
            </a>
          ))}
          <a
            href={WHATSAPP_LINK}
            onClick={() => setMenuOpen(false)}
            className="mt-4 flex min-h-12 items-center justify-center rounded-full bg-clay-deep px-5 text-base font-semibold text-clay-deep-foreground sm:hidden"
          >
            Enquire about a Clear Offer Page
          </a>
        </nav>
      </div>
    </header>
  );
}
