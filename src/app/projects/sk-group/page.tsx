import type { Metadata } from "next";
import Image from "next/image";
import ParticleNetwork from "@/components/ParticleNetwork";
import SiteNav from "@/components/SiteNav";

export const metadata: Metadata = {
  title: "Silicon vs. Sentiment: SK Group Case Study | William Potter",
  description:
    "A case study on SK Hynix and SK Telecom - structural AI exposure versus sentiment-driven re-rating.",
};

const paragraphs = [
  "In an era where artificial intelligence continues to surpass analyst expectations and dominate technology investing, it is important to realise the two distinct forces by which the industry causes the market to move.",
  "The SK Group ecosystem can be dissected to form a view of each force in action. SK Telecom and SK Hynix, the quasi-independent constituents of the group and the main focus of this case study, have both rallied on the AI hype train whilst providing very different opportunities for AI exposure. Their rallies appear to have occurred in tandem; however, their profit drivers diverge sharply: SK Hynix is anchored by tangible demand and backed by industry fundamentals, driving profit directly, while SK Telecom's core profit remains in the traditional, well-established industry of telecommunications; its AI-driven rally reflects sentiment rather than earnings.",
  "SK Hynix represents the purest expression of AI demand, translating industry-related innovation and manufacturing directly into earnings. This is evident in the company having closed FY2025 with revenue of 97.1 trillion won and operating profit of 47.2 trillion won, a 49% operating margin, with operating profit more than doubling year-on-year and revenue climbing nearly 50%. This can be attributed to the rise of HBM which was a marginal product line up until the late 2010s, with conventional DRAM and NAND flash accounting for the vast majority of the company's revenue; nevertheless, SK Hynix still invested heavily in HBM research and development for over a decade. This prepared it for the huge demand generative AI created for AI accelerators around 2023, with Hynix being the first in its industry to mass-produce both HBM3 and HBM3E which were major components of NVIDIA's H100 and H200 GPUs respectively. SK Hynix has continued to benefit from an accelerating demand for high-bandwidth memory. In just the first quarter of 2026, revenue reached approximately 52.6 trillion won, up 198% year-on-year, while operating profit rose to approximately 37.6 trillion won. This underscores the AI infrastructure build-out that continues to drive demand for the company's high-value memory products, for which it is often the only viable supplier capable of meeting both technological requirements and volume demand. Crucially, none of this growth is speculative with HBM having become a physical necessity in the AI supply chain, being a non-substitutable component in AI accelerators, so it can be concluded that Hynix's re-rating is a lagging indicator of realised performance, independent of the narrative which has driven the growth of its corporate cousin.",
  "SK Telecom's re-rating rests not on an expanding market for its services, but overwhelmingly on a single position: a $100 million investment into Anthropic's 2023 series C extension, made when Anthropic was valued at a mere $5 billion. Anthropic's valuation has since climbed to $965 billion following its May 2026 Series H round; this leaves SK Telecom's stake estimated at between $1 billion and $2.6 billion, and reportedly equivalent to around 18% of the company's entire market capitalisation as of July 2026. Whilst SK Telecom has a higher percentage of market cap held in an Anthropic stake than any other public company, which may appear to investors as an appealing opportunity to gain exposure to the world's most valuable privately held AI company, the investment case ultimately hinges on the continued appreciation of a single unlisted asset rather than any fundamental improvement in SK Telecom's underlying operating business. Moreover, under standard accounting treatment, the appreciation of the stake sits as unrealised comprehensive income and will not touch SK Telecom's reported profit unless it is sold, which management has signalled no urgency to do. This means the company's core telecommunication business will remain the actual source of reported earnings, and similar to the rest of the industry, it is a mature, low-growth base which has shown limited signs of independent acceleration. More recently, SK Telecom introduced further AI initiatives, notably an AWS-backed data centre targeting 1 trillion won in revenue by 2030. This announcement is set to act as a long-term catalyst for growth, and has already contributed to the share price of SK Telecom rising by 59% in only the first half of 2026. However, most of this rise is still attributed to the hype and growth around the company's stake in Anthropic. A rally of this size, built on the optionality of an unrealised asset rather than on operating performance, signals a clear disconnect between SKT's valuation and the fundamentals of the business it is actually being valued at. The re-rating is starker once it is benchmarked against the company's own valuation history: before their Anthropic stake drew market attention, it traded at a trailing P/E of roughly 9-11x, similar to any other telco company at the time, but today, its trailing P/E has surged past 50x. Even on a forward basis, which accounts for expected earnings growth, SKT trades at 17-22x, still above the 16x average forward P/E across wireless telecom peers in Asia. This re-rating is not associated with an increase in subscriber growth, an expansion of operations, or any margin gains within the telecommunications business. Even when treated purely as a proxy for Anthropic, SK Telecom's re-rating leaves it carrying a materially higher risk profile than either its core telecoms business or SK Hynix's structural AI exposure would justify.",
  "Placed side by side, analysis of the two companies presents a natural view of how AI is currently being priced across public markets. SK Hynix demonstrates the case of structural AI exposure: demand is first contracted, revenue is then booked, and margin expansion is verifiable each quarter in earnings reports. SK Telecom conversely demonstrates the opposite case, where AI exposure stems from the company's optionality: a single illiquid, unrealised stake accounts for a disproportionate share of enterprise value, while the operating business it sits alongside has not shown any comparable transformation, and has instead proven its rigidity in the mostly stagnant telecoms market. Nonetheless, SK Hynix could stall if the memory supercycle turns for reasons of evolving technologies or a genuine drop in demand, and SK Telecom's Anthropic stake could still deliver an outsized windfall at IPO. The core takeaway is that each stock carries fundamentally opposing risk profiles, obscured by their shared \"AI rally\" label. For investors, the distinction between silicon and sentiment is not academic: it determines whether a re-rating is supported by a balance sheet already reflecting reality, or by a valuation still waiting for one to arrive.",
];

export default function SkGroupCaseStudyPage() {
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
              src="/projects/sk-group-cover.png"
              alt="Silicon vs. Sentiment: SK Group Case Study cover"
              width={1600}
              height={900}
              className="h-auto w-full object-contain"
              priority
            />
          </div>

          <header className="animate-fade-up-delay-2 mt-10">
            <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-white/50">
              Equity Research · July 2026
            </p>
            <h1 className="mt-4 text-3xl font-semibold tracking-tight sm:text-4xl">
              Silicon vs. Sentiment: SK Group Case Study
            </h1>
            <p className="mt-3 text-sm tracking-wide text-white/55">
              Equity Research · SK Hynix · SK Telecom · AI
            </p>
          </header>

          <article className="mt-10 space-y-6 font-serif text-[15px] leading-8 text-white/80 sm:text-base sm:leading-8">
            {paragraphs.map((paragraph) => (
              <p key={paragraph.slice(0, 48)}>{paragraph}</p>
            ))}
          </article>
        </main>
      </div>
    </div>
  );
}
