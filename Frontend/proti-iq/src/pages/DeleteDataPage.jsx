import React, { useState } from 'react';
import { requestDataDeletion } from '../services/authClient';

export default function DeleteDataPage({ onBack, onDeleted }) {
  const [confirmed, setConfirmed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const handleDelete = async () => {
    if (!confirmed) {
      setErrorMsg('Please check the confirmation box below to proceed.');
      return;
    }
    setLoading(true);
    setErrorMsg('');
    try {
      await requestDataDeletion();
      setSuccess(true);
    } catch (err) {
      setErrorMsg(err.message || 'Data deletion failed. You may not have an active session.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#F9FAFB] flex flex-col justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-xl w-full mx-auto bg-white border border-gray-200 rounded-2xl p-6 sm:p-10 shadow-sm space-y-6">
        <div className="border-b border-gray-200 pb-4 flex items-center justify-between">
          <h1 className="text-2xl font-black text-gray-900">Permanent Data Deletion</h1>
          <button
            type="button"
            onClick={onBack}
            className="text-sm font-semibold text-gray-500 hover:text-gray-900 cursor-pointer"
          >
            Cancel
          </button>
        </div>

        {errorMsg && (
          <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-800 text-sm font-medium">
            {errorMsg}
          </div>
        )}

        {success ? (
          <div className="space-y-4 text-center py-4">
            <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 text-base font-semibold">
              Your profile data has been permanently deleted from both local and cloud databases.
            </div>
            <p className="text-sm text-gray-600">
              In accordance with NDPA 2023 and GDPR Article 17, no personal identifying records remain.
            </p>
            <button
              type="button"
              onClick={onDeleted}
              className="mt-2 py-3 px-6 rounded-xl bg-[#14532D] text-white font-bold cursor-pointer"
            >
              Return to Landing Page
            </button>
          </div>
        ) : (
          <div className="space-y-5">
            <p className="text-sm text-gray-700 leading-relaxed">
              Under the Nigeria Data Protection Act (NDPA 2023) and international privacy standards, you have the absolute right to complete erasure.
            </p>

            <div className="bg-red-50/50 border border-red-200 rounded-xl p-4 text-xs text-red-900 space-y-1">
              <p className="font-bold">What will be permanently erased:</p>
              <ul className="list-disc list-inside space-y-0.5">
                <li>Your full name and age from local and Supabase cloud databases.</li>
                <li>Your geographic country and region mapping.</li>
                <li>Your assigned role and active session authentication tokens.</li>
              </ul>
            </div>

            <label className="flex items-start gap-2 text-sm text-gray-800 cursor-pointer">
              <input
                type="checkbox"
                checked={confirmed}
                onChange={(e) => setConfirmed(e.target.checked)}
                className="mt-1"
              />
              <span>
                I confirm that I want to permanently delete my Proti IQ profile and session data. I understand this action cannot be reversed.
              </span>
            </label>

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={onBack}
                className="w-1/3 py-3.5 px-4 rounded-xl border border-gray-300 hover:bg-gray-50 text-gray-800 font-bold text-sm cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDelete}
                disabled={loading}
                className="w-2/3 py-3.5 px-6 rounded-xl bg-red-700 hover:bg-red-800 text-white font-bold text-sm transition cursor-pointer disabled:opacity-50"
              >
                {loading ? 'Deleting Records...' : 'Permanently Delete My Data'}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
