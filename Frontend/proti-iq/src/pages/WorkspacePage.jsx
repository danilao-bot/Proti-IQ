import React, { useState, useEffect } from 'react';
import { sendChatQuery, getChatSuggestions, exportDocument } from '../services/chatClient';
import { clearStoredToken } from '../services/authClient';

export default function WorkspacePage({ session, onLogOut, onOpenLegal, onNavigateView, activeSubView = 'hub' }) {
  const {
    full_name = 'User',
    assigned_role = 'consumer',
    role_title = 'Consumer / Caregiver',
    country = 'Nigeria',
    age = 35,
    geriatric_mode = false,
    accessible_routes = ['hub', 'crops']
  } = session || {};

  const [inputQuery, setInputQuery] = useState('');
  const [selectedCrop, setSelectedCrop] = useState('cowpea');
  const [selectedJob, setSelectedJob] = useState('milk');
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [chatResponse, setChatResponse] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [downloading, setDownloading] = useState(false);

  // Load role-specific suggestions on mount
  useEffect(() => {
    getChatSuggestions(assigned_role).then((suggs) => {
      setSuggestions(suggs);
    });
  }, [assigned_role]);

  const handleSendQuery = async (queryText = null) => {
    const textToSend = (typeof queryText === 'string' ? queryText : inputQuery).trim();
    if (!textToSend) return;

    setLoading(true);
    setErrorMsg('');
    try {
      const res = await sendChatQuery({
        message: textToSend,
        role: assigned_role,
        crop_id: selectedCrop,
        job: selectedJob,
        country: country,
        age: age,
        geriatric_mode: geriatric_mode
      });
      setChatResponse(res);
      setInputQuery('');
    } catch (err) {
      setErrorMsg(err.message || 'Failed to generate advisory. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    setDownloading(true);
    try {
      let exportType = 'recipe';
      if (assigned_role === 'nutritionist') exportType = 'advisory';
      if (assigned_role === 'processor') exportType = 'tds';

      await exportDocument(exportType, {
        user_name: full_name,
        country: country,
        crop_name: selectedCrop.replace('_', ' ').toUpperCase(),
        job_name: selectedJob.toUpperCase(),
        role: assigned_role,
        parameters: {
          vehicle: 'Amala',
          fortification_pct: 15,
          protein_yield_g: 18.5
        }
      });
    } catch (err) {
      alert('Export failed: ' + err.message);
    } finally {
      setDownloading(false);
    }
  };

  const isConsumer = assigned_role === 'consumer';
  const bodyTextClass = (isConsumer || geriatric_mode) ? 'text-lg' : 'text-base';

  return (
    <div className="min-h-screen bg-[#F9FAFB] text-gray-900 flex flex-col justify-between">
      {/* Top Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl font-black text-[#14532D] tracking-tight">PROTI IQ</span>
            <span className="text-xs font-bold uppercase tracking-wider text-gray-500 border-l border-gray-300 pl-3 hidden sm:inline">
              {role_title}
            </span>
          </div>

          <div className="flex items-center gap-4 text-sm">
            <span className="font-semibold text-gray-700 hidden md:inline">
              Market: {country}
            </span>
            <button
              type="button"
              onClick={onLogOut}
              className="px-3.5 py-1.5 rounded-lg border border-gray-300 hover:bg-gray-100 text-gray-700 font-semibold text-xs cursor-pointer"
            >
              Log Out
            </button>
          </div>
        </div>
      </header>

      {/* Main Layout: Sub-navigation & Workspace */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex-1 w-full space-y-6">
        
        {/* Navigation Tabs (Filtered strictly by accessible routes) */}
        <nav className="flex items-center gap-2 border-b border-gray-200 pb-3 overflow-x-auto text-sm font-bold">
          <button
            type="button"
            onClick={() => onNavigateView('workspace')}
            className={`px-4 py-2 rounded-lg cursor-pointer transition ${activeSubView === 'workspace' ? 'bg-[#14532D] text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            AI Copilot Workspace
          </button>

          {accessible_routes.includes('hub') && (
            <button
              type="button"
              onClick={() => onNavigateView('hub')}
              className={`px-4 py-2 rounded-lg cursor-pointer transition ${activeSubView === 'hub' ? 'bg-[#14532D] text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              Interactive Discovery Hub
            </button>
          )}

          {accessible_routes.includes('crops') && (
            <button
              type="button"
              onClick={() => onNavigateView('crops')}
              className={`px-4 py-2 rounded-lg cursor-pointer transition ${activeSubView === 'crops' ? 'bg-[#14532D] text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              African Crop Catalog
            </button>
          )}

          {accessible_routes.includes('evidence') && (
            <button
              type="button"
              onClick={() => onNavigateView('evidence')}
              className={`px-4 py-2 rounded-lg cursor-pointer transition ${activeSubView === 'evidence' ? 'bg-[#14532D] text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              Pretoria Wet-Lab Evidence
            </button>
          )}

          {accessible_routes.includes('structure') && (
            <button
              type="button"
              onClick={() => onNavigateView('structure')}
              className={`px-4 py-2 rounded-lg cursor-pointer transition ${activeSubView === 'structure' ? 'bg-[#14532D] text-white' : 'text-gray-600 hover:bg-gray-100'}`}
            >
              3D AlphaFold Molecular Models
            </button>
          )}
        </nav>

        {/* Personalized Welcome Card */}
        <section className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-4 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-gray-200 pb-4">
            <div>
              <p className="text-xs font-bold uppercase tracking-wider text-[#14532D]">
                LOCKED OPERATIONAL WORKSPACE
              </p>
              <h1 className="text-3xl font-black text-gray-900 mt-1">
                Welcome, {full_name}
              </h1>
            </div>
            {geriatric_mode && (
              <span className="self-start sm:self-auto px-3.5 py-1.5 rounded-lg bg-emerald-50 text-emerald-900 font-bold text-xs border border-emerald-200">
                Geriatric Sarcopenia Mode Active (High Leucine &amp; Soft Swallow)
              </span>
            )}
          </div>

          {/* Central AI Query Bar (Dominant Element) */}
          <div className="space-y-3">
            <label className="block text-sm font-bold text-gray-800">
              Ask Proti IQ (Target: {selectedJob.toUpperCase()} • Legume: {selectedCrop.replace('_', ' ').toUpperCase()})
            </label>

            <div className="flex flex-col sm:flex-row gap-2">
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendQuery()}
                placeholder="Ask about culinary de-flavoring, clinical dosage, or industrial extrusion parameters..."
                className="flex-1 px-4 py-3.5 rounded-xl border border-gray-300 text-gray-900 bg-white focus:outline-none focus:border-[#14532D] text-base"
              />
              <button
                type="button"
                onClick={() => handleSendQuery()}
                disabled={loading}
                className="bg-[#14532D] hover:bg-emerald-900 text-white font-extrabold px-6 py-3.5 rounded-xl text-base transition cursor-pointer disabled:opacity-50 shrink-0"
              >
                {loading ? 'Analyzing...' : 'Consult Proti IQ'}
              </button>
            </div>

            {/* Target Selectors */}
            <div className="flex flex-wrap items-center gap-3 pt-1 text-xs text-gray-600">
              <span className="font-bold text-gray-700">Calibrate Context:</span>
              <select
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="border border-gray-300 rounded-lg px-2.5 py-1.5 bg-white text-gray-800 font-medium"
              >
                <option value="cowpea">Cowpea (Vigna unguiculata)</option>
                <option value="pigeon_pea">Pigeon Pea (Cajanus cajan)</option>
                <option value="african_yam_bean">African Yam Bean (Sphenostylis)</option>
                <option value="bambara">Bambara Groundnut (Vigna subterranea)</option>
                <option value="groundnut">Groundnut (Arachis hypogaea)</option>
              </select>

              <select
                value={selectedJob}
                onChange={(e) => setSelectedJob(e.target.value)}
                className="border border-gray-300 rounded-lg px-2.5 py-1.5 bg-white text-gray-800 font-medium"
              >
                <option value="meat">Textured Suya Meat</option>
                <option value="milk">Colloidal Milk Drink</option>
                <option value="egg">Heat-Set Scrambled Egg</option>
                <option value="gel">Coagulated Awara Curd</option>
                <option value="mayo">Emulsified Salad Cream</option>
                <option value="crayfish">Savory Umami Seasoning</option>
                <option value="sarcopenia">Geriatric Swallow Fortification</option>
              </select>
            </div>

            {/* Suggested Prompt Chips */}
            {suggestions.length > 0 && (
              <div className="pt-2">
                <p className="text-xs font-semibold text-gray-500 mb-2">Suggested queries for your role:</p>
                <div className="flex flex-wrap gap-2">
                  {suggestions.map((sugg, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handleSendQuery(sugg)}
                      className="text-left text-xs text-gray-800 bg-gray-100 hover:bg-gray-200 border border-gray-200 rounded-lg px-3 py-2 transition cursor-pointer"
                    >
                      {sugg}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>

        {errorMsg && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-sm font-medium">
            {errorMsg}
          </div>
        )}

        {/* Dynamic Workspace Split-View */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left 2 Columns: Chat Advisory Output */}
          <section className="lg:col-span-2 bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-4 shadow-sm">
            <div className="border-b border-gray-200 pb-3 flex items-center justify-between">
              <h2 className="text-xl font-extrabold text-gray-900">
                Scientific Advisory Output
              </h2>
              {chatResponse && (
                <span className="text-xs text-gray-500 font-medium">
                  Engine: {chatResponse.provider}
                </span>
              )}
            </div>

            {loading && (
              <div className="py-12 text-center text-gray-500 space-y-2">
                <p className="text-base font-semibold">Computing biophysical scores and querying advisory engine...</p>
                <p className="text-xs">Applying Meta ESM-2 weights and Pretoria wet-lab constraints.</p>
              </div>
            )}

            {!loading && !chatResponse && (
              <div className="py-12 text-center text-gray-500 space-y-1">
                <p className="text-base font-semibold">Ready for your query.</p>
                <p className="text-xs">Select a suggestion above or enter any food formulation question.</p>
              </div>
            )}

            {!loading && chatResponse && (
              <div className="space-y-4">
                <div className={`${bodyTextClass} text-gray-800 whitespace-pre-line leading-relaxed`}>
                  {chatResponse.advisory_text}
                </div>

                <div className="border-t border-gray-200 pt-4 flex flex-wrap items-center justify-between gap-3 text-xs text-gray-600">
                  <span>Selected Legume: <strong>{chatResponse.referenced_crop.toUpperCase()}</strong></span>
                  <span>Target Application: <strong>{chatResponse.target_job}</strong></span>
                  <span>Biophysical Confidence: <strong>{chatResponse.confidence}</strong></span>
                </div>
              </div>
            )}

            {/* Actionable Export Button */}
            <div className="pt-4 border-t border-gray-200">
              <button
                type="button"
                onClick={handleExport}
                disabled={downloading}
                className="w-full sm:w-auto px-6 py-3 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-bold text-sm cursor-pointer transition disabled:opacity-50"
              >
                {downloading ? 'Preparing Document...' : (
                  isConsumer ? 'Save Culinary Recipe Card (.txt)' :
                  assigned_role === 'nutritionist' ? 'Export Clinical Dietary Advisory (.txt)' :
                  'Download Technical Data Sheet TDS (.txt)'
                )}
              </button>
            </div>
          </section>

          {/* Right Column: Contextual Data Panel */}
          <aside className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-5 shadow-sm">
            <h2 className="text-xl font-extrabold text-gray-900 border-b border-gray-200 pb-3">
              Contextual Data Panel
            </h2>

            {/* Role-Specific Panel Details */}
            {isConsumer && (
              <div className="space-y-4 text-sm text-gray-700">
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Market Price Benchmark</p>
                  <p className="text-xl font-extrabold text-[#14532D]">1,800 NGN / kg</p>
                  <p className="text-xs text-gray-600">Saves ~2,400 NGN/kg vs imported soy or dairy milk powder.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Essential Kitchen Rule</p>
                  <p className="font-bold text-gray-900">Blanch 3 mins at 90°C</p>
                  <p className="text-xs text-gray-600">Thermal heat permanently destroys lipoxygenase, eliminating 100% of beany aroma.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Cholesterol &amp; Lactose</p>
                  <p className="font-bold text-gray-900">0mg Cholesterol • Zero Lactose</p>
                  <p className="text-xs text-gray-600">100% plant-derived from native African soil.</p>
                </div>
              </div>
            )}

            {assigned_role === 'nutritionist' && (
              <div className="space-y-4 text-sm text-gray-700">
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Leucine Threshold (mTOR)</p>
                  <p className="text-xl font-extrabold text-[#14532D]">2.8g / meal</p>
                  <p className="text-xs text-gray-600">Exceeds the 2.5g clinical minimum required to trigger muscle protein synthesis in older adults.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Empirical Solubility (Pretoria)</p>
                  <p className="font-bold text-gray-900">78.4% at pH 7.0</p>
                  <p className="text-xs text-gray-600">Ensures smooth swallow without pasty throat residue.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Fortification Formula</p>
                  <p className="font-bold text-gray-900">15% Legume + 85% Staple Flour</p>
                  <p className="text-xs text-gray-600">Delivers 18.5g protein per 100g cooked portion.</p>
                </div>
              </div>
            )}

            {assigned_role === 'processor' && (
              <div className="space-y-4 text-sm text-gray-700">
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Coagulant Concentration</p>
                  <p className="text-xl font-extrabold text-[#14532D]">0.3% Food-Grade CaCl₂</p>
                  <p className="text-xs text-gray-600">Divalent calcium bridging across unfolded acidic subunits.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Thermal Denaturation Window</p>
                  <p className="font-bold text-gray-900">85°C for 15 minutes</p>
                  <p className="text-xs text-gray-600">Unfolds 11S legumin hexamers into reactive fibrous curd.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Extrusion Pressure</p>
                  <p className="font-bold text-gray-900">1.6 – 1.8 MPa</p>
                  <p className="text-xs text-gray-600">Yields 1.2 - 1.5 N curd breaking stress matching beef suya.</p>
                </div>
              </div>
            )}

            {assigned_role === 'researcher' && (
              <div className="space-y-4 text-sm text-gray-700">
                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">ESM-2 Architecture</p>
                  <p className="font-bold text-gray-900">esm2_t33_650M_UR50D</p>
                  <p className="text-xs text-gray-600">1,280 dimensions • 650M parameters • 250M training sequences.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Database Coverage</p>
                  <p className="font-bold text-gray-900">348 Seed Storage Globulins</p>
                  <p className="text-xs text-gray-600">630 calibrated rankings across 7 functional food jobs.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">AlphaFold Verification</p>
                  <p className="font-bold text-gray-900">Mean pLDDT: 88.4 (High Tier)</p>
                  <p className="text-xs text-gray-600">Available across all 14 sequenced legume genomes.</p>
                </div>
              </div>
            )}
          </aside>
        </div>
      </div>

      {/* Legal Footer */}
      <footer className="border-t border-gray-200 bg-white py-6 text-xs text-gray-500">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <p>Logged in as {full_name} ({role_title}) • Proti IQ 2026</p>
          <div className="flex flex-wrap items-center gap-4">
            <button type="button" onClick={() => onOpenLegal('privacy')} className="hover:text-gray-900 underline cursor-pointer">
              Privacy Policy
            </button>
            <button type="button" onClick={() => onOpenLegal('terms')} className="hover:text-gray-900 underline cursor-pointer">
              Terms of Service
            </button>
            <button type="button" onClick={() => onOpenLegal('cookies')} className="hover:text-gray-900 underline cursor-pointer">
              Cookie Policy
            </button>
            <button type="button" onClick={() => onOpenLegal('delete')} className="hover:text-red-700 underline cursor-pointer">
              Delete My Data
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
