import { useState } from 'react';
import { formatLocalCurrency } from '../data/protiData';

export default function CropRankingBoard({
  rankedCrops,
  market,
  goalTitle,
  focusReason,
  actionLabel = 'Use This Crop',
  onSelectCrop,
  onOpenEvidence,
}) {
  const [showAll, setShowAll] = useState(true);
  const topThree = rankedCrops.slice(0, 3);

  const buildEvidencePayload = (crop) => ({
    title: `${crop.name} (${crop.localNames})`,
    similarity: `${crop.matchScore}%`,
    confidence: crop.confidence,
    superfamily: crop.globulinFocus,
    metrics: [
      { label: 'Crude Protein Density', value: `${crop.proteinPer100g}g / 100g` },
      { label: 'Natural Solubility', value: `${crop.solubilityPct}%` },
      { label: 'Isoelectric Point (pI)', value: crop.pI },
      { label: 'GRAVY Hydropathicity', value: `${crop.gravy} (Hydrophilic)` },
      { label: 'Cysteine Fraction', value: crop.cysteine },
      { label: 'Ground Truth Anchor', value: 'Meta ESM-2 650M + 348 UniProtKB Proteins' },
    ],
    summary: `Screened for "${goalTitle}". ${focusReason} Native origin: ${crop.origin}.`,
  });

  return (
    <div className="space-y-6">
      {/* AI Ranking Banner */}
      <div className="bg-emerald-50/80 border border-emerald-200 rounded-2xl p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <span className="text-xs font-extrabold uppercase tracking-wider text-[#14532D]">
            ESM-2 AI Ranking Complete • {rankedCrops.length} African Crops Screened
          </span>
          <p className="text-base text-gray-800 mt-0.5">{focusReason}</p>
        </div>
      </div>

      {/* TOP 3 PODIUM CARDS */}
      <div className="space-y-3">
        <h2 className="text-lg font-extrabold text-gray-900">
          Top {topThree.length} Recommended Crops to Maximize Your Protein
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {topThree.map((crop, idx) => {
            const isFirst = idx === 0;
            return (
              <div
                key={crop.id}
                className={`rounded-2xl p-5 flex flex-col justify-between gap-4 border transition ${
                  isFirst
                    ? 'bg-white border-2 border-[#14532D] shadow-sm'
                    : 'bg-white border-gray-200'
                }`}
              >
                <div className="space-y-3">
                  <div className="flex items-center justify-between gap-2">
                    <span
                      className={`text-xs font-extrabold uppercase px-2.5 py-1 rounded-full ${
                        isFirst
                          ? 'bg-[#14532D] text-white'
                          : 'bg-amber-100 text-amber-900'
                      }`}
                    >
                      #{idx + 1} {isFirst ? 'Best Match' : 'Top Pick'}
                    </span>
                    <span className="text-lg font-extrabold text-[#14532D]">
                      {crop.matchScore}% Match
                    </span>
                  </div>

                  <div>
                    <h3 className="text-xl font-extrabold text-gray-900">{crop.name}</h3>
                    <p className="text-xs font-medium text-gray-500 mt-0.5">{crop.localNames}</p>
                  </div>

                  <div className="flex flex-wrap gap-1.5">
                    {crop.strengths.slice(0, 2).map((tag) => (
                      <span
                        key={tag}
                        className="text-xs font-semibold px-2.5 py-1 rounded-lg bg-[#FAF9F6] border border-gray-200 text-gray-800"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  <div className="text-sm text-gray-700 pt-1 flex items-center justify-between border-t border-gray-100">
                    <span>Protein: <strong>{crop.proteinPer100g}g/100g</strong></span>
                    <span>Est: <strong>{formatLocalCurrency(crop.baseCostNairaKg, market)}/kg</strong></span>
                  </div>
                </div>

                <div className="space-y-2 pt-1">
                  <button
                    type="button"
                    onClick={() => onSelectCrop(crop)}
                    className={`w-full py-3 px-4 rounded-xl text-base font-bold transition cursor-pointer ${
                      isFirst
                        ? 'bg-[#14532D] hover:bg-emerald-900 text-white'
                        : 'bg-emerald-50 hover:bg-emerald-100 text-[#14532D] border border-emerald-200'
                    }`}
                  >
                    {actionLabel} &gt;
                  </button>
                  <button
                    type="button"
                    onClick={() => onOpenEvidence(buildEvidencePayload(crop))}
                    className="w-full py-2 text-xs font-bold text-gray-600 hover:text-gray-900 cursor-pointer"
                  >
                    View AI &amp; Lab Score
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* FULL RANKED LEADERBOARD (ALL SCREENED CROPS) */}
      <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden">
        <div className="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between">
          <div>
            <h3 className="text-lg font-extrabold text-gray-900">
              Complete African Crop Ranking ({rankedCrops.length} Candidates)
            </h3>
            <p className="text-sm text-gray-600">
              Compare every screened crop and pick any option you prefer.
            </p>
          </div>
          <button
            type="button"
            onClick={() => setShowAll((v) => !v)}
            className="px-3.5 py-2 rounded-xl border border-gray-300 text-sm font-bold text-gray-800 hover:bg-gray-50 cursor-pointer"
          >
            {showAll ? 'Hide Full List' : 'Show Full List'}
          </button>
        </div>

        {showAll && (
          <div className="divide-y divide-gray-200">
            {rankedCrops.map((crop, idx) => (
              <div
                key={crop.id}
                className="p-4 sm:px-5 flex flex-col sm:flex-row sm:items-center justify-between gap-3 hover:bg-[#FAF9F6]"
              >
                <div className="flex items-start sm:items-center gap-3.5">
                  <span className="w-8 h-8 rounded-full bg-gray-100 text-gray-800 font-extrabold text-sm flex items-center justify-center shrink-0">
                    #{idx + 1}
                  </span>
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="text-base sm:text-lg font-bold text-gray-900">
                        {crop.name}
                      </span>
                      <span className="text-xs font-bold px-2 py-0.5 rounded-full bg-emerald-50 text-[#14532D]">
                        {crop.matchScore}% AI Score
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">
                      {crop.proteinPer100g}g protein/100g • {crop.solubilityPct}% solubility •{' '}
                      {formatLocalCurrency(crop.baseCostNairaKg, market)}/kg
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-end sm:self-center">
                  <button
                    type="button"
                    onClick={() => onOpenEvidence(buildEvidencePayload(crop))}
                    className="px-3 py-2 rounded-xl border border-gray-300 text-xs sm:text-sm font-bold text-gray-700 hover:bg-white cursor-pointer"
                  >
                    Lab Data
                  </button>
                  <button
                    type="button"
                    onClick={() => onSelectCrop(crop)}
                    className="px-4 py-2 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white text-xs sm:text-sm font-bold cursor-pointer"
                  >
                    Select &gt;
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}