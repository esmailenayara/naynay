type P = { className?: string };
const base = "shrink-0";

export const IconWhatsApp = ({ className = "size-5" }: P) => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className={`${base} ${className}`} fill="currentColor">
    <path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5.1 5.2-1.4A9.9 9.9 0 1 0 12.04 2Zm0 18.1a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7 3.9Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.6-.3Z" />
  </svg>
);

const Stroke = ({ className = "size-5", d }: P & { d: string }) => (
  <svg
    viewBox="0 0 24 24"
    aria-hidden="true"
    className={`${base} ${className}`}
    fill="none"
    stroke="currentColor"
    strokeWidth={1.7}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    <path d={d} />
  </svg>
);

export const IconPin = (p: P) => (
  <Stroke {...p} d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Zm0-9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5Z" />
);
export const IconClock = (p: P) => <Stroke {...p} d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Zm0-13v4l3 2" />;
export const IconInstagram = ({ className = "size-5" }: P) => (
  <svg viewBox="0 0 24 24" aria-hidden="true" className={`${base} ${className}`} fill="none" stroke="currentColor" strokeWidth={1.7}>
    <rect x="3" y="3" width="18" height="18" rx="5" />
    <circle cx="12" cy="12" r="4" />
    <circle cx="17.5" cy="6.5" r="0.9" fill="currentColor" stroke="none" />
  </svg>
);
export const IconCheck = (p: P) => <Stroke {...p} d="m5 12.5 4.5 4.5L19 7.5" />;
export const IconStar = (p: P) => (
  <Stroke {...p} d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9L12 3Z" />
);
export const IconChevron = (p: P) => <Stroke {...p} d="m6 9 6 6 6-6" />;
export const IconExternal = (p: P) => <Stroke {...p} d="M14 4h6v6m0-6-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" />;
