import Image from "next/image";
import ParticleNetwork from "@/components/ParticleNetwork";
import SiteNav from "@/components/SiteNav";

export default function ProjectsPage() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-[#0b0b0b] text-white">
      <ParticleNetwork />

      <div className="relative z-10 flex min-h-screen flex-col">
        <SiteNav />

        <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col px-6 pb-20 pt-6 sm:px-10">
          <p className="animate-fade-up text-[11px] font-medium uppercase tracking-[0.22em] text-white/50">
            Projects
          </p>

          <article className="animate-fade-up-delay mt-10">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">
                  Implied Volatility Surface
                </h1>
                <p className="mt-3 text-sm tracking-wide text-white/55">
                  Python · Options · Black-Scholes · Plotly
                </p>
              </div>
              <div className="flex flex-wrap gap-3">
                <a
                  href="#iv-demo"
                  className="inline-flex w-fit items-center gap-2 border border-white/25 px-4 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-white/90 transition-colors hover:border-white/60 hover:bg-white/5"
                >
                  Watch demo
                  <span aria-hidden>↓</span>
                </a>
                <a
                  href="https://iv-surface-project.streamlit.app/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex w-fit items-center gap-2 border border-white/15 px-4 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-white/70 transition-colors hover:border-white/40 hover:text-white/90"
                >
                  Open app
                  <span aria-hidden>→</span>
                </a>
              </div>
            </div>

            <p className="mt-6 max-w-3xl text-sm leading-relaxed tracking-wide text-white/70 sm:text-[15px]">
              An interactive options analytics tool which pulls live market
              prices using various APIs, and generates implied volatility using
              an inverse Black-Scholes model. It maps out the full volatility
              surface and smile based on user inputted parameters. This was
              built to show how pricing, liquidity filters, and skew can be
              used to form a clearer read on market risk.
            </p>

            <div
              id="iv-demo"
              className="mt-8 overflow-hidden border border-white/10 bg-black/40"
            >
              {/* Animated GIF: keep unoptimized so frames are not flattened */}
              <img
                src="/projects/iv-surface-demo.gif"
                alt="Implied volatility surface demo walkthrough"
                className="h-auto w-full"
              />
            </div>
            <p className="mt-2 text-[11px] tracking-wide text-white/40">
              Instant demo · live app may take ~30s to wake on first open
            </p>

            <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
              <a
                href="https://iv-surface-project.streamlit.app/"
                target="_blank"
                rel="noopener noreferrer"
                className="block overflow-hidden border border-white/10 bg-black/40"
              >
                <Image
                  src="/projects/iv-surface.png"
                  alt="Implied volatility surface dashboard"
                  width={1200}
                  height={750}
                  className="h-auto w-full object-contain"
                  priority
                />
              </a>

              <a
                href="https://iv-surface-project.streamlit.app/"
                target="_blank"
                rel="noopener noreferrer"
                className="block overflow-hidden border border-white/10 bg-black/40"
              >
                <Image
                  src="/projects/iv-surface-smile.png"
                  alt="Call smile volatility plot"
                  width={1200}
                  height={750}
                  className="h-auto w-full object-contain"
                />
              </a>
            </div>
          </article>

          <article className="animate-fade-up-delay mt-20 border-t border-white/10 pt-16">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">
                  Silicon vs. Sentiment: SK Group Case Study
                </h2>
                <p className="mt-3 text-sm tracking-wide text-white/55">
                  Equity Research · SK Hynix · SK Telecom · AI
                </p>
              </div>
              <a
                href="/projects/sk-group"
                className="inline-flex w-fit items-center gap-2 border border-white/25 px-4 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-white/90 transition-colors hover:border-white/60 hover:bg-white/5"
              >
                Read article
                <span aria-hidden>→</span>
              </a>
            </div>

            <p className="mt-6 max-w-3xl text-sm leading-relaxed tracking-wide text-white/70 sm:text-[15px]">
              SK Hynix and SK Telecom have both rallied hard on AI. Only one of
              them has the earnings to show for it. Case study on the difference
              between fundamentals-driven and sentiment-driven AI exposure,
              using SK Group as the natural experiment.
            </p>

            <a
              href="/projects/sk-group"
              className="mt-8 block overflow-hidden border border-white/10 bg-black/40"
            >
              <Image
                src="/projects/sk-group-cover.png"
                alt="Silicon vs. Sentiment: SK Group Case Study cover"
                width={1600}
                height={900}
                className="h-auto w-full object-contain"
              />
            </a>
          </article>

          <article className="animate-fade-up-delay mt-20 border-t border-white/10 pt-16">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">
                  Equity Beta Estimation
                </h2>
                <p className="mt-3 text-sm tracking-wide text-white/55">
                  Python · Pandas · CRSP · Systematic Risk
                </p>
              </div>
              <a
                href="/projects/market-betas"
                className="inline-flex w-fit items-center gap-2 border border-white/25 px-4 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-white/90 transition-colors hover:border-white/60 hover:bg-white/5"
              >
                View project
                <span aria-hidden>→</span>
              </a>
            </div>

            <p className="mt-6 max-w-3xl text-sm leading-relaxed tracking-wide text-white/70 sm:text-[15px]">
              Estimated equity betas for Apple, Nvidia, Broadcom, Microsoft and
              Oracle from CRSP daily returns against the value-weighted market —
              ranking which names carry more systematic risk.
            </p>

            <a
              href="/projects/market-betas"
              className="mt-8 block overflow-hidden border border-white/10 bg-black/40"
            >
              <Image
                src="/projects/market-betas/cover.png"
                alt="Equity Beta Estimation cover"
                width={1600}
                height={900}
                className="h-auto w-full object-contain"
              />
            </a>
          </article>

          <article className="animate-fade-up-delay mt-20 border-t border-white/10 pt-16">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">
                  Loan Book Diversification
                </h2>
                <p className="mt-3 text-sm tracking-wide text-white/55">
                  Python · NumPy · Credit Risk · Monte Carlo
                </p>
              </div>
              <a
                href="/projects/loan-book"
                className="inline-flex w-fit items-center gap-2 border border-white/25 px-4 py-2 text-[11px] font-medium uppercase tracking-[0.18em] text-white/90 transition-colors hover:border-white/60 hover:bg-white/5"
              >
                View project
                <span aria-hidden>→</span>
              </a>
            </div>

            <p className="mt-6 max-w-3xl text-sm leading-relaxed tracking-wide text-white/70 sm:text-[15px]">
              Monte Carlo simulation of loan defaults showing that larger books
              keep the same average loss but cut bad-year tail risk — a clean
              demonstration of credit diversification.
            </p>

            <a
              href="/projects/loan-book"
              className="mt-8 block overflow-hidden border border-white/10 bg-black/40"
            >
              <Image
                src="/projects/loan-book/cover.png"
                alt="Loan Book Diversification cover"
                width={1600}
                height={900}
                className="h-auto w-full object-contain"
              />
            </a>
          </article>
        </main>
      </div>
    </div>
  );
}
