import type { Metadata } from "next";
import Image from "next/image";
import ParticleNetwork from "@/components/ParticleNetwork";
import SiteNav from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Equity Beta Estimation | William Potter",
  description:
    "Estimating equity betas for major tech stocks from CRSP daily returns against the value-weighted market.",
};

const results = [
  { name: "Apple", ticker: "AAPL", beta: "1.30" },
  { name: "Nvidia", ticker: "NVDA", beta: "1.96" },
  { name: "Broadcom", ticker: "AVGO", beta: "1.92" },
  { name: "Microsoft", ticker: "MSFT", beta: "0.90" },
  { name: "Oracle", ticker: "ORCL", beta: "1.57" },
];

export default function MarketBetasPage() {
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
              src="/projects/market-betas/cover.png"
              alt="Equity Beta Estimation cover"
              width={1600}
              height={900}
              className="h-auto w-full object-contain"
              priority
            />
          </div>

          <header className="animate-fade-up-delay-2 mt-10">
            <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
              Equity Beta Estimation
            </h1>
            <p className="mt-3 text-sm tracking-wide text-white/55">
              Python · Pandas · CRSP · Systematic Risk
            </p>
          </header>

          <p className="mt-6 text-sm leading-relaxed tracking-wide text-white/70 sm:text-[15px]">
            A Python notebook that estimates equity betas for five large
            technology names using CRSP 2025 daily returns. Each stock&apos;s
            beta is the covariance of its total return with the
            value-weighted market return, divided by the market variance —
            the classic CAPM measure of systematic risk.
          </p>

          <div className="mt-8 overflow-hidden border border-white/10 bg-black/40">
            <Image
              src="/projects/market-betas/betas-chart.png"
              alt="Bar chart of equity betas for Apple, Nvidia, Broadcom, Microsoft and Oracle"
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
              <table className="w-full min-w-[320px] text-left text-[13px]">
                <thead>
                  <tr className="border-b border-white/10 text-white/45">
                    <th className="py-2 pr-4 font-medium">Company</th>
                    <th className="py-2 pr-4 font-medium">Ticker</th>
                    <th className="py-2 font-medium">Beta</th>
                  </tr>
                </thead>
                <tbody className="text-white/75">
                  {results.map((row) => (
                    <tr key={row.ticker} className="border-b border-white/5">
                      <td className="py-2.5 pr-4">{row.name}</td>
                      <td className="py-2.5 pr-4 text-white/50">{row.ticker}</td>
                      <td className="py-2.5 font-medium text-white">{row.beta}</td>
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
              Nvidia and Broadcom sit well above 1 — more market-sensitive than
              the average stock. Microsoft prints below 1, a lower-beta profile
              within the same sector cohort. The notebook isolates that ranking
              directly from returns data rather than relying on a third-party
              beta feed.
            </p>
          </section>

          <a
            href="https://github.com/WilliamPotterDev/PortfolioWebsite/tree/main/notebooks/market-betas"
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
