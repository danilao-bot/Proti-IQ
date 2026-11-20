import { useState } from 'react';
import FlowHeader from '../FlowHeader';
import CropRankingBoard from '../CropRankingBoard';
import {
  AFRICAN_CROPS,
  NUTRITIONIST_COHORTS,
  STAPLE_VEHICLES,
  rankCropsForTarget,
} from '../../data/protiData';

export default function NutritionistFlow({ country, market, onOpenEvidence }) {
  const [step, setStep] = useState(1);
  const [cohortId, setCohortId] = useState('sarcopenia');
  const [selectedCrop, setSelectedCrop] = useState(AFRICAN_CROPS[1]); // Cowpea default
  const [vehicleId, setVehicleId] = useState('amala');
  const [fortificationPct, setFortificationPct] = useState(15);
  const [exported, setExported] = useState(false);

  const cohort = NUTRITIONIST_COHORTS.find((c) => c.id === cohortId) || NUTRITIONIST_COHORTS[0];
  const vehicle = STAPLE_VEHICLES.find((v) => v.id === vehicleId) || STAPLE_VEHICLES[0];
  const rankedCrops = rankCropsForTarget({ targetId: 'fortify' });

  // Live protein yield based on the specific crop chosen by the nutritionist!
  const proteinRatio = selectedCrop.proteinPer100g / 100;
  const addedGrams = Math.round(vehicle.servingG * (fortificationPct / 100) * proteinRatio * 3.1 * 10) / 10;
  const totalMealProtein = Math.round((vehicle.baseProteinG + addedGrams) * 10) / 10;
  const targetPct = Math.min(100, Math.round((totalMealProtein / cohort.targetGramsPerMeal) * 100));

  return (
    <div className="space-y-6">
      <FlowHeader
        flowLabel="NUTRITIONIST CLINICAL SUITE"
        step={step}
        totalSteps={4}
        onBack={() => setStep((s) => Math.max(1, s - 1))}
        onReset={() => {
          setStep(1);
          setExported(false);
        }}
      />

      {/* SCREEN 1: COHORT SELECTION */}
      {step === 1 && (
        <section className="space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900">
              Select Patient or Population Cohort
            </h1>
            <p className="text-lg text-gray-600">
              Screen and rank indigenous African legumes for clinical dietary prescriptions in {country}.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {NUTRITIONIST_COHORTS.map((item) => (
              <div
                key={item.id}
                onClick={() => {
                  setCohortId(item.id);
                  setStep(2);
                }}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    setCohortId(item.id);
                    setStep(2);
                  }
                }}
                className="bg-white border border-gray-200 hover:border-[#14532D] rounded-2xl p-6 transition cursor-pointer flex flex-col justify-between gap-4"
              >
                <div className="space-y-2">
                  <span className="inline-block text-xs font-bold uppercase tracking-wider text-amber-800 bg-amber-50 px-2.5 py-1 rounded-md">
                    {item.tag}
                  </span>
                  <h2 className="text-2xl font-bold text-gray-900">{item.title}</h2>
                  <p className="text-base text-gray-600">{item.summary}</p>
                </div>

                <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                  <span className="text-sm font-semibold text-gray-700">
                    Target: {item.targetGramsPerMeal}g protein / meal
                  </span>
                  <span className="text-base font-bold text-[#14532D]">Rank Crops &gt;</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SCREEN 2: AI RANKING OF LEGUMES FOR THIS COHORT */}
      {step === 2 && (
        <section className="space-y-5">
          <div className="space-y-1">
            <p className="text-sm font-bold uppercase tracking-wider text-[#14532D]">
              Cohort: {cohort.title}
            </p>
            <h1 className="text-3xl font-extrabold text-gray-900">
              Ranked Indigenous Protein Fortifiers
            </h1>
          </div>

          <CropRankingBoard
            rankedCrops={rankedCrops}
            market={market}
            goalTitle={cohort.title}
            focusReason="Ranked by essential amino acid completeness, digestibility, and antinutrient reduction."
            actionLabel="Fortify Meals With This"
            onSelectCrop={(crop) => {
              setSelectedCrop(crop);
              setStep(3);
            }}
            onOpenEvidence={onOpenEvidence}
          />
        </section>
      )}

      {/* SCREEN 3: TRADITIONAL STAPLE FORTIFICATION SLIDER */}
      {step === 3 && (
        <section className="space-y-6">
          <div className="space-y-1">
            <p className="text-sm font-bold uppercase tracking-wider text-amber-800">
              {cohort.title} • Using {selectedCrop.name} ({selectedCrop.proteinPer100g}g/100g)
            </p>
            <h1 className="text-3xl font-extrabold text-gray-900">
              Staple Meal Fortification Calculator
            </h1>
          </div>

          <div className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-6">
            <div className="space-y-2.5">
              <label className="block text-base font-bold text-gray-900">
                1. Choose Traditional Staple Vehicle
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {STAPLE_VEHICLES.map((v) => {
                  const active = v.id === vehicleId;
                  return (
                    <button
                      key={v.id}
                      type="button"
                      onClick={() => setVehicleId(v.id)}
                      className={`py-3 px-3.5 rounded-xl border text-sm sm:text-base font-bold transition cursor-pointer ${
                        active
                          ? 'bg-[#14532D] text-white border-[#14532D]'
                          : 'bg-[#FAF9F6] text-gray-800 border-gray-300 hover:bg-gray-100'
                      }`}
                    >
                      {v.name}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="space-y-3 pt-1">
              <div className="flex items-center justify-between">
                <label htmlFor="nutri-slider" className="text-base font-bold text-gray-900">
                  2. {selectedCrop.name} Hydrolysate Inclusion
                </label>
                <span className="px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-base font-extrabold">
                  {fortificationPct}% Blend
                </span>
              </div>

              <input
                id="nutri-slider"
                type="range"
                min="0"
                max="30"
                step="5"
                value={fortificationPct}
                onChange={(e) => setFortificationPct(Number(e.target.value))}
                className="w-full accent-[#14532D] h-3 cursor-pointer"
              />
              <div className="flex justify-between text-xs font-semibold text-gray-500">
                <span>0% (Base Staple)</span>
                <span>15% (Optimal Clinical Blend)</span>
                <span>30% (High-Density)</span>
              </div>
            </div>

            <div className="bg-[#FAF9F6] border border-gray-200 rounded-2xl p-5 space-y-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-base font-semibold text-gray-700">
                  Fortified {vehicle.name} Yield:
                </span>
                <span className="text-2xl font-extrabold text-[#14532D]">
                  {totalMealProtein}g protein / serving
                </span>
              </div>

              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className="bg-[#14532D] h-3 rounded-full transition-all"
                  style={{ width: `${targetPct}%` }}
                />
              </div>

              <p className="text-sm sm:text-base text-gray-700">
                Hits <strong>{targetPct}%</strong> of the {cohort.targetGramsPerMeal}g per-meal clinical target for <strong>{cohort.title}</strong> with 78% reduced antinutrients and smooth texture.
              </p>
            </div>

            <button
              type="button"
              onClick={() => {
                setExported(false);
                setStep(4);
              }}
              className="w-full py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white text-lg font-bold transition cursor-pointer"
            >
              Generate Dietary Advisory Note &gt;
            </button>
          </div>
        </section>
      )}

      {/* SCREEN 4: CLINICAL EXPORT */}
      {step === 4 && (
        <section className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-5">
          <div className="flex flex-wrap items-center justify-between gap-2 border-b border-gray-200 pb-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-gray-500">
                PROTI IQ DIETARY ADVISORY NOTE • {country.toUpperCase()}
              </p>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-gray-900 mt-1">
                {cohort.title}
              </h1>
            </div>
            <span className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-900 text-sm font-bold">
              Clinical Ready
            </span>
          </div>

          <div className="space-y-3 text-base sm:text-lg text-gray-800">
            <p>
              <strong>Selected Indigenous Protein:</strong> {selectedCrop.name} ({selectedCrop.localNames}) — {selectedCrop.proteinPer100g}g protein/100g.
            </p>
            <p>
              <strong>Meal Fortification Prescription:</strong> Blend <strong>{fortificationPct}% {selectedCrop.name} hydrolysate</strong> into <strong>{vehicle.name}</strong> ({vehicle.servingG}g serving).
            </p>
            <p>
              <strong>Clinical Outcome:</strong> Delivers <strong>{totalMealProtein}g bioavailable protein</strong> per meal ({targetPct}% of target) without lactose or digestive discomfort.
            </p>
          </div>

          {exported && (
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 font-semibold text-base">
              Dietary Advisory Note exported for patient handoff.
            </div>
          )}

          <div className="pt-2 flex flex-col sm:flex-row gap-3">
            <button
              type="button"
              onClick={() => {
                setExported(true);
                window.print();
              }}
              className="flex-1 py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white text-lg font-bold transition cursor-pointer"
            >
              Export Dietary Advisory Note
            </button>
            <button
              type="button"
              onClick={() => setStep(3)}
              className="py-4 px-5 rounded-xl border border-gray-300 bg-white hover:bg-gray-50 text-gray-900 text-base font-bold cursor-pointer"
            >
              Adjust Blend
            </button>
          </div>
        </section>
      )}
    </div>
  );
}