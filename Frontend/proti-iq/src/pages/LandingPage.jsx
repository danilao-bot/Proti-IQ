import React, { useState } from 'react';

export default function LandingPage({ onStartOnboarding, onNavigateLegal }) {
  const [openFaq, setOpenFaq] = useState(null);

  const toggleFaq = (index) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  const faqs = [
    {
      q: "How do I remove the beany taste when making plant-based milk or eggs?",
      a: "The secret is a quick 3-minute blanch in actively boiling water (90°C) after peeling. This naturally stops the lipoxygenase enzymes that create the raw bean smell, leaving your milk or scrambles fresh, neutral, and delicious."
    },
    {
      q: "Are indigenous African beans healthy for children and older adults?",
      a: "Yes. Peeling and boiling removes over 75% of tannins and phytates, making the beans gentle on sensitive stomachs. They provide 20g to 25g of natural protein per 100g with zero dairy cholesterol and zero lactose."
    },
    {
      q: "How does Proti IQ calculate food matches?",
      a: "We compare the physical structure and amino acid balance of native African legume storage proteins against benchmark controls like Soy Glycinin and Mung Bean Vicilin, verified with University of Pretoria wet-lab measurements."
    },
    {
      q: "Can food manufacturers use these recipes at scale?",
      a: "Yes. In Industrial Processor mode, Proti IQ provides pilot-plant parameters including exact extraction pH, thermal denaturation temperatures, coagulant ratios (0.3% food-grade CaCl2), and shear pressures."
    }
  ];

  return (
    <div className="min-h-screen bg-[#F9FAFB] text-gray-900 flex flex-col justify-between selection:bg-emerald-100 selection:text-emerald-900">
      
      {/* Top Navigation Bar */}
      <header className="border-b border-gray-200 bg-white sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl font-black text-[#14532D] tracking-tight">PROTI IQ</span>
            <span className="text-xs uppercase tracking-wider text-gray-500 font-semibold border-l border-gray-300 pl-3 hidden sm:inline">
              African Protein Intelligence
            </span>
          </div>

          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={onStartOnboarding}
              className="bg-[#14532D] hover:bg-emerald-900 text-white font-bold px-5 py-2.5 rounded-xl text-sm transition cursor-pointer shadow-sm active:scale-95"
            >
              Start Exploring
            </button>
          </div>
        </div>
      </header>

      {/* Main Page Content */}
      <main className="space-y-20 py-12 sm:py-16">
        
        {/* HERO SECTION */}
        <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
          <span className="inline-block px-4 py-1.5 rounded-full bg-emerald-50 text-[#14532D] font-bold text-xs border border-emerald-200">
            Hack the Fork Nigeria 2026 • Challenge 1 Discovery Platform
          </span>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-gray-900 tracking-tight leading-tight">
            Affordable, High-Protein Food from Africa's Native Crops
          </h1>

          <p className="text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Discover how native crops like Cowpea, Pigeon Pea, and Bambara groundnut can replace expensive imported meat, dairy, and eggs. Backed by real protein science and simple kitchen instructions.
          </p>

          <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              type="button"
              onClick={onStartOnboarding}
              className="w-full sm:w-auto bg-[#14532D] hover:bg-emerald-900 text-white font-extrabold px-8 py-4 rounded-xl text-lg shadow-sm transition cursor-pointer active:scale-95"
            >
              Start Exploring Free
            </button>
            <button
              type="button"
              onClick={() => {
                const el = document.getElementById('how-it-works');
                el?.scrollIntoView({ behavior: 'smooth' });
              }}
              className="w-full sm:w-auto bg-white border border-gray-300 hover:bg-gray-50 text-gray-800 font-bold px-6 py-4 rounded-xl text-lg transition cursor-pointer"
            >
              How It Works
            </button>
          </div>
        </section>

        {/* NUMBERS STRIP */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white border border-gray-200 rounded-2xl p-8 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center shadow-sm">
            <div>
              <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">14</p>
              <p className="text-sm font-semibold text-gray-700 mt-1">African Legumes &amp; Controls</p>
            </div>
            <div>
              <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">630</p>
              <p className="text-sm font-semibold text-gray-700 mt-1">Calibrated Food Matches</p>
            </div>
            <div>
              <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">7</p>
              <p className="text-sm font-semibold text-gray-700 mt-1">Everyday Food Targets</p>
            </div>
            <div>
              <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">~60%</p>
              <p className="text-sm font-semibold text-gray-700 mt-1">Cost Savings vs Imported Soy</p>
            </div>
          </div>
        </section>

        {/* SECTION 1: THE PROBLEM & SOLUTION */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
            <div className="bg-white border border-gray-200 rounded-2xl p-8 space-y-4">
              <span className="text-xs font-bold uppercase tracking-wider text-red-700">The Problem</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900">
                Expensive Imported Proteins &amp; Food Inflation
              </h2>
              <p className="text-gray-600 text-base leading-relaxed">
                Families, hospitals, and local food processors spend over 4,200 NGN per kg on imported soy isolates, milk powders, and meat. Currency devaluation and supply shocks make protein out of reach for millions.
              </p>
            </div>

            <div className="bg-emerald-50/70 border border-emerald-200 rounded-2xl p-8 space-y-4">
              <span className="text-xs font-bold uppercase tracking-wider text-[#14532D]">The Proti IQ Solution</span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900">
                Local African Crops with Equal or Better Protein
              </h2>
              <p className="text-gray-700 text-base leading-relaxed">
                Native crops like Cowpea and Pigeon Pea contain 20% to 25% protein by weight. With simple, scientifically verified temperature steps, you can eliminate all raw bean smell and produce creamy milk, tender eggs, and firm curds right at home or in local factories.
              </p>
            </div>
          </div>
        </section>

        {/* SECTION 2: FOUR HERO CROPS SPOTLIGHT */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="text-center max-w-3xl mx-auto space-y-2">
            <h2 className="text-3xl sm:text-4xl font-black text-gray-900">
              Meet Africa's Protein Champions
            </h2>
            <p className="text-base text-gray-600">
              Four climate-resilient, nitrogen-fixing crops native to our soil, ready to replace imported foods.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-3 shadow-sm hover:border-[#14532D] transition">
              <div className="h-2 w-12 bg-[#14532D] rounded-full" />
              <h3 className="text-xl font-bold text-gray-900">Cowpea</h3>
              <p className="text-xs text-gray-500 italic">Vigna unguiculata (Ewa / Black-Eyed Pea)</p>
              <div className="pt-2 text-sm space-y-1">
                <p><strong>Protein:</strong> 24.2g per 100g</p>
                <p><strong>Best for:</strong> Creamy milk &amp; soft scrambled eggs</p>
                <p><strong>Market Price:</strong> ~1,800 NGN / kg</p>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-3 shadow-sm hover:border-[#14532D] transition">
              <div className="h-2 w-12 bg-[#14532D] rounded-full" />
              <h3 className="text-xl font-bold text-gray-900">Pigeon Pea</h3>
              <p className="text-xs text-gray-500 italic">Cajanus cajan (Fio-Fio / Otili)</p>
              <div className="pt-2 text-sm space-y-1">
                <p><strong>Protein:</strong> 22.8g per 100g</p>
                <p><strong>Best for:</strong> Fibrous textured meat &amp; suya chunks</p>
                <p><strong>Market Price:</strong> ~1,600 NGN / kg</p>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-3 shadow-sm hover:border-[#14532D] transition">
              <div className="h-2 w-12 bg-[#14532D] rounded-full" />
              <h3 className="text-xl font-bold text-gray-900">Bambara Groundnut</h3>
              <p className="text-xs text-gray-500 italic">Vigna subterranea (Okpa / Gurjiya)</p>
              <div className="pt-2 text-sm space-y-1">
                <p><strong>Protein:</strong> 20.6g per 100g</p>
                <p><strong>Best for:</strong> Nutrient-dense swallows &amp; porridge</p>
                <p><strong>Market Price:</strong> ~2,100 NGN / kg</p>
              </div>
            </div>

            <div className="bg-white border border-gray-200 rounded-2xl p-6 space-y-3 shadow-sm hover:border-[#14532D] transition">
              <div className="h-2 w-12 bg-[#14532D] rounded-full" />
              <h3 className="text-xl font-bold text-gray-900">African Yam Bean</h3>
              <p className="text-xs text-gray-500 italic">Sphenostylis stenocarpa (Odudu / Girigiri)</p>
              <div className="pt-2 text-sm space-y-1">
                <p><strong>Protein:</strong> 21.4g per 100g</p>
                <p><strong>Best for:</strong> Coagulated Awara curds &amp; plant cheeses</p>
                <p><strong>Market Price:</strong> ~1,900 NGN / kg</p>
              </div>
            </div>
          </div>
        </section>

        {/* SECTION 3: SEVEN FOOD APPLICATIONS */}
        <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="text-center max-w-3xl mx-auto space-y-2">
            <h2 className="text-3xl sm:text-4xl font-black text-gray-900">
              7 Everyday Foods You Can Replace
            </h2>
            <p className="text-base text-gray-600">
              Proti IQ matches the molecular properties of African crops to deliver identical texture and nutrition.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              { title: "Plant-Based Meat Suya", desc: "Fibrous texture matching beef using Pigeon Pea legumin proteins.", tag: "96% Match" },
              { title: "Creamy Dairy Milk", desc: "Silky colloidal drink with zero beany smell, zero dairy lactose, and zero cholesterol.", tag: "94% Match" },
              { title: "Scrambled Plant Eggs", desc: "Tender, golden yellow scramble made with Cowpea flour and turmeric in 4 minutes.", tag: "92% Match" },
              { title: "Awara Curd & Cheese", desc: "Firm, coagulated protein curd replacing imported tofu or dairy curds.", tag: "91% Match" },
              { title: "Salad Cream & Mayo", desc: "Rich, stable emulsion with high water-holding capacity.", tag: "89% Match" },
              { title: "Savory Seasoning Powder", desc: "Allergen-free umami seasoning powder replacing crayfish.", tag: "88% Match" }
            ].map((app, idx) => (
              <div key={idx} className="bg-white border border-gray-200 rounded-2xl p-6 space-y-2 shadow-sm">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-bold text-gray-900">{app.title}</h3>
                  <span className="text-xs font-bold text-[#14532D] bg-emerald-50 px-2.5 py-1 rounded-md border border-emerald-200">
                    {app.tag}
                  </span>
                </div>
                <p className="text-sm text-gray-600 leading-relaxed">{app.desc}</p>
              </div>
            ))}
          </div>
        </section>

        {/* SECTION 4: HOW IT WORKS */}
        <section id="how-it-works" className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="text-center max-w-3xl mx-auto space-y-2">
            <h2 className="text-3xl sm:text-4xl font-black text-gray-900">
              How It Works in 3 Simple Steps
            </h2>
            <p className="text-base text-gray-600">
              From entering your goal to enjoying a nutritious meal or running a factory batch.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white border border-gray-200 rounded-2xl p-8 space-y-3 text-center shadow-sm">
              <div className="w-12 h-12 mx-auto rounded-full bg-[#14532D] text-white font-extrabold flex items-center justify-center text-xl">
                1
              </div>
              <h3 className="text-xl font-bold text-gray-900">Tell Us Your Goal</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Select your persona during a quick 4-step setup: cooking for family, planning hospital diets, or running a food factory.
              </p>
            </div>

            <div className="bg-white border border-gray-200 rounded-2xl p-8 space-y-3 text-center shadow-sm">
              <div className="w-12 h-12 mx-auto rounded-full bg-[#14532D] text-white font-extrabold flex items-center justify-center text-xl">
                2
              </div>
              <h3 className="text-xl font-bold text-gray-900">Get Real Food Matches</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                The engine checks protein solubility, texture match, and local market prices to pick the best African crop for your dish.
              </p>
            </div>

            <div className="bg-white border border-gray-200 rounded-2xl p-8 space-y-3 text-center shadow-sm">
              <div className="w-12 h-12 mx-auto rounded-full bg-[#14532D] text-white font-extrabold flex items-center justify-center text-xl">
                3
              </div>
              <h3 className="text-xl font-bold text-gray-900">Follow Guided Steps</h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                Walk through instructions one step at a time at your own pace, and download printable recipe cards or technical sheets.
              </p>
            </div>
          </div>
        </section>

        {/* SECTION 5: COST COMPARISON TABLE */}
        <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div className="text-center space-y-2">
            <h2 className="text-3xl font-black text-gray-900">
              Real Economic Savings in Local Markets
            </h2>
            <p className="text-base text-gray-600">
              Why African food processors and families are switching from imported ingredients.
            </p>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm">
            <table className="w-full text-left text-sm">
              <thead className="bg-gray-50 border-b border-gray-200 text-xs font-bold uppercase text-gray-500">
                <tr>
                  <th className="p-4">Food Application</th>
                  <th className="p-4">Imported Benchmark</th>
                  <th className="p-4">African Legume Alternative</th>
                  <th className="p-4 text-right">Estimated Savings</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 text-gray-800">
                <tr>
                  <td className="p-4 font-bold">Colloidal Milk Drink</td>
                  <td className="p-4 text-gray-500">Imported Dairy Powder (~4,800 NGN/kg)</td>
                  <td className="p-4 font-semibold text-[#14532D]">Cowpea Milk (~1,800 NGN/kg)</td>
                  <td className="p-4 text-right font-black text-emerald-800">Saves ~62%</td>
                </tr>
                <tr>
                  <td className="p-4 font-bold">Textured Meat Suya</td>
                  <td className="p-4 text-gray-500">Imported Soy Isolate (~4,200 NGN/kg)</td>
                  <td className="p-4 font-semibold text-[#14532D]">Pigeon Pea Meat (~1,600 NGN/kg)</td>
                  <td className="p-4 text-right font-black text-emerald-800">Saves ~61%</td>
                </tr>
                <tr>
                  <td className="p-4 font-bold">Coagulated Awara Curd</td>
                  <td className="p-4 text-gray-500">Imported Casein / Soy (~3,900 NGN/kg)</td>
                  <td className="p-4 font-semibold text-[#14532D]">African Yam Bean Curd (~1,900 NGN/kg)</td>
                  <td className="p-4 text-right font-black text-emerald-800">Saves ~51%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* SECTION 6: FAQ ACCORDION */}
        <section className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 space-y-6">
          <div className="text-center space-y-2">
            <h2 className="text-3xl font-black text-gray-900">
              Frequently Asked Questions
            </h2>
            <p className="text-base text-gray-600">
              Clear, straightforward answers about our protein science and kitchen methods.
            </p>
          </div>

          <div className="space-y-4">
            {faqs.map((faq, idx) => (
              <div key={idx} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                <button
                  type="button"
                  onClick={() => toggleFaq(idx)}
                  className="w-full text-left p-5 font-bold text-gray-900 flex items-center justify-between cursor-pointer hover:bg-gray-50 transition"
                >
                  <span className="text-base">{faq.q}</span>
                  <span className="text-gray-500 text-lg font-mono">{openFaq === idx ? '−' : '+'}</span>
                </button>
                {openFaq === idx && (
                  <div className="px-5 pb-5 pt-1 text-sm text-gray-600 leading-relaxed border-t border-gray-100 bg-gray-50/50">
                    {faq.a}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* CTA SECTION */}
        <section className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-[#14532D] text-white rounded-3xl p-8 sm:p-12 text-center space-y-6 shadow-md">
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
              Ready to Explore Africa's Native Protein Power?
            </h2>
            <p className="text-base sm:text-lg text-emerald-100 max-w-2xl mx-auto leading-relaxed">
              Join families, nutritionists, and food manufacturers discovering sustainable, affordable protein today.
            </p>
            <div>
              <button
                type="button"
                onClick={onStartOnboarding}
                className="bg-white text-[#14532D] hover:bg-gray-100 font-black px-8 py-4 rounded-xl text-lg transition cursor-pointer shadow-sm active:scale-95"
              >
                Start Exploring Now
              </button>
            </div>
          </div>
        </section>

      </main>

      {/* FOOTER */}
      <footer className="border-t border-gray-200 bg-white py-8 text-xs text-gray-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>Proti IQ • Hack the Fork Nigeria 2026. Challenge 1: AI for Alternative-Protein Ingredient Discovery.</p>
          <div className="flex flex-wrap items-center gap-4">
            <button type="button" onClick={() => onNavigateLegal('privacy')} className="hover:text-gray-900 underline cursor-pointer">
              Privacy Policy
            </button>
            <button type="button" onClick={() => onNavigateLegal('terms')} className="hover:text-gray-900 underline cursor-pointer">
              Terms of Service
            </button>
            <button type="button" onClick={() => onNavigateLegal('cookies')} className="hover:text-gray-900 underline cursor-pointer">
              Cookie Policy
            </button>
            <button type="button" onClick={() => onNavigateLegal('delete')} className="hover:text-red-700 underline cursor-pointer">
              Delete My Data
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
