import React, { useState } from 'react';
import { submitOnboarding } from '../services/authClient';

export default function OnboardingPage({ onOnboardingComplete, onCancel }) {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    full_name: '',
    age: '',
    country: 'Nigeria',
    region: '',
    mission: 'consumer',
    scale: 'household',
    consent_given: false,
    cookie_consent: false
  });
  const [errorMsg, setErrorMsg] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const numAge = parseInt(formData.age, 10);
  const isOlderAdult = numAge >= 50;

  const handleNextFromStep1 = () => {
    setErrorMsg('');
    if (!formData.full_name.trim() || formData.full_name.trim().length < 2) {
      setErrorMsg('Please enter your full name (minimum 2 characters).');
      return;
    }
    if (isNaN(numAge) || numAge < 13 || numAge > 120) {
      if (numAge < 13) {
        setErrorMsg('Proti IQ requires users to be at least 13 years old. If you are under 13, please ask a parent or guardian to use this platform with you.');
      } else {
        setErrorMsg('Please enter a valid age between 13 and 120.');
      }
      return;
    }
    setStep(2);
  };

  const handleNextFromStep2 = () => {
    setErrorMsg('');
    if (!formData.country) {
      setErrorMsg('Please select your African country.');
      return;
    }
    setStep(3);
  };

  const handleNextFromStep3 = () => {
    setStep(4);
  };

  const handleNextFromStep4 = () => {
    setStep(5); // Confirmation screen
  };

  const handleSubmitProfile = async () => {
    setErrorMsg('');
    if (!formData.consent_given) {
      setErrorMsg('You must review and accept the Terms of Service and Privacy Policy to proceed.');
      return;
    }
    if (!formData.cookie_consent) {
      setErrorMsg('You must accept essential session cookies to operate your workspace.');
      return;
    }

    setIsSubmitting(true);
    try {
      const res = await submitOnboarding({
        full_name: formData.full_name.trim(),
        age: numAge,
        country: formData.country,
        region: formData.region.trim() || null,
        mission: formData.mission,
        scale: formData.scale,
        consent_given: formData.consent_given,
        cookie_consent: formData.cookie_consent
      });
      onOnboardingComplete(res);
    } catch (err) {
      setErrorMsg(err.message || 'Onboarding failed. Please verify your details.');
    } finally {
      setIsSubmitting(false);
    }
  };

  // Derive resolved role preview for confirmation screen
  const getRolePreview = () => {
    const m = formData.mission;
    const s = formData.scale;
    if (m === 'researcher' || s === 'laboratory') return 'Research Scientist / Academic';
    if (m === 'processor' || s === 'factory') return 'Industrial Processor / R&D Engineer';
    if (m === 'nutritionist' || s === 'clinical') return 'Clinical Nutritionist / Dietitian';
    return 'Consumer / Caregiver';
  };

  return (
    <div className="min-h-screen bg-[#F9FAFB] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-xl w-full mx-auto bg-white border border-gray-200 rounded-2xl p-6 sm:p-10 shadow-sm space-y-6">
        
        {/* Progress Header */}
        <div className="border-b border-gray-200 pb-4 flex items-center justify-between">
          <div>
            <p className="text-xs font-black uppercase tracking-wider text-[#14532D]">
              PROTI IQ • STEP {step} OF 5
            </p>
            <h1 className="text-2xl font-black text-gray-900 mt-1">
              {step === 1 && 'Tell us about yourself'}
              {step === 2 && 'Where are you based?'}
              {step === 3 && 'What brings you to Proti IQ?'}
              {step === 4 && 'How do you work with food?'}
              {step === 5 && 'Review and confirm your profile'}
            </h1>
          </div>
          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              className="text-sm font-semibold text-gray-500 hover:text-gray-900 cursor-pointer"
            >
              Exit
            </button>
          )}
        </div>

        {errorMsg && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-sm font-medium">
            {errorMsg}
          </div>
        )}

        {/* STEP 1: Name and Age */}
        {step === 1 && (
          <div key="step-1" className="space-y-5 animate-fadeIn">
            <div>
              <label className="block text-sm font-bold text-gray-900 mb-1">
                Full Name
              </label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                placeholder="e.g., Ameh Anthony"
                className="w-full px-4 py-3 rounded-xl border border-gray-300 text-gray-900 focus:outline-none focus:border-[#14532D]"
              />
              <p className="text-xs text-gray-500 mt-1">Your name personalizes your workspace and any reports you export.</p>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-900 mb-1">
                Age
              </label>
              <input
                type="number"
                min="13"
                max="120"
                value={formData.age}
                onChange={(e) => setFormData({ ...formData, age: e.target.value })}
                placeholder="e.g., 58"
                className="w-full px-4 py-3 rounded-xl border border-gray-300 text-gray-900 focus:outline-none focus:border-[#14532D]"
              />
              <p className="text-xs text-gray-500 mt-1">You must be at least 13 years old to use Proti IQ.</p>
            </div>

            <button
              type="button"
              onClick={handleNextFromStep1}
              className="w-full py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-bold text-base transition cursor-pointer"
            >
              Continue
            </button>
          </div>
        )}

        {/* STEP 2: Location */}
        {step === 2 && (
          <div key="step-2" className="space-y-5 animate-fadeIn">
            <div>
              <label className="block text-sm font-bold text-gray-900 mb-1">
                African Country
              </label>
              <select
                value={formData.country}
                onChange={(e) => setFormData({ ...formData, country: e.target.value })}
                className="w-full px-4 py-3 rounded-xl border border-gray-300 text-gray-900 bg-white focus:outline-none focus:border-[#14532D]"
              >
                <option value="Nigeria">Nigeria (NGN - Naira)</option>
                <option value="Ghana">Ghana (GHS - Cedi)</option>
                <option value="Kenya">Kenya (KES - Shilling)</option>
                <option value="South Africa">South Africa (ZAR - Rand)</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">Sets local currency and regional agricultural crop availability.</p>
            </div>

            <div>
              <label className="block text-sm font-bold text-gray-900 mb-1">
                State or Region
              </label>
              <input
                type="text"
                value={formData.region}
                onChange={(e) => setFormData({ ...formData, region: e.target.value })}
                placeholder="e.g., Oyo State, Benue, Ashanti"
                className="w-full px-4 py-3 rounded-xl border border-gray-300 text-gray-900 focus:outline-none focus:border-[#14532D]"
              />
            </div>

            <div className="flex gap-3">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="w-1/3 py-4 px-4 rounded-xl border border-gray-300 hover:bg-gray-50 text-gray-800 font-bold text-sm cursor-pointer"
              >
                Back
              </button>
              <button
                type="button"
                onClick={handleNextFromStep2}
                className="w-2/3 py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-bold text-base transition cursor-pointer"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* STEP 3: Primary Mission */}
        {step === 3 && (
          <div key="step-3" className="space-y-4 animate-fadeIn">
            <p className="text-sm text-gray-600">Select what you primarily aim to accomplish with Proti IQ:</p>
            
            {[
              { id: 'consumer', title: 'Affordable Family Meals & Healthy Cooking', desc: 'Prepare healthy, affordable plant-based meals at home, remove beany flavors, or cook for loved ones.' },
              { id: 'nutritionist', title: 'Clinical Dietary Formulation', desc: 'Formulate balanced, high-protein diets for hospital patients, elderly nutrition, or growing children.' },
              { id: 'processor', title: 'Commercial Food Manufacturing', desc: 'Manufacture plant-based milk, meat, or curd alternatives at commercial scale to replace imported soy.' },
              { id: 'researcher', title: 'Scientific Food Research & Innovation', desc: 'Study protein quality, amino acid profiles, and nutritional science of native African legumes.' }
            ].map((opt) => (
              <label
                key={opt.id}
                className={`block p-4 rounded-xl border cursor-pointer transition ${formData.mission === opt.id ? 'border-[#14532D] bg-emerald-50/50' : 'border-gray-200 hover:bg-gray-50'}`}
              >
                <div className="flex items-start gap-3">
                  <input
                    type="radio"
                    name="mission"
                    value={opt.id}
                    checked={formData.mission === opt.id}
                    onChange={(e) => setFormData({ ...formData, mission: e.target.value })}
                    className="mt-1"
                  />
                  <div>
                    <p className="font-bold text-gray-900 text-sm sm:text-base">{opt.title}</p>
                    <p className="text-xs text-gray-600 mt-0.5">{opt.desc}</p>
                  </div>
                </div>
              </label>
            ))}

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => setStep(2)}
                className="w-1/3 py-4 px-4 rounded-xl border border-gray-300 hover:bg-gray-50 text-gray-800 font-bold text-sm cursor-pointer"
              >
                Back
              </button>
              <button
                type="button"
                onClick={handleNextFromStep3}
                className="w-2/3 py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-bold text-base transition cursor-pointer"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* STEP 4: Scale */}
        {step === 4 && (
          <div key="step-4" className="space-y-4 animate-fadeIn">
            <p className="text-sm text-gray-600">Select your operating scale or facility type:</p>

            {[
              { id: 'household', title: 'Household Kitchen or Community Center', desc: 'Standard pots, home blenders, stovetop cooking, local wet-markets.' },
              { id: 'clinical', title: 'Clinical Ward, Hospital, or Dietetic Practice', desc: 'Patient meal planning, therapeutic feeding, dietary counseling.' },
              { id: 'factory', title: 'Commercial Factory or Processing Facility', desc: 'Food production lines, curd-making equipment, bulk ingredient processing.' },
              { id: 'laboratory', title: 'Research Center or Laboratory', desc: 'Food testing, quality assessment, and nutritional development.' }
            ].map((opt) => (
              <label
                key={opt.id}
                className={`block p-4 rounded-xl border cursor-pointer transition ${formData.scale === opt.id ? 'border-[#14532D] bg-emerald-50/50' : 'border-gray-200 hover:bg-gray-50'}`}
              >
                <div className="flex items-start gap-3">
                  <input
                    type="radio"
                    name="scale"
                    value={opt.id}
                    checked={formData.scale === opt.id}
                    onChange={(e) => setFormData({ ...formData, scale: e.target.value })}
                    className="mt-1"
                  />
                  <div>
                    <p className="font-bold text-gray-900 text-sm sm:text-base">{opt.title}</p>
                    <p className="text-xs text-gray-600 mt-0.5">{opt.desc}</p>
                  </div>
                </div>
              </label>
            ))}

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => setStep(3)}
                className="w-1/3 py-4 px-4 rounded-xl border border-gray-300 hover:bg-gray-50 text-gray-800 font-bold text-sm cursor-pointer"
              >
                Back
              </button>
              <button
                type="button"
                onClick={handleNextFromStep4}
                className="w-2/3 py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-bold text-base transition cursor-pointer"
              >
                Continue
              </button>
            </div>
          </div>
        )}

        {/* STEP 5: Confirmation and Role Lock */}
        {step === 5 && (
          <div key="step-5" className="space-y-5 animate-fadeIn">
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-5 space-y-3 text-sm">
              <h2 className="font-extrabold text-gray-900 text-base border-b border-gray-200 pb-2">
                Resolved Profile Summary
              </h2>
              <div className="grid grid-cols-2 gap-2 text-gray-700">
                <span className="font-semibold">Full Name:</span>
                <span>{formData.full_name}</span>
                <span className="font-semibold">Age:</span>
                <span>{formData.age} years</span>
                <span className="font-semibold">Country:</span>
                <span>{formData.country} {formData.region ? `(${formData.region})` : ''}</span>
                <span className="font-semibold">Locked Persona:</span>
                <span className="font-black text-[#14532D]">{getRolePreview()}</span>
                {isOlderAdult && (
                  <>
                    <span className="font-semibold">Nutritional Mode:</span>
                    <span className="font-bold text-emerald-800">Geriatric Sarcopenia Mode</span>
                  </>
                )}
              </div>
            </div>

            {/* Mandatory Consents */}
            <div className="space-y-3 text-xs text-gray-700 pt-1">
              <label className="flex items-start gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.consent_given}
                  onChange={(e) => setFormData({ ...formData, consent_given: e.target.checked })}
                  className="mt-0.5"
                />
                <span>
                  I agree to the <strong>Terms of Service</strong> and <strong>Privacy Policy</strong>. I understand Proti IQ provides computational screening and nutritional guidance, not individualized medical advice.
                </span>
              </label>

              <label className="flex items-start gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.cookie_consent}
                  onChange={(e) => setFormData({ ...formData, cookie_consent: e.target.checked })}
                  className="mt-0.5"
                />
                <span>
                  I consent to strictly essential session cookies to store my locked role and active calculations.
                </span>
              </label>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => setStep(4)}
                className="w-1/3 py-4 px-4 rounded-xl border border-gray-300 hover:bg-gray-50 text-gray-800 font-bold text-sm cursor-pointer"
              >
                Back to Edit
              </button>
              <button
                type="button"
                onClick={handleSubmitProfile}
                disabled={isSubmitting}
                className="w-2/3 py-4 px-6 rounded-xl bg-[#14532D] hover:bg-emerald-900 text-white font-extrabold text-base transition cursor-pointer disabled:opacity-50"
              >
                {isSubmitting ? 'Locking Workspace Profile...' : 'Confirm & Enter Workspace'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
