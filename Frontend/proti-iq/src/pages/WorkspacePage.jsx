import React, { useState, useEffect, useRef } from 'react';
import { sendChatQuery, getChatSuggestions, exportDocument } from '../services/chatClient';

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
  const [loadingStage, setLoadingStage] = useState(0);
  const [errorMsg, setErrorMsg] = useState('');
  const [downloading, setDownloading] = useState(false);

  // Chat Conversation State
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'assistant',
      text: `Hi ${full_name}! I am your Proti IQ AI advisor for ${role_title}. What African legume or food recipe would you like to prepare, fortify, or optimize today?`,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      steps: null,
      follow_ups: [
        "How do I make smooth cowpea milk with zero beany taste?",
        "What is the best African bean to replace eggs in cooking?",
        "How can I fortify family meals with Pigeon Pea?"
      ]
    }
  ]);

  // Guided Walkthrough Stepper State (Tracks step index per message or active response)
  const [activeStepIndices, setActiveStepIndices] = useState({});
  const [showAllStepsMap, setShowAllStepsMap] = useState({});
  const [showExaminedParamsMap, setShowExaminedParamsMap] = useState({});

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Load role-specific suggestions on mount
  useEffect(() => {
    getChatSuggestions(assigned_role).then((suggs) => {
      if (suggs && suggs.length > 0) {
        setSuggestions(suggs);
      }
    });
  }, [assigned_role]);

  // Stage progression animation while loading
  useEffect(() => {
    let timer;
    if (loading) {
      setLoadingStage(0);
      timer = setInterval(() => {
        setLoadingStage((prev) => (prev < 2 ? prev + 1 : prev));
      }, 700);
    }
    return () => clearInterval(timer);
  }, [loading]);

  const handleSendQuery = async (queryText = null) => {
    const textToSend = (typeof queryText === 'string' ? queryText : inputQuery).trim();
    if (!textToSend) return;

    const userMsgId = 'user-' + Date.now();
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    // Append User Message to Chat Stream
    setMessages((prev) => [
      ...prev,
      {
        id: userMsgId,
        sender: 'user',
        text: textToSend,
        timestamp: timeStr
      }
    ]);

    setInputQuery('');
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

      const assistantMsgId = 'assistant-' + Date.now();
      
      // Initialize active step for this message
      setActiveStepIndices((prev) => ({ ...prev, [assistantMsgId]: 0 }));

      // Append Assistant Response to Chat Stream
      setMessages((prev) => [
        ...prev,
        {
          id: assistantMsgId,
          sender: 'assistant',
          text: res.advisory_text,
          steps: res.steps || [],
          examined_parameters: res.examined_parameters || [],
          follow_ups: res.follow_up_suggestions || [],
          provider: res.provider,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } catch (err) {
      setErrorMsg(err.message || 'Failed to generate advisory. Please retry.');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async (msgSteps) => {
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
          vehicle: 'African Legume Formulation',
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
  const bodyTextClass = isConsumer ? 'text-base sm:text-lg' : 'text-sm sm:text-base';

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

      {/* Main Layout */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">
        
        {/* Navigation Tabs */}
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

        {errorMsg && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-sm font-medium animate-fadeIn">
            {errorMsg}
          </div>
        )}

        {/* Dynamic Workspace Split-View */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left 2 Columns: Modern Interactive Conversational Chat */}
          <section className="lg:col-span-2 bg-white border border-gray-200 rounded-2xl flex flex-col shadow-sm overflow-hidden h-[720px]">
            
            {/* Chat Pane Header */}
            <div className="p-4 sm:p-5 border-b border-gray-200 flex items-center justify-between bg-white shrink-0">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[#14532D] text-white font-black flex items-center justify-center text-sm shadow-sm">
                  IQ
                </div>
                <div>
                  <h2 className="font-extrabold text-gray-900 text-base leading-tight">
                    Proti IQ Assistant
                  </h2>
                  <p className="text-xs text-gray-500 flex items-center gap-1.5 mt-0.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                    <span>Active • Calibrated for {role_title}</span>
                  </p>
                </div>
              </div>

              <span className="text-xs font-semibold text-gray-400">
                Market: {country}
              </span>
            </div>

            {/* Chat Messages Scrollable Stream */}
            <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6 bg-[#FAF9F6]">
              {messages.map((msg) => (
                <div key={msg.id} className="space-y-3">
                  
                  {/* USER MESSAGE */}
                  {msg.sender === 'user' && (
                    <div className="flex justify-end animate-fadeIn">
                      <div className="bg-[#14532D] text-white rounded-2xl rounded-tr-sm px-5 py-3 max-w-lg shadow-sm text-sm sm:text-base leading-relaxed">
                        <p>{msg.text}</p>
                        <span className="block text-[10px] text-emerald-200/80 text-right mt-1">
                          {msg.timestamp}
                        </span>
                      </div>
                    </div>
                  )}

                  {/* ASSISTANT MESSAGE */}
                  {msg.sender === 'assistant' && (
                    <div className="flex items-start gap-3 animate-fadeIn">
                      <div className="w-8 h-8 rounded-full bg-[#14532D] text-white font-black flex items-center justify-center text-xs shrink-0 mt-1 shadow-sm">
                        IQ
                      </div>

                      <div className="space-y-4 max-w-2xl flex-1">
                        
                        {/* Advisory Text Bubble */}
                        <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm p-5 shadow-sm space-y-3 text-gray-800">
                          <p className={`${bodyTextClass} leading-relaxed`}>
                            {msg.text}
                          </p>

                          {msg.provider && (
                            <p className="text-[11px] text-gray-400 border-t border-gray-100 pt-2">
                              Formulated via {msg.provider}
                            </p>
                          )}
                        </div>

                        {/* Interactive Step-by-Step Guided Stepper */}
                        {msg.steps && msg.steps.length > 0 && (
                          <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm space-y-4 animate-fadeIn">
                            
                            <div className="flex items-center justify-between border-b border-gray-100 pb-3">
                              <span className="text-xs font-extrabold uppercase tracking-wider text-[#14532D]">
                                Step-by-Step Interactive Guide
                              </span>
                              <button
                                type="button"
                                onClick={() =>
                                  setShowAllStepsMap((prev) => ({
                                    ...prev,
                                    [msg.id]: !prev[msg.id]
                                  }))
                                }
                                className="text-xs font-bold text-gray-600 hover:text-[#14532D] cursor-pointer"
                              >
                                {showAllStepsMap[msg.id] ? 'Single-Step Mode' : 'View All Steps'}
                              </button>
                            </div>

                            {/* Single Step Stepper Mode */}
                            {!showAllStepsMap[msg.id] && (() => {
                              const sIdx = activeStepIndices[msg.id] || 0;
                              const curStep = msg.steps[sIdx] || msg.steps[0];
                              const totalSteps = msg.steps.length;

                              return (
                                <div className="space-y-4">
                                  {/* Progress bar */}
                                  <div className="space-y-1">
                                    <div className="flex items-center justify-between text-xs font-bold text-gray-600">
                                      <span>Step {curStep.step_number} of {totalSteps}</span>
                                      <span>{curStep.duration || 'Action Step'}</span>
                                    </div>
                                    <div className="w-full bg-gray-100 rounded-full h-1.5 overflow-hidden">
                                      <div
                                        className="bg-[#14532D] h-1.5 rounded-full transition-all duration-300"
                                        style={{ width: `${(curStep.step_number / totalSteps) * 100}%` }}
                                      />
                                    </div>
                                  </div>

                                  {/* Step Card Content */}
                                  <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-2">
                                    <h4 className="font-bold text-gray-900 text-base">
                                      {curStep.title}
                                    </h4>
                                    <p className={`${bodyTextClass} text-gray-700 leading-relaxed`}>
                                      {curStep.instruction}
                                    </p>

                                    {curStep.critical_tip && (
                                      <div className="p-3 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-950 font-medium mt-2">
                                        <strong>Key Tip:</strong> {curStep.critical_tip}
                                      </div>
                                    )}
                                  </div>

                                  {/* Step Navigation Buttons */}
                                  <div className="flex items-center justify-between gap-3 pt-1">
                                    <button
                                      type="button"
                                      onClick={() =>
                                        setActiveStepIndices((prev) => ({
                                          ...prev,
                                          [msg.id]: Math.max(0, sIdx - 1)
                                        }))
                                      }
                                      disabled={sIdx === 0}
                                      className="px-4 py-2.5 rounded-xl border border-gray-300 hover:bg-gray-100 text-gray-800 font-bold text-xs cursor-pointer disabled:opacity-40 transition"
                                    >
                                      Previous Step
                                    </button>

                                    {sIdx < totalSteps - 1 ? (
                                      <button
                                        type="button"
                                        onClick={() =>
                                          setActiveStepIndices((prev) => ({
                                            ...prev,
                                            [msg.id]: Math.min(totalSteps - 1, sIdx + 1)
                                          }))
                                        }
                                        className="px-5 py-2.5 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-bold text-xs cursor-pointer transition shadow-sm"
                                      >
                                        Next Step
                                      </button>
                                    ) : (
                                      <button
                                        type="button"
                                        onClick={() => handleExport(msg.steps)}
                                        disabled={downloading}
                                        className="px-5 py-2.5 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-bold text-xs cursor-pointer transition shadow-sm"
                                      >
                                        {downloading ? 'Preparing...' : 'Completed! Download Guide'}
                                      </button>
                                    )}
                                  </div>
                                </div>
                              );
                            })()}

                            {/* View All Steps Mode */}
                            {showAllStepsMap[msg.id] && (
                              <div className="space-y-3">
                                {msg.steps.map((st, sidx) => (
                                  <div key={sidx} className="p-3.5 rounded-xl border border-gray-200 bg-gray-50 flex items-start gap-3">
                                    <span className="w-6 h-6 rounded-full bg-[#14532D] text-white font-bold text-xs flex items-center justify-center shrink-0">
                                      {st.step_number}
                                    </span>
                                    <div className="space-y-1 flex-1">
                                      <div className="flex items-center justify-between">
                                        <h5 className="font-bold text-gray-900 text-sm">{st.title}</h5>
                                        <span className="text-xs text-gray-500">{st.duration}</span>
                                      </div>
                                      <p className="text-xs text-gray-700">{st.instruction}</p>
                                    </div>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        )}

                        {/* Follow-up Prompts */}
                        {msg.follow_ups && msg.follow_ups.length > 0 && (
                          <div className="space-y-2 pt-1">
                            <p className="text-xs font-semibold text-gray-500">
                              Suggested follow-up questions:
                            </p>
                            <div className="flex flex-wrap gap-2">
                              {msg.follow_ups.map((fup, fidx) => (
                                <button
                                  key={fidx}
                                  type="button"
                                  onClick={() => handleSendQuery(fup)}
                                  className="text-xs text-[#14532D] bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 rounded-lg px-3 py-1.5 font-medium cursor-pointer transition"
                                >
                                  {fup}
                                </button>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              ))}

              {/* LIVE TYPING / FORMULATING MICRO-ANIMATION */}
              {loading && (
                <div className="flex items-start gap-3 animate-fadeIn">
                  <div className="w-8 h-8 rounded-full bg-[#14532D] text-white font-black flex items-center justify-center text-xs shrink-0 shadow-sm">
                    IQ
                  </div>
                  <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm p-4 text-sm text-gray-700 shadow-sm space-y-1.5">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-gray-900">Proti IQ is formulating</span>
                      <span className="flex gap-1 items-center">
                        <span className="w-1.5 h-1.5 rounded-full bg-[#14532D] typing-dot-1"></span>
                        <span className="w-1.5 h-1.5 rounded-full bg-[#14532D] typing-dot-2"></span>
                        <span className="w-1.5 h-1.5 rounded-full bg-[#14532D] typing-dot-3"></span>
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">
                      {loadingStage === 0 && "Scanning native legume protein profiles..."}
                      {loadingStage === 1 && "Calibrating temperature and taste balance..."}
                      {loadingStage >= 2 && "Synthesizing step-by-step instructions..."}
                    </p>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Chat Input Bar Pinned at Bottom */}
            <div className="p-4 border-t border-gray-200 bg-white shrink-0 space-y-3">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={inputQuery}
                  onChange={(e) => setInputQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && !loading && handleSendQuery()}
                  placeholder="Ask a question or request a recipe..."
                  className="flex-1 px-4 py-3 rounded-xl border border-gray-300 text-gray-900 bg-white focus:outline-none focus:border-[#14532D] text-sm sm:text-base"
                />
                <button
                  type="button"
                  onClick={() => handleSendQuery()}
                  disabled={loading || !inputQuery.trim()}
                  className="bg-[#14532D] hover:bg-emerald-900 text-white font-extrabold px-6 py-3 rounded-xl text-sm sm:text-base transition cursor-pointer disabled:opacity-40 shrink-0 shadow-sm"
                >
                  {loading ? 'Thinking...' : 'Send'}
                </button>
              </div>

              {/* Starter Prompt Chips if user has only welcome message */}
              {messages.length === 1 && suggestions.length > 0 && (
                <div className="flex flex-wrap gap-2 pt-1">
                  {suggestions.slice(0, 3).map((sugg, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handleSendQuery(sugg)}
                      className="text-xs text-gray-700 bg-gray-100 hover:bg-gray-200 border border-gray-200 rounded-lg px-2.5 py-1.5 cursor-pointer transition"
                    >
                      {sugg}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </section>

          {/* Right Column: Contextual Data Panel */}
          <aside className="bg-white border border-gray-200 rounded-2xl p-6 sm:p-8 space-y-5 shadow-sm self-start">
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
                  <p className="text-xs font-bold uppercase text-gray-500">Crude Protein Density</p>
                  <p className="text-xl font-extrabold text-[#14532D]">24.8% Dry Seed Weight</p>
                  <p className="text-xs text-gray-600">Composed primarily of 7S vicilin and 11S legumin globulin fractions.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Thermal Gelation Window</p>
                  <p className="font-bold text-gray-900">82°C – 88°C Peak Denaturation</p>
                  <p className="text-xs text-gray-600">Optimal temperature window for protein network unfolding without burning.</p>
                </div>

                <div className="p-4 rounded-xl bg-gray-50 border border-gray-200 space-y-1">
                  <p className="text-xs font-bold uppercase text-gray-500">Pretoria Wet-Lab Solubility</p>
                  <p className="font-bold text-gray-900">78.4% at Neutral pH 7.0</p>
                  <p className="text-xs text-gray-600">Empirically validated high dispersion suitable for clear beverages and emulsions.</p>
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
