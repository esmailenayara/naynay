"use client";

import { EVENTO_ABRIR_COOKIES } from "./CookieBanner";

export function CookiePrefsButton() {
  return (
    <button
      type="button"
      onClick={() => window.dispatchEvent(new Event(EVENTO_ABRIR_COOKIES))}
      className="underline underline-offset-2 hover:opacity-80"
    >
      Preferências de cookies
    </button>
  );
}
