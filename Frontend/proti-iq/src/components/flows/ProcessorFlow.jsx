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

const INDUSTRIAL_LINES = TARGET_APPLICATIONS.filter((t) =>
  ['meat', 'egg', 'milk', 'wara'].includes(t.id)
);

export default function ProcessorFlow({ country, market, onOpenEvidence }) {
  const [step, setStep] = useState(1);
  const [lineId, setLineId] = useState('meat');
  const [selectedCrop, setSelectedCrop] = useState(AFRICAN_CROPS[2]); // African Yam Bean default
  const [downloaded, setDownloaded] = useState(false);
  const [aiAdvisory, setAiAdvisory] = useState(null);
  const [loadingAi, setLoadingAi] = useState(false);

  const activeLine = INDUSTRIAL_LINES.find((l) => l.id === lineId) || INDUSTRIAL_LINES[0];
  const rankedCrops = rankCropsForTarget({ targetId: lineId });

  const importedBenchmarkCost = formatLocalCurrency(4200, market);
  const localCropCost = formatLocalCurrency(selectedCrop.baseCostNairaKg, market);

  const handleDownloadTDS = () => {
    const text = [
      `PROTI IQ - PATH B INDUSTRIAL TECHNICAL DATA SHEET (TDS)`,
      `Market: ${country}`,
      `Commercial Line: ${activeLine.label}`,
      `Selected African Legume: ${selectedCrop.name} (${selectedCrop.localNames})`,
      `Replaced Imported Benchmark: ${activeLine.benchmark}`,
      `ESM-2 Biophysical Match: ${selectedCrop.matchScore || 92}%`,
      ``,
      `PATH B FACTORY PROCESSING PROTOCOL:`,
      `- Cross-Linking Agent: 0.3% Food-Grade CaCl2`,
      `- Thermal Denaturation Window: 82°C - 90°C (15-18 mins)`,
      `- pH-Shifting Regime: Solubilize at pH 8.5 -> Precipitate at pI ${selectedCrop.pI}`,
      `- Pressing / Texturization: 1.6 - 1.8 MPa controlled shear`,
      `- Estimated Raw Material Cost: ${localCropCost}/kg vs Imported Benchmark ${importedBenchmarkCost}/kg`,
    ].join('\n');

    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ProtiIQ-PathB-${selectedCrop.id}-${lineId}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    setDownloaded(true);
  };

  const handleFetchAiAdvisory = async () => {
    setLoadingAi(true);
    try {
      const res = await requestAdvisory({
        role: 'processor',
        job: lineId,
        cropId: selectedCrop.id,
      });
      if (res && res.ai_generative_advisory) {
        setAiAdvisory(res);
      } else {
        setAiAdvisory({
          ai_generative_advisory: `For ${selectedCrop.name} industrial processing in ${activeLine.label}, implement an alkaline extraction at pH 8.5 at 45°C followed by isoelectric precipitation at pI ${selectedCrop.pI}. Cross-link using 0.3% food-grade CaCl2 at 85°C.`,
          ai_provider: 'Proti IQ Rule Engine'
        });
      }
    } catch {
      setAiAdvisory({
        ai_generative_advisory: `Alkaline solubilization at pH 8.5 followed by 0.3% CaCl2 coagulant addition at 85°C achieves optimal texturization.`,
        ai_provider: 'Proti IQ Fallback'
      });
    } finally {
      setLoadingAi(false);
    }
  };

  return (
    <div className="space-y-6">
      <FlowHeader
        flowLabel="FOOD MANUFACTURER R&D FLOW"
        step={step}
        totalSteps={3}
        onBack={() => setStep((s) => Math.max(1, s - 1))}
        onReset={() => {
          setStep(1);
          setDownloaded(false);
        }}
      />

      {/* SCREEN 1: COMMERCIAL PRODUCT LINE */}
      {step === 1 && (
        <section className="space-y-6">
          <div className="text-center space-y-2">
            <h1 className="text-3xl sm:text-4xl font-extrabold text-gray-900">
              Select Commercial Product Line
            </h1>
            <p className="text-lg text-gray-600">
              Screen 8 African legumes to replace imported Soy SPI, Whey, or poultry eggs in {country}.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {INDUSTRIAL_LINES.map((line) => (
              <div
                key={line.id}
                onClick={() => {
                  setLineId(line.id);
                  setStep(2);
                }}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') {
                    setLineId(line.id);
                    setStep(2);
                  }
                }}
                className="bg-white border border-gray-200 hover:border-[#14532D] rounded-2xl p-6 transition cursor-pointer flex flex-col justify-between gap-4"
              >
                <div className="space-y-2">
                  <span className="inline-block text-xs font-bold uppercase tracking-wider text-amber-800 bg-amber-50 px-2.5 py-1 rounded-md">
                    {line.category}
                  </span>
                  <h2 className="text-2xl font-bold text-gray-900">{line.label}</h2>
                  <p className="text-base text-gray-600">{line.description}</p>
                </div>

                <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                  <span className="text-sm font-medium text-gray-600">
                    Replaces: <strong>{line.benchmark}</strong>
                  </span>
                  <span className="text-base font-bold text-[#14532D]">Screen Crops &gt;</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* SCREEN 2: AI RANKING OF CANDIDATE CROPS */}
      {step === 2 && (
        <section className="space-y-5">
          <div className="space-y-1">
            <p className="text-sm font-bold uppercase tracking-wider text-[#14532D]">
              Industrial Target: {activeLine.label}
            </p>
            <h1 className="text-3xl font-extrabold text-gray-900">
              AI-Ranked African Raw Materials
            </h1>
          </div>

          <CropRankingBoard
            rankedCrops={rankedCrops}
            market={market}
            goalTitle={activeLine.label}
            focusReason={activeLine.focusReason}
            actionLabel="View Spec & Path B Protocol"
            onSelectCrop={(crop) => {
              setSelectedCrop(crop);
              setDownloaded(false);
              setStep(3);
            }}
            onOpenEvidence={onOpenEvidence}
          />
        </section>
      )}

      {/* SCREEN 3: HEAD-TO-HEAD SPEC + PATH B PROTOCOL */}
      {step === 3 && (
        <section className="space-y-6">
          <div className="space-y-1">
            <p className="text-sm font-bold uppercase tracking-wider text-amber-800">
              {selectedCrop.name} vs. {activeLine.benchmark}
            </p>
            <h1 className="text-3xl font-extrabold text-gray-900">
              Technical Spec &amp; Path B Factory Protocol
            </h1>
          </div>

          {/* Head-to-Head Spec Table */}
          <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-[#FAF9F6] border-b border-gray-200">
                  <th className="p-4 text-sm font-bold uppercase text-gray-500">Metric</th>
                  <th className="p-4 text-base font-extrabold text-[#14532D]">
                    {selectedCrop.name}
                  </th>
                  <th className="p-4 text-base font-bold text-gray-600">
                    Imported Benchmark
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 text-base">
                <tr>
                  <td className="p-4 font-semibold text-gray-800">Protein &amp; Solubility</td>
                  <td className="p-4 font-bold text-gray-900 bg-emerald-50/40">
                    {selectedCrop.proteinPer100g}g/100g ({selectedCrop.solubilityPct}% soluble)
                  </td>
                  <td className="p-4 text-gray-600">Standard commercial isolate</td>
                </tr>
                <tr>
                  <td className="p-4 font-semibold text-gray-800">Structural Globulin Profile</td>
                  <td className="p-4 font-bold text-gray-900 bg-emerald-50/40">
                    {selectedCrop.globulinFocus}
                  </td>
                  <td className="p-4 text-gray-600">7S/11S Soy or Egg Albumen</td>
                </tr>
                <tr>
                  <td className="p-4 font-semibold text-gray-800">Estimated Cost / kg</td>
                  <td className="p-4 font-extrabold text-[#14532D] bg-emerald-50/40">
                    {localCropCost} / kg
                  </td>
                  <td className="p-4 text-gray-600">{importedBenchmarkCost} / kg</td>
                </tr>
              </tbody>
            </table>
          </div>

          {/* Path B Lab Protocol Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-white border border-gray-200 rounded-2xl p-5">
              <p className="text-xs font-bold uppercase text-gray-500">Cross-Linking Agent</p>
              <p className="text-xl font-extrabold text-[#14532D] mt-1">0.3% Food-Grade CaCl₂</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl p-5">
              <p className="text-xs font-bold uppercase text-gray-500">Thermal Denaturation Window</p>
              <p className="text-xl font-extrabold text-gray-900 mt-1">82°C – 90°C (15–18 mins)</p>
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl p-5">
              <p className="text-xs font-bold uppercase text-gray-500">pH-Shifting Regime</p>
              <p className="text-base font-bold text-gray-900 mt-1">
                Extract at pH 8.5 → Isoelectric precipitation at pI {selectedCrop.pI}
              </p>
            </div>
            <div className="bg-white border border-gray-200 rounded-2xl p-5">
              <p className="text-xs font-bold uppercase text-gray-500">Pressing &amp; Shear</p>
              <p className="text-base font-bold text-gray-900 mt-1">
                1.6 – 1.8 MPa controlled extrusion / curd pressing
              </p>
            </div>
          </div>

          {/* AI Factory Formulation Advisory */}
          <div className="bg-emerald-50/60 border border-emerald-200 rounded-2xl p-6 text-left space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-emerald-800">
                  AI Factory Process Advisory
                </span>
                <p className="text-sm text-gray-600">
                  Biophysical parameter calibration via Meta ESM-2 &amp; Pretoria wet-lab data
                </p>
              </div>
              <button
                type="button"
                onClick={handleFetchAiAdvisory}
                disabled={loadingAi}
                className="px-4 py-2 rounded-lg bg-[#14532D] hover:bg-emerald-900 text-white font-semibold text-sm transition cursor-pointer disabled:opacity-50"
              >
                {loadingAi ? 'Calibrating Process...' : 'Consult Proti IQ AI Engineer'}
              </button>
            </div>

            {aiAdvisory && (
              <div className="pt-3 border-t border-emerald-200 text-sm text-gray-800 space-y-2">
                <p className="font-medium whitespace-pre-line leading-relaxed">
                  {aiAdvisory.ai_generative_advisory}
                </p>
                <div className="flex items-center justify-between text-xs text-gray-500 pt-1">
                  <span>Engine: {aiAdvisory.ai_provider}</span>
                  <span>Industrial Line: {activeLine.label}</span>
                </div>
              </div>
            )}
          </div>

          {downloaded && (
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 font-semibold text-base">
              Path B Technical Data Sheet downloaded for {selectedCrop.name}.
            </div>
          )}

          <div className="flex flex-col sm:flex-row gap-3">
            <button
              type="button"
              onClick={handleDownloadTDS}
              className="flex-1 py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white text-lg font-bold transition cursor-pointer"
            >
              Download Path B Lab Protocol
            </button>
            <button
              type="button"
              onClick={() => setStep(2)}
              className="py-4 px-5 rounded-xl border border-gray-300 bg-white hover:bg-gray-50 text-gray-900 text-base font-bold cursor-pointer"
            >
              Pick Another Ranked Crop
            </button>
          </div>
        </section>
      )}
    </div>
  );
}