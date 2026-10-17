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
                Finance BSc (Hons) · Durham University
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
              href="mailto:william.g.potter@durham.ac.uk"
              className="transition-opacity hover:text-white"
            >
              william.g.potter@durham.ac.uk
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
              +44 7484 119738
            </a>
          </div>

          <section className="animate-fade-up-delay-2 mt-12 space-y-6">
            <SectionTitle>Education</SectionTitle>

            <div className="space-y-6">
              <div>
                <RoleHeader
                  org="Durham University"
                  location="Durham"
                  title="BSc Finance (Hons)"
                  dates="09/2026 – 06/2029"
                />
              </div>

              <div>
                <RoleHeader
                  org="Holy Cross College"
                  location="Bury, Manchester"
                  title="A-Levels: Mathematics (A), Computer Science (B), Physics (C)"
                  dates="09/2024 – 06/2026"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Built a recruitment system in VBA, Access and SQL, with
                    dashboards that tracked candidates, employers and
                    consultants, as computer science coursework.
                  </li>
                </ul>
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
                    Worked through STEM problems three times a week and
                    explained the solutions in tutoring sessions.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Attended the Cambridge STEM SMART summer school and
                    lectures.
                  </li>
                </ul>
              </div>
            </div>
          </section>

          <section className="mt-12 space-y-6">
            <SectionTitle>Experience</SectionTitle>

            <div className="space-y-8">
              <div>
                <RoleHeader
                  org="The Derby High School"
                  location="Bury, Manchester"
                  title="Mathematics Mentor &amp; Tutor"
                  dates="11/2024 – 05/2025"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Mentored GCSE maths pupils every week after college,
                    one-to-one and in groups of up to 12, focusing on the
                    topics that blocked grades 8 and 9.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Found where each pupil was stuck, then explained the next
                    step in plain language.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Kept several pupils moving in the same hour and decided who
                    needed the time first.
                  </li>
                </ul>
              </div>

              <div>
                <RoleHeader
                  org="TechMates"
                  location="Bury, Manchester"
                  title="Technical Help Assistant"
                  dates="11/2024 – 05/2025"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Taught group and one-to-one sessions on software for
                    everyday tasks and small businesses, and wrote a separate
                    plan so each person could carry on without help.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Turned problems that kept coming up into short written
                    guides.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Checked the steps with the team before a guide was handed
                    out.
                  </li>
                </ul>
              </div>

              <div>
                <RoleHeader
                  org="Government Department for Science, Innovation, and Technology"
                  location="Salford, Manchester"
                  title="Work Experience"
                  dates="06/2024 – 07/2024"
                />
                <ul className="mt-3 space-y-1.5 text-[13px] leading-relaxed text-white/65">
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Attended briefings on tendering, procurement planning and
                    public-private partnerships, and kept notes on the process.
                  </li>
                  <li className="pl-4 before:mr-2 before:content-['–']">
                    Followed the implementation plan for the National
                    Underground Asset Register and raised points from those
                    briefings.
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
                  Built a Python tool that takes live option and share prices,
                  drops illiquid prices, and solves for implied volatility from
                  data that can be checked.
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
                  Set SK Hynix&apos;s semiconductor results next to SK
                  Telecom&apos;s market position, with the figures and the
                  valuation in one document.
                </p>
              </div>

              <div>
                <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
                  <h3 className="text-[15px] font-semibold tracking-tight text-white">
                    Equity Beta Estimation
                  </h3>
                  <a
                    href="/projects/market-betas"
                    className="text-[12px] tracking-wide text-white/50 transition-opacity hover:text-white"
                  >
                    View →
                  </a>
                </div>
                <p className="mt-2 text-[13px] leading-relaxed text-white/65">
                  Estimated equity betas for Apple, Nvidia, Broadcom, Microsoft
                  and Oracle from CRSP daily returns against the value-weighted
                  market.
                </p>
              </div>

              <div>
                <div className="flex flex-col gap-1 sm:flex-row sm:items-baseline sm:justify-between">
                  <h3 className="text-[15px] font-semibold tracking-tight text-white">
                    Loan Book Diversification
                  </h3>
                  <a
                    href="/projects/loan-book"
                    className="text-[12px] tracking-wide text-white/50 transition-opacity hover:text-white"
                  >
                    View →
                  </a>
                </div>
                <p className="mt-2 text-[13px] leading-relaxed text-white/65">
                  Monte Carlo simulation of loan defaults showing how larger
                  books keep the same average loss but cut bad-year tail risk.
                </p>
              </div>
            </div>
          </section>

          <section className="mt-12 space-y-6">
            <SectionTitle>Awards &amp; Certifications</SectionTitle>
            <ul className="space-y-2 text-[13px] leading-relaxed text-white/65">
              <li className="pl-4 before:mr-2 before:content-['–']">
                UKMT Senior Mathematics Challenge 2024 and 2025 — Silver Awards
                in Both
              </li>
              <li className="pl-4 before:mr-2 before:content-['–']">
                IBM: Data Science Tools, Data Science in Practice
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
              Excel (Advanced) · VBA · SQL · Python · C++ (Basic)
            </p>
          </section>
        </main>
      </div>
    </div>
  );
}
