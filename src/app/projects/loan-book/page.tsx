import type { Metadata } from "next";
import Image from "next/image";
import ParticleNetwork from "@/components/ParticleNetwork";
import SiteNav from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Loan Book Diversification | William Potter",
  description:
    "Monte Carlo simulation of loan-book default losses showing how diversification reduces bad-year credit risk.",
};

const rows = [
  { loans: "100", typical: "0.79%", bad: "2.00%" },
  { loans: "1,000", typical: "0.80%", bad: "1.08%" },
  { loans: "20,000", typical: "0.80%", bad: "0.86%" },
];

export default function LoanBookPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#0b0b0b] text-white">
      <ParticleNetwork />

      <div className="relative z-10 flex min-h-screen flex-col">
        <SiteNav />

        <main className="mx-auto flex w-full max-w-3xl flex-1 flex-col px-6 pb-24 pt-6 sm:px-10">
          <a
            href="/projects"
            className="animate-fade-up text-[11px] font-medium uppercase tracking-[0.22em] text-white/50 transition-opacity hover:text-white/80"
          >
            ← Projects
          </a>

          <div className="animate-fade-up-delay mt-8 overflow-hidden border border-white/10">
            <Image
              src="/projects/loan-book/cover.png"
              alt="Loan Book Diversification cover"
              width={1600}
              height={900}
              className="h-auto w-full object-contain"
              priority
            />
          </div>

          <header className="animate-fade-up-delay-2 mt-10">
            <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
              Loan Book Diversification
            </h1>
            <p className="mt-3 text-sm tracking-wide text-white/55">
              Python · NumPy · Credit Risk · Monte Carlo
            </p>
          </header>

          <p className="mt-6 text-sm leading-relaxed tracking-wide text-white/70 sm:text-[15px]">
            A Monte Carlo model of a loan book under independent defaults: each
            loan fails with a 2% probability and loses 40% of face value when it
            does. Running 5,000 simulated years across book sizes of 100, 1,000
            and 20,000 loans shows how idiosyncratic credit risk thins out as
            the portfolio grows.
          </p>

          <div className="mt-8 overflow-hidden border border-white/10 bg-black/40">
            <Image
              src="/projects/loan-book/loss-chart.png"
              alt="Chart comparing typical and bad-year loan book loss rates by portfolio size"
              width={1400}
              height={720}
              className="h-auto w-full object-contain"
            />
          </div>

          <section className="mt-10">
            <h2 className="border-b border-white/15 pb-2 text-[11px] font-medium uppercase tracking-[0.22em] text-white/55">
              Results
            </h2>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full min-w-[360px] text-left text-[13px]">
                <thead>
                  <tr className="border-b border-white/10 text-white/45">
                    <th className="py-2 pr-4 font-medium">Book size</th>
                    <th className="py-2 pr-4 font-medium">Typical year</th>
                    <th className="py-2 font-medium">Bad year (95th %ile)</th>
                  </tr>
                </thead>
                <tbody className="text-white/75">
                  {rows.map((row) => (
                    <tr key={row.loans} className="border-b border-white/5">
                      <td className="py-2.5 pr-4">{row.loans} loans</td>
                      <td className="py-2.5 pr-4">{row.typical}</td>
                      <td className="py-2.5 font-medium text-white">{row.bad}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>

          <section className="mt-10 space-y-3 text-sm leading-relaxed text-white/70">
            <h2 className="border-b border-white/15 pb-2 text-[11px] font-medium uppercase tracking-[0.22em] text-white/55">
              Takeaway
            </h2>
            <p>
              Average (typical) loss stays near 0.80% regardless of book size —
              expected credit loss does not change with diversification. The
              bad-year loss, however, almost halves from a 100-loan book to a
              20,000-loan book. That is the credit-risk case for diversification:
              same mean, thinner left tail.
            </p>
          </section>

          <a
            href="https://github.com/WilliamPotterDev/PortfolioWebsite/tree/main/notebooks/loan-book"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-10 inline-flex w-fit items-center gap-2 border border-white/25 px-4 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-white/90 transition-colors hover:border-white/60 hover:bg-white/5"
          >
            View notebook
            <span aria-hidden>→</span>
          </a>
        </main>
      </div>
    </div>
  );
}
