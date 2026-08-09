const navLinks = [
  { label: "Home", href: "/" },
  { label: "Projects", href: "/projects" },
  { label: "CV", href: "#cv" },
];

export default function SiteNav() {
  return (
    <header className="flex items-center justify-end gap-4 px-5 py-6 sm:px-10">
      <nav className="flex flex-wrap items-center justify-end gap-x-5 gap-y-2 sm:gap-x-8">
        {navLinks.map((link) => (
          <a
            key={link.label}
            href={link.href}
            className="text-[11px] font-medium uppercase tracking-[0.18em] text-white/90 transition-opacity hover:opacity-60"
          >
            {link.label}
          </a>
        ))}
      </nav>
    </header>
  );
}
