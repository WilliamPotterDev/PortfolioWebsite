import type { Metadata } from "next";
import type { ReactNode } from "react";
import ParticleNetwork from "@/components/ParticleNetwork";
import SiteNav from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "CV | William Potter",
  description:
    "Curriculum vitae of William Potter — Finance BSc, Durham University.",
};

function SectionTitle({ children }: { children: ReactNode }) {
  return (
    <h2 className="border-b border-white/15 pb-2 text-[11px] font-medium uppercase tracking-[0.22em] text-white/55">
      {children}
    </h2>
  );
}

function RoleHeader({
  org,
  location,
  title,
  dates,
}: {
  org: string;
  location: string;
  title: string;
  dates: string;
}) {
  return (
    <div className="space-y-1">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
        <h3 className="text-[15px] font-semibold tracking-tight text-white sm:text-base">
          {org}
        </h3>
        <p className="text-[12px] tracking-wide text-white/50 sm:text-right">
          {location}
        </p>
      </div>
      <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
        <p className="text-[13px] italic text-white/70">{title}</p>
        <p className="text-[12px] tracking-wide text-white/45 sm:text-right">
          {dates}
        </p>
      </div>
    </div>
  );
}

export default function CvPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#0b0b0b] text-white">
      <ParticleNetwork />

      <div className="relative z-10 flex min-h-screen flex-col">
        <SiteNav />

        <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col px-6 pb-24 pt-6 sm:px-10">
          <div className="animate-fade-up flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-white/50">
                Curriculum Vitae
              </p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight sm:text-4xl">
                William Potter
              </h1>
              <p className="mt-3 text-sm tracking-wide text-white/60">
                Finance BSc · Durham University · Equity Research &amp; Markets
              </p>
            </div>
            <a
              href="/cv/William_Potter_Resume.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex w-fit items-center gap-2 border border-white/25 px-4 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-white/90 transition-colors hover:border-white/60 hover:bg-white/5"
            >
              Download PDF
              <span aria-hidden>↓</span>
            </a>
          </div>

          <div className="animate-fade-up-delay mt-6 flex flex-wrap gap-x-5 gap-y-2 text-[12px] tracking-wide text-white/55">
            <a
              href="mailto:williamgpotter@outlook.com"
              className="transition-opacity hover:text-white"
            >
              williamgpotter@outlook.com
            </a>
            <span className="text-white/25">·</span>
            <a
              href="https://www.linkedin.com/in/WilliamPotter0/"
              target="_blank"
              rel="noopener noreferrer"
              className="transition-opacity hover:text-white"
            >
              LinkedIn
            </a>
            <span className="text-white/25">·</span>
            <a href="tel:+447484119738" className="transition-opacity hover:text-white">
              +44 07484 119738
            </a>
          </div>

          <section className="animate-fade-up-delay-2 mt-12 space-y-6">
            <SectionTitle>Education</SectionTitle>

            <div className="space-y-6">
              <div>
                <RoleHeader
                  org="Durham University"
                  location="Durham"
                  title="BSc Finance"
                  dates="09/2026 – 06/2029"
                />
              </div>

              <div>
                <RoleHeader
                  org="Holy Cross College"
                  location="Bury, Greater Manchester"
                  title="A-levels: Mathematics (A), Computer Science (B), Physics (C)"
                  dates="09/2024 – 06/2026"
                />
              </div>

              <div>
                <RoleHeader
                  org="Cambridge University"
                  location="Cambridge"
                  title="STEM SMART Programme"
                  dates="01/2025 – 05/2026"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Tri-weekly extra &amp; super-curricular STEM problem-solving
                    and tutoring sessions.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Cambridge University summer school and lecture sessions.
                  </li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mt-12 space-y-6">
            <SectionTitle>Relevant Experience</SectionTitle>

            <div className="space-y-8">
              <div>
                <RoleHeader
                  org="The Derby High School"
                  location="Bury, Greater Manchester"
                  title="Mathematics Mentor / Tutor"
                  dates="11/2024 – 05/2025"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Partnered with The Derby High School to provide weekly GCSE
                    maths mentoring after college.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Delivered 1-to-1 and group sessions of up to 12 pupils.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Focused on difficult concepts that typically hold students
                    back from grades 8 and 9.
                  </li>
                </ul>
              </div>

              <div>
                <RoleHeader
                  org="TechMates"
                  location="Wigan, Greater Manchester"
                  title="Technical Help Assistant"
                  dates="08/2024 – 02/2025"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Taught and assisted in group and 1-to-1 sessions on using
                    technology to improve personal and business outcomes.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Created personalised learning plans for independent software
                    use.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Collaborated with a team to develop simple guides for common
                    technical problems.
                  </li>
                </ul>
              </div>

              <div>
                <RoleHeader
                  org="Government Dept. for Science, Innovation and Technology"
                  location="Salford, Greater Manchester"
                  title="Work Experience"
                  dates="06/2024 – 07/2024"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Attended briefings and meetings, building a core
                    understanding of government procedures including tender
                    processes, procurement planning, and public-private
                    partnerships.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Provided insights into the implementation plan for the
                    National Underground Asset Register (NUAR).
                  </li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mt-12 space-y-6">
            <SectionTitle>Projects</SectionTitle>

            <div className="space-y-6">
              <div>
                <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
                  <h3 className="text-[15px] font-semibold tracking-tight text-white">
                    Implied Volatility Surface
                  </h3>
                  <a
                    href="https://iv-surface-project.streamlit.app/"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-[12px] tracking-wide text-white/50 transition-opacity hover:text-white"
                  >
                    Live app →
                  </a>
                </div>
                <p className="mt-2 text-[13px] leading-relaxed text-white/65">
                  Developed a risk-valuation tool in Python that ingests live
                  options and underlying prices via API, numerically inverts
                  Black-Scholes to solve for implied volatility, and applies
                  liquidity filters to construct a volatility surface for risk
                  assessment.
                </p>
              </div>

              <div>
                <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
                  <h3 className="text-[15px] font-semibold tracking-tight text-white">
                    Silicon vs. Sentiment — SK Group Case Study
                  </h3>
                  <a
                    href="/projects/sk-group"
                    className="text-[12px] tracking-wide text-white/50 transition-opacity hover:text-white"
                  >
                    Read →
                  </a>
                </div>
                <p className="mt-2 text-[13px] leading-relaxed text-white/65">
                  Independent equity research contrasting SK Hynix&apos;s
                  semiconductor fundamentals with SK Telecom&apos;s
                  sentiment-driven AI re-rating; built the financial analysis and
                  valuation narrative.
                </p>
              </div>
            </div>
          </section>

          <section className="mt-12 space-y-6">
            <SectionTitle>Awards &amp; Certifications</SectionTitle>
            <ul className="space-y-2 text-[13px] leading-relaxed text-white/65">
              <li className="pl-4 before:mr-2 before:content-['–']">
                UKMT Senior Mathematics Challenge 2024 and 2025 — Silver Award
                in both years
              </li>
              <li className="pl-4 before:mr-2 before:content-['–']">
                IBM — Data Science Tools
              </li>
              <li className="pl-4 before:mr-2 before:content-['–']">
                IBM — Data Science in Practice
              </li>
              <li className="pl-4 before:mr-2 before:content-['–']">
                KPMG U.S. — Career Catalyst: Advisory
              </li>
              <li className="pl-4 before:mr-2 before:content-['–']">
                Duke of Edinburgh Gold Award 2026
              </li>
            </ul>
          </section>

          <section className="mt-12 space-y-6">
            <SectionTitle>Technical Skills</SectionTitle>
            <p className="text-[13px] leading-relaxed tracking-wide text-white/70">
              Excel (Advanced) · Python · SQL · VBA · C++
            </p>
          </section>
        </main>
      </div>
    </div>
  );
}
