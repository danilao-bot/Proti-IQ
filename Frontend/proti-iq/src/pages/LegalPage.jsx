import React, { useState, useEffect } from 'react';
import { fetchLegalDocument } from '../services/legalClient';

export default function LegalPage({ docType = 'privacy', onBack }) {
  const [doc, setDoc] = useState({ title: '', content: '' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let active = true;
    setLoading(true);
    fetchLegalDocument(docType).then((res) => {
      if (active) {
        setDoc(res);
        setLoading(false);
      }
    });
    return () => { active = false; };
  }, [docType]);

  return (
    <div className="min-h-screen bg-[#F9FAFB] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto bg-white border border-gray-200 rounded-2xl p-6 sm:p-10 shadow-sm space-y-6">
        <div className="flex items-center justify-between border-b border-gray-200 pb-4">
          <span className="text-xl font-black text-[#14532D]">PROTI IQ COMPLIANCE</span>
          <button
            type="button"
            onClick={onBack}
            className="text-sm font-bold text-gray-700 hover:text-black border border-gray-300 px-4 py-2 rounded-lg cursor-pointer"
          >
            &lt; Return to Application
          </button>
        </div>

        {loading ? (
          <p className="text-gray-500 py-12 text-center">Loading official document...</p>
        ) : (
          <div className="prose max-w-none text-gray-800 text-sm sm:text-base leading-relaxed whitespace-pre-line">
            {doc.content}
          </div>
        )}
      </div>
    </div>
  );
}
