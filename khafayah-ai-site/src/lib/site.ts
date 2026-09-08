export const BRAND = "Khafayah.AI";
export const OFFER = "Clear Offer Page";
export const PRICE = "£300";

/**
 * LAUNCH SWITCH.
 *
 * false  -> the whole site is hidden from search engines (work in progress).
 * true   -> the site is open to search engines.
 *
 * Set this to true on launch day. It is the only change needed.
 * public/robots.txt must be updated at the same time.
 */
export const LAUNCHED = false;

export const ROBOTS = LAUNCHED ? "index, follow" : "noindex, nofollow";

/** Update this one line when the custom domain goes live. */
export const SITE_URL = "https://real-reach-builder.lovable.app";

export const SHARE_IMAGE = `${SITE_URL}/share-image.jpg`;

/**
 * PERMISSION GATE for the sample pages section.
 *
 * The practice page at my-practice-space.lovable.app was created as an
 * example for another practitioner, using material from her Instagram.
 * Set this to true only once she has confirmed in writing that you may
 * show the page publicly and quote her words. Your own terms require
 * that permission before publication.
 */
export const SHOW_PRACTICE_SAMPLE = false;


const WHATSAPP_MESSAGE =
  "As-salamu alaykum, I’m interested in a £300 Clear Offer Page. I already offer a defined service and would like to discuss whether the page is a good fit.";

export const WHATSAPP_LINK = `https://wa.me/447585847631?text=${encodeURIComponent(
  WHATSAPP_MESSAGE,
)}`;
export const WHATSAPP_NUMBER_DISPLAY = "+44 7585 847631";
export const EMAIL = "khafayah@khafayahconsultancyltd.com";
export const EMAIL_LINK = `mailto:${EMAIL}?subject=Clear%20Offer%20Page%20enquiry`;

export const SENSITIVE_WARNING =
  "Please do not send client-identifiable information, counselling notes, health information, safeguarding information or other sensitive personal details. A brief outline of your business and the page you need is enough.";

export const COMPANY = {
  name: "Khafayah Consultancy Limited",
  number: "10977938",
  ico: "ZB074804",
  address:
    "Belmont Suite, Paragon Business Park, Chorley New Road, Horwich, Bolton, BL6 6HG, United Kingdom",
};

export const LAST_UPDATED = "8 September 2026";
