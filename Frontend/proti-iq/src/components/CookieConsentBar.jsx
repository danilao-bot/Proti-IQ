import React, { useState, useEffect } from 'react';

export default function CookieConsentBar({ onOpenCookiePolicy }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const consent = localStorage.getItem('proti_cookie_consent');
    if (!consent) {
      setVisible(true);
    }
  }, []);

  const handleAccept = () => {
    localStorage.setItem('proti_cookie_consent', 'accepted');
    setVisible(false);
  };

  if (!visible) return null;

  return (
    <div
      role="region"
      aria-label="Cookie consent notice"
      className="fixed bottom-0 left-0 right-0 z-50 bg-[#111827] text-white border-t border-gray-700 px-4 py-3 sm:px-8 sm:py-4 shadow-lg"
    >
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3 text-sm">
        <p className="text-gray-300">
          Proti IQ uses strictly essential session cookies to preserve your locked role and biophysical calculations. We do not use advertising or tracking cookies.
        </p>
        <div className="flex items-center gap-3 shrink-0">
          <button
            type="button"
            onClick={onOpenCookiePolicy}
            className="text-gray-400 hover:text-white underline cursor-pointer"
          >
            Cookie Policy
          </button>
          <button
            type="button"
            onClick={handleAccept}
            className="bg-[#14532D] hover:bg-emerald-900 text-white font-bold px-4 py-2 rounded-lg cursor-pointer transition"
          >
            Accept Essential Cookies
          </button>
        </div>
      </div>
    </div>
  );
}
