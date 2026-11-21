import React from 'react';

export default function LandingPage({ onStartOnboarding, onNavigateLegal }) {
  return (
    <div className="min-h-screen bg-[#F9FAFB] text-gray-900 flex flex-col justify-between">
      {/* Top Brand Bar */}
      <header className="border-b border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl font-black text-[#14532D] tracking-tight">PROTI IQ</span>
            <span className="text-xs uppercase tracking-wider text-gray-500 font-semibold border-l border-gray-300 pl-3">
              Precision Protein Intelligence
            </span>
          </div>
          <button
            type="button"
            onClick={onStartOnboarding}
            className="bg-[#14532D] hover:bg-emerald-900 text-white font-bold px-5 py-2.5 rounded-lg text-sm transition cursor-pointer"
          >
            Start Discovery &gt;
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 space-y-16">
        {/* Hero Section */}
        <section className="text-center max-w-4xl mx-auto space-y-6">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-gray-900 tracking-tight leading-tight">
            Precision Protein Intelligence for Africa's Indigenous Crops
          </h1>
          <p className="text-lg sm:text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Screening 14 native legumes against 7 commercial food benchmarks using Meta ESM-2 biophysical embeddings and University of Pretoria empirical wet-lab data.
          </p>
          <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button
              type="button"
              onClick={onStartOnboarding}
              className="w-full sm:w-auto bg-[#14532D] hover:bg-emerald-900 text-white font-extrabold px-8 py-4 rounded-xl text-lg shadow-sm transition cursor-pointer"
            >
              Start Discovery
            </button>
            <button
              type="button"
              onClick={() => onNavigateLegal('terms')}
              className="w-full sm:w-auto bg-white border border-gray-300 hover:bg-gray-50 text-gray-800 font-bold px-6 py-4 rounded-xl text-lg transition cursor-pointer"
            >
              Read Scientific Scope
            </button>
          </div>
        </section>

        {/* Defensible Numbers Strip */}
        <section className="border-t border-b border-gray-200 py-8 grid grid-cols-2 lg:grid-cols-4 gap-6 text-center">
          <div>
            <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">14</p>
            <p className="text-sm font-semibold text-gray-600 mt-1">Sequenced Legumes &amp; Controls</p>
          </div>
          <div>
            <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">630</p>
            <p className="text-sm font-semibold text-gray-600 mt-1">Calibrated Job Rankings</p>
          </div>
          <div>
            <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">1,280</p>
            <p className="text-sm font-semibold text-gray-600 mt-1">ESM-2 Vector Dimensions</p>
          </div>
          <div>
            <p className="text-3xl sm:text-4xl font-black text-[#14532D] tabular-nums">7</p>
            <p className="text-sm font-semibold text-gray-600 mt-1">Alternative-Protein Target Jobs</p>
          </div>
        </section>

        {/* Core Capabilities */}
        <section className="space-y-8">
          <div className="text-center space-y-2">
            <h2 className="text-2xl sm:text-3xl font-extrabold text-gray-900">
              Three Pillars of Defensible Protein Replacement
            </h2>
            <p className="text-base text-gray-600">
              Rigorous biophysical computation paired with wet-lab validation and practical food formulation.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-3">
              <h3 className="text-xl font-bold text-gray-900">1. Biophysical Protein Screening</h3>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
                Compares molecular weight, isoelectric point, net surface charge, hydrophobicity, and cysteine disulfide potential of African legume storage globulins against commercial soy and mung bean benchmarks.
              </p>
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-3">
              <h3 className="text-xl font-bold text-gray-900">2. AI-Powered Formulation Advisory</h3>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
                Generates role-specific processing parameters calibrated to your facility type, from household kitchen thermal enzyme de-flavoring to industrial extrusion shear pressure specifications.
              </p>
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-3">
              <h3 className="text-xl font-bold text-gray-900">3. Empirical Wet-Lab Validation</h3>
              <p className="text-gray-600 text-sm sm:text-base leading-relaxed">
                Every computational prediction is cross-checked against University of Pretoria laboratory measurements: solubility curves, least gelation concentrations, and water/oil absorption capacities.
              </p>
            </div>
          </div>
        </section>

        {/* Target Audience Descriptions */}
        <section className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-6">
          <h2 className="text-xl font-extrabold text-gray-900 border-b border-gray-200 pb-3">
            Configured for Four Operational Personas
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 text-sm text-gray-700">
            <div>
              <p className="font-bold text-gray-900 mb-1">Consumer &amp; Caregiver</p>
              <p>For families and caregivers managing affordable, nutritious plant-based meals with specific de-flavoring steps and geriatric swallow safety guidance.</p>
            </div>
            <div>
              <p className="font-bold text-gray-900 mb-1">Clinical Nutritionist &amp; Dietitian</p>
              <p>For dietitians formulating therapeutic meal fortifications for sarcopenic older adults and malnourished cohorts using leucine thresholds.</p>
            </div>
            <div>
              <p className="font-bold text-gray-900 mb-1">Industrial Food Manufacturer</p>
              <p>For ingredient processors replacing imported soy and whey with local crops using exact denaturation temperatures, pH-shifting, and shear metrics.</p>
            </div>
            <div>
              <p className="font-bold text-gray-900 mb-1">Research Scientist &amp; Academic</p>
              <p>For molecular biophysicists analyzing 1,280-dimensional ESM-2 embeddings, AlphaFold coordinates, and raw wet-lab titration tables.</p>
            </div>
          </div>
        </section>
      </main>

      {/* Legal Footer */}
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
