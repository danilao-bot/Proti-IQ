// src/components/flows/ConsumerFlow.jsx
import { useState } from 'react';
import FlowHeader from '../FlowHeader';
import CropRankingBoard from '../CropRankingBoard';
import {
  AFRICAN_CROPS,
  TARGET_APPLICATIONS,
  rankCropsForTarget,
  formatLocalCurrency,
} from '../../data/protiData';
import { requestAdvisory } from '../../services/apiClient';

export default function ConsumerFlow({ country, market, onOpenEvidence, onSwitchRole }) {
  const [step, setStep] = useState(1);
  const [selectedTargetId, setSelectedTargetId] = useState('milk');
  const [customGoal, setCustomGoal] = useState('');
  const [availableCropIds, setAvailableCropIds] = useState([]); // empty = screen all 8
  const [chosenCrop, setChosenCrop] = useState(AFRICAN_CROPS[0]);
  const [aiAdvisory, setAiAdvisory] = useState(null);
  const [loadingAi, setLoadingAi] = useState(false);

  const activeTarget =
    TARGET_APPLICATIONS.find((t) => t.id === selectedTargetId) || TARGET_APPLICATIONS[0];

  const goalTitle = customGoal.trim() ? customGoal.trim() : activeTarget.label;

  const rankedCrops = rankCropsForTarget({
    targetId: selectedTargetId,
    customGoal,
    availableCropIds,
  });

  const toggleCropFilter = (id) => {
    setAvailableCropIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const handleStartScreening = (targetIdOverride = null) => {
    if (targetIdOverride) {
      setSelectedTargetId(targetIdOverride);
    }
    setStep(2);
  };

  const handleSelectCrop = (crop) => {
    setChosenCrop(crop);
    setStep(3);
  };

  // Dynamic savings estimate vs imported/animal benchmark
  const estimatedSavingsNaira = Math.max(1200, 4200 - chosenCrop.baseCostNairaKg);

  const handleFetchAiAdvisory = async () => {
    setLoadingAi(true);
    try {
      const res = await requestAdvisory({
        role: 'consumer',
        job: selectedTargetId,
        cropId: chosenCrop.id,
      });
      if (res && res.ai_generative_advisory) {
        setAiAdvisory(res);
      } else {
        setAiAdvisory({
          ai_generative_advisory: `For ${chosenCrop.name} in ${activeTarget.label}, blanch de-hulled seeds at 90°C for 3 minutes to destroy lipoxygenase enzymes and eliminate beany off-flavors, then wet-mill at 1:6 ratio for smooth culinary suspension.`,
          ai_provider: 'Proti IQ Rule Engine'
        });
      }
    } catch {
      setAiAdvisory({
        ai_generative_advisory: `Blanch de-hulled ${chosenCrop.name} seeds at 90°C for 3 minutes before blending to guarantee zero beany aroma.`,
        ai_provider: 'Proti IQ Fallback'
      });
    } finally {
      setLoadingAi(false);
    }
  };

  return (
    <div className="space-y-6">
      <FlowHeader
        flowLabel="CONSUMER & CAREGIVER DISCOVERY"
        step={step}
        totalSteps={4}
        onBack={() => setStep((s) => Math.max(1, s - 1))}
        onReset={() => {
          setStep(1);
          setCustomGoal('');
          setAvailableCropIds([]);
        }}
      />

      {/* SCREEN 1: BROAD GOAL + AVAILABLE CROPS */}
      {step === 1 && (
        <section className="space-y-6">
          <div className="text-center space-y-2">
            <span className="inline-block px-3.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-900 text-sm font-semibold">
              Africanized Alternative Protein Discovery
            </span>
            <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900">
              What plant-based protein do you want to make?
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Pick a target below or describe your own meal—our AI ranks the best African legumes for you.
            </p>
          </div>

          {/* 6 Broad Product Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {TARGET_APPLICATIONS.map((target) => {
              const isSelected = selectedTargetId === target.id && !customGoal.trim();
              return (
                <div
                  key={target.id}
                  onClick={() => {
                    setCustomGoal('');
                    setSelectedTargetId(target.id);
                  }}
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      setCustomGoal('');
                      setSelectedTargetId(target.id);
                    }
                  }}
                  className={`rounded-2xl p-5 border transition cursor-pointer flex flex-col justify-between gap-3 ${
                    isSelected
                      ? 'bg-white border-2 border-[#14532D] shadow-xs'
                      : 'bg-white border-gray-200 hover:border-gray-400'
                  }`}
                >
                  <div className="space-y-1.5">
                    <span className="text-[11px] font-bold uppercase tracking-wider text-amber-800 bg-amber-50 px-2 py-0.5 rounded">
                      {target.category}
                    </span>
                    <h2 className="text-xl font-bold text-gray-900">{target.label}</h2>
                    <p className="text-sm sm:text-base text-gray-600">{target.description}</p>
                  </div>
                  <p className="text-xs font-semibold text-gray-500 pt-2 border-t border-gray-100">
                    Replaces: {target.benchmark}
                  </p>
                </div>
              );
            })}
          </div>

          {/* Custom Goal Input + Optional Available Crops Filter */}
          <div className="bg-white border border-gray-200 rounded-2xl p-5 sm:p-6 space-y-5">
            <div className="space-y-2">
              <label htmlFor="custom-goal" className="block text-base font-bold text-gray-900">
                Or describe a custom plant-based food you want to create (Optional)
              </label>
              <input
                id="custom-goal"
                type="text"
                value={customGoal}
                onChange={(e) => setCustomGoal(e.target.value)}
                placeholder="e.g., High-protein moi-moi binder, creamy pap milk, dairy-free custard..."
                className="w-full px-4 py-3 rounded-xl border border-gray-300 text-base focus:outline-none focus:ring-2 focus:ring-[#14532D]"
              />
            </div>

            <div className="space-y-2.5">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-base font-bold text-gray-900">
                  Filter by African crops you have available (Optional)
                </span>
                <span className="text-xs font-semibold text-gray-500">
                  {availableCropIds.length === 0
                    ? 'Screening all 8 African legumes'
                    : `${availableCropIds.length} crop(s) selected`}
                </span>
              </div>

              <div className="flex flex-wrap gap-2">
                {AFRICAN_CROPS.map((crop) => {
                  const active = availableCropIds.includes(crop.id);
                  return (
                    <button
                      key={crop.id}
                      type="button"
                      onClick={() => toggleCropFilter(crop.id)}
                      className={`px-3.5 py-2 rounded-xl text-sm font-semibold border transition cursor-pointer ${
                        active
                          ? 'bg-[#14532D] text-white border-[#14532D]'
                          : 'bg-[#FAF9F6] text-gray-800 border-gray-300 hover:bg-gray-100'
                      }`}
                    >
                      {active ? '✓ ' : '+ '}
                      {crop.name}
                    </button>
                  );
                })}
              </div>
            </div>

            <button
              type="button"
              onClick={() => handleStartScreening()}
              className="w-full py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white text-lg font-bold transition cursor-pointer"
            >
              Rank Best African Crops for “{goalTitle}” &gt;
            </button>
          </div>
        </section>
      )}

      {/* SCREEN 2: AI RANKING BOARD (TOP 3 + FULL LIST) */}
      {step === 2 && (
        <section className="space-y-5">
          <div className="space-y-1">
            <p className="text-sm font-bold uppercase tracking-wider text-[#14532D]">
              Target: {goalTitle}
            </p>
            <h1 className="text-3xl font-extrabold text-gray-900">
              AI-Ranked African Protein Matches
            </h1>
          </div>

          <CropRankingBoard
            rankedCrops={rankedCrops}
            market={market}
            goalTitle={goalTitle}
            focusReason={activeTarget.focusReason}
            actionLabel="Get Recipe & Prep Guide"
            onSelectCrop={handleSelectCrop}
            onOpenEvidence={onOpenEvidence}
          />
        </section>
      )}

      {/* SCREEN 3: PREPARATION GUIDE */}
      {step === 3 && (
        <section className="space-y-6">
          <div className="space-y-1">
            <p className="text-sm font-bold uppercase tracking-wider text-amber-800">
              {chosenCrop.name} • {goalTitle}
            </p>
            <h1 className="text-3xl font-extrabold text-gray-900">
              Step-by-Step Preparation Guide
            </h1>
          </div>

          <div className="space-y-4">
            {chosenCrop.prepSteps.map((s, idx) => (
              <div
                key={idx}
                className="bg-white border border-gray-200 rounded-2xl p-5 sm:p-6 flex items-start gap-4"
              >
                <div className="w-10 h-10 rounded-full bg-[#14532D] text-white font-extrabold flex items-center justify-center text-lg shrink-0">
                  {idx + 1}
                </div>
                <div className="space-y-1">
                  <h2 className="text-xl font-bold text-gray-900">{s.title}</h2>
                  <p className="text-base sm:text-lg text-gray-600">{s.detail}</p>
                </div>
              </div>
            ))}
          </div>

          <button
            type="button"
            onClick={() => setStep(4)}
            className="w-full py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white text-lg font-bold transition cursor-pointer"
          >
            See Nutrition &amp; Cost Savings &gt;
          </button>
        </section>
      )}

      {/* SCREEN 4: SAVINGS & HEALTH SUMMARY */}
      {step === 4 && (
        <section className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 text-center space-y-6">
          <span className="inline-block px-3.5 py-1 rounded-full bg-emerald-50 text-emerald-900 text-sm font-bold">
            {country} Impact Summary • {chosenCrop.name}
          </span>

          <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900">
            Saves ~{formatLocalCurrency(estimatedSavingsNaira, market)}/kg vs. imported animal/soy benchmarks
          </h1>

          <p className="text-lg text-gray-700 max-w-xl mx-auto">
            Delivers <strong>{chosenCrop.proteinPer100g}g protein per 100g</strong> with{' '}
            <strong>zero dairy cholesterol</strong>, zero lactose, and{' '}
            <strong>{chosenCrop.solubilityPct}% natural solubility</strong>.
          </p>

          {/* AI Formulation Advisory Section */}
          <div className="bg-emerald-50/60 border border-emerald-200 rounded-2xl p-6 text-left space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-800">
                  AI Culinary Formulation Advisory
                </span>
                <p className="text-sm text-gray-600">
                  Powered by Groq Cloud &amp; Meta ESM-2 biophysical rules
                </p>
              </div>
              <button
                type="button"
                onClick={handleFetchAiAdvisory}
                disabled={loadingAi}
                className="px-4 py-2 rounded-lg bg-[#14532D] hover:bg-emerald-900 text-white font-semibold text-sm transition cursor-pointer disabled:opacity-50"
              >
                {loadingAi ? 'Generating Advisory...' : 'Consult Proti IQ AI'}
              </button>
            </div>

            {aiAdvisory && (
              <div className="pt-3 border-t border-emerald-200 text-sm text-gray-800 space-y-2">
                <p className="font-medium whitespace-pre-line leading-relaxed">
                  {aiAdvisory.ai_generative_advisory}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500 pt-1">
                  <span>Engine: {aiAdvisory.ai_provider}</span>
                  <span>Target: {activeTarget.label}</span>
                </div>
              </div>
            )}
          </div>

          <div className="pt-3 flex flex-col sm:flex-row justify-center gap-3">
            <button
              type="button"
              onClick={() => setStep(1)}
              className="py-3.5 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white text-base font-bold cursor-pointer"
            >
              Explore Another Protein Target
            </button>
            <button
              type="button"
              onClick={() => onSwitchRole('nutritionist')}
              className="py-3.5 px-6 rounded-xl border border-gray-300 bg-white hover:bg-gray-50 text-gray-900 text-base font-bold cursor-pointer"
            >
              Open Nutritionist Planner
            </button>
          </div>
        </section>
      )}
    </div>
  );
}