import ParticleNetwork from "@/components/ParticleNetwork";
import SiteNav from "@/components/SiteNav";

function LinkedInIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden className="h-5 w-5 fill-current">
      <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
    </svg>
  );
}

function GitHubIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden className="h-5 w-5 fill-current">
      <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.757-1.333-1.757-1.09-.745.083-.729.083-.729 1.205.084 1.84 1.236 1.84 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12" />
    </svg>
  );
}

function OutlookIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden className="h-5 w-5 fill-current">
      <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z" />
    </svg>
  );
}

const socialLinks = [
  {
    label: "LinkedIn",
    tooltip: "William Potter",
    href: "https://www.linkedin.com/in/WilliamPotter0/",
    external: true,
    Icon: LinkedInIcon,
  },
  {
    label: "GitHub",
    tooltip: "WilliamPotterDev",
    href: "https://github.com/WilliamPotterDev",
    external: true,
    Icon: GitHubIcon,
  },
  {
    label: "Outlook",
    tooltip: "williamgpotter@outlook.com",
    href: "mailto:williamgpotter@outlook.com",
    external: false,
    Icon: OutlookIcon,
  },
];

export default function Home() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#0b0b0b] text-white">
      <ParticleNetwork />

      <div className="relative z-10 flex min-h-screen flex-col">
        <SiteNav />

        <main className="flex flex-1 flex-col items-center justify-center px-6 pb-24 text-center">
          <h1 className="animate-fade-up text-[2.6rem] font-semibold tracking-tight text-white sm:text-5xl md:text-6xl">
            William Potter
          </h1>
          <p className="animate-fade-up-delay mt-4 text-base font-light tracking-wide text-white/85 sm:text-lg">
            Finance BSc student at Durham · Python · C++ · Financial Modelling
          </p>

          <div className="animate-fade-up-delay-2 mt-10 flex items-center gap-7">
            {socialLinks.map(({ label, tooltip, href, external, Icon }) => (
              <a
                key={label}
                href={href}
                target={external ? "_blank" : undefined}
                rel={external ? "noopener noreferrer" : undefined}
                aria-label={`${label} — ${tooltip}`}
                className="group relative text-white/90 transition-transform duration-200 hover:scale-110 hover:text-white"
              >
                <Icon />
                <span className="pointer-events-none absolute left-1/2 top-full z-20 mt-2.5 -translate-x-1/2 whitespace-nowrap rounded-md bg-[#3a3a3a] px-2.5 py-1 text-[11px] font-normal tracking-wide text-white opacity-0 shadow-lg transition-opacity duration-150 group-hover:opacity-100">
                  {tooltip}
                </span>
              </a>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
