import { useState } from 'react';

const PRETORIA_EVALUATIONS = [
  {
    crop: 'Bambara Groundnut',
    accessionStatus: '0 UniProt Storage Globulins (Tier 1 Wet-Lab Only)',
    solubilityPH7: '82.27%',
    lgc: '8.0% - 10.0% w/v',
    crudeProtein: '21.5%',
    waterAbsorption: '2.3 g/g',
    oilAbsorption: '1.8 g/g',
    verifiedFunction: 'Ideal for colloidal plant-based milk and low-viscosity geriatric porridges.'
  },
  {
    crop: 'Cowpea (Black-eyed)',
    accessionStatus: '45 Sequenced Globulins in UniProtKB',
    solubilityPH7: '82.64%',
    lgc: '10.0% - 12.0% w/v',
    crudeProtein: '23.8%',
    waterAbsorption: '2.1 g/g',
    oilAbsorption: '1.6 g/g',
    verifiedFunction: 'High solubility at neutral pH; rapid 7S thermal gelation for egg alternatives and Akara.'
  },
  {
    crop: 'Pigeon Pea',
    accessionStatus: '87 Sequenced Globulins in UniProtKB',
    solubilityPH7: '76.40%',
    lgc: '12.0% - 14.0% w/v',
    crudeProtein: '22.4%',
    waterAbsorption: '1.9 g/g',
    oilAbsorption: '1.7 g/g',
    verifiedFunction: 'Highest sulfur-containing 11S legumin match for textured meat and protein swallows.'
  },
  {
    crop: 'African Yam Bean',
    accessionStatus: '28 Sequenced Globulins in UniProtKB',
    solubilityPH7: '68.50%',
    lgc: '6.0% - 8.0% w/v (Lowest / Firmest Gel)',
    crudeProtein: '24.6%',
    waterAbsorption: '2.4 g/g',
    oilAbsorption: '1.9 g/g',
    verifiedFunction: 'Forms the firmest coagulated curd under 0.3% CaCl2 cross-linking; optimal for Awara.'
  }
];

export default function EvidencePage() {
  const [selectedCrop, setSelectedCrop] = useState(PRETORIA_EVALUATIONS[0]);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 border border-[#E5E7EB] shadow-xs">
        <h1 className="text-2xl font-bold text-[#111827] tracking-tight">
          Empirical Wet-Lab Validation & University of Pretoria Dataset
        </h1>
        <p className="mt-2 text-sm text-[#4B5563]">
          Grounded in empirical laboratory testing (University of Pretoria, 2020). Every computational prediction in Proti IQ is anchored against real physical solubility, gelation, and texture measurements.
        </p>
      </div>

      {/* Scientific Integrity Highlight: Bambara Case Study */}
      <div className="bg-[#FEF3C7] border border-[#FDE68A] rounded-2xl p-5 text-[#92400E]">
        <div className="flex items-start gap-3">
          <div className="p-2 rounded-lg bg-[#F59E0B] text-white font-bold text-xs">
            INTEGRITY
          </div>
          <div>
            <h3 className="font-bold text-sm text-[#78350F]">
              Scientific Honesty: Why Bambara Groundnut Is Handled Differently
            </h3>
            <p className="text-xs text-[#92400E] mt-1 leading-relaxed">
              In UniProtKB, Bambara groundnut currently has <strong>zero reviewed seed storage globulin sequences</strong>. Rather than hallucinating speculative AI sequence scores, Proti IQ enforces a strict <strong>Tier 1 Wet-Lab Priority</strong> protocol, ranking Bambara strictly by its physical 82.27% solubility curve and 8%–10% Least Gelation Concentration from wet-lab trials.
            </p>
          </div>
        </div>
      </div>

      {/* Interactive Pretoria Wet-Lab Table */}
      <div className="bg-white rounded-2xl border border-[#E5E7EB] shadow-xs overflow-hidden">
        <div className="p-5 border-b border-[#F3F4F6] flex justify-between items-center">
          <h2 className="font-bold text-base text-[#111827]">
            Empirical Wet-Lab Functional Comparisons
          </h2>
          <span className="text-xs font-mono bg-[#F3F4F6] text-[#4B5563] px-2.5 py-1 rounded-md">
            Source: Pretoria M38-M42
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-[#FAF9F6] text-[#4B5563] border-b border-[#E5E7EB] uppercase text-[10px] tracking-wider font-semibold">
              <tr>
                <th className="py-3 px-4">African Legume</th>
                <th className="py-3 px-4">UniProt Status</th>
                <th className="py-3 px-4">pH 7 Solubility</th>
                <th className="py-3 px-4">Least Gelation (LGC)</th>
                <th className="py-3 px-4">Crude Protein</th>
                <th className="py-3 px-4">Primary Verified Application</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#F3F4F6]">
              {PRETORIA_EVALUATIONS.map((row) => (
                <tr
                  key={row.crop}
                  className={`hover:bg-[#FAF9F6] cursor-pointer transition-colors ${
                    selectedCrop.crop === row.crop ? 'bg-[#ECFDF5]' : ''
                  }`}
                  onClick={() => setSelectedCrop(row)}
                >
                  <td className="py-3.5 px-4 font-bold text-[#111827]">{row.crop}</td>
                  <td className="py-3.5 px-4 text-[#6B7280]">{row.accessionStatus}</td>
                  <td className="py-3.5 px-4 font-mono font-semibold text-[#059669]">
                    {row.solubilityPH7}
                  </td>
                  <td className="py-3.5 px-4 font-mono text-[#111827]">{row.lgc}</td>
                  <td className="py-3.5 px-4 font-mono text-[#111827]">{row.crudeProtein}</td>
                  <td className="py-3.5 px-4 text-[#4B5563]">{row.verifiedFunction}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Crop Laboratory Deep Dive */}
      <div className="bg-white rounded-2xl p-6 border border-[#E5E7EB] shadow-xs space-y-4">
        <h3 className="font-bold text-base text-[#111827]">
          Laboratory Dossier: {selectedCrop.crop}
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3 rounded-xl bg-[#FAF9F6] border border-[#E5E7EB]">
            <span className="text-[#6B7280] block">Water Absorption</span>
            <span className="font-mono font-bold text-[#111827] text-sm mt-0.5 block">
              {selectedCrop.waterAbsorption}
            </span>
          </div>
          <div className="p-3 rounded-xl bg-[#FAF9F6] border border-[#E5E7EB]">
            <span className="text-[#6B7280] block">Oil Absorption</span>
            <span className="font-mono font-bold text-[#111827] text-sm mt-0.5 block">
              {selectedCrop.oilAbsorption}
            </span>
          </div>
          <div className="p-3 rounded-xl bg-[#FAF9F6] border border-[#E5E7EB]">
            <span className="text-[#6B7280] block">Least Gelation (LGC)</span>
            <span className="font-mono font-bold text-[#059669] text-sm mt-0.5 block">
              {selectedCrop.lgc}
            </span>
          </div>
          <div className="p-3 rounded-xl bg-[#FAF9F6] border border-[#E5E7EB]">
            <span className="text-[#6B7280] block">Crude Protein Fraction</span>
            <span className="font-mono font-bold text-[#111827] text-sm mt-0.5 block">
              {selectedCrop.crudeProtein}
            </span>
          </div>
        </div>

        <p className="text-xs text-[#4B5563] leading-relaxed pt-2">
          <strong>Food Processing Recommendation:</strong> {selectedCrop.verifiedFunction}
        </p>
      </div>
    </div>
  );
}
