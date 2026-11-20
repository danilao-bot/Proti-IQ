
export default function EvidenceDrawer({ evidence, onClose }) {
  if (!evidence) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-xs">
      <div className="w-full max-w-lg bg-white h-full overflow-y-auto p-6 sm:p-8 shadow-2xl flex flex-col justify-between gap-6">
        <div className="space-y-6">
          <div className="flex items-start justify-between gap-4 border-b border-gray-200 pb-4">
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-amber-800 bg-amber-100 px-2.5 py-1 rounded-full">
                Meta ESM-2 650M + Wet-Lab Anchor
              </span>
              <h2 className="text-2xl font-extrabold text-gray-900 mt-2">
                {evidence.title}
              </h2>
            </div>
            <button
              type="button"
              onClick={onClose}
              className="px-3 py-1.5 rounded-xl border border-gray-300 text-sm font-bold text-gray-700 hover:bg-gray-100 cursor-pointer"
            >
              Close
            </button>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4">
              <p className="text-xs font-bold uppercase text-emerald-800">Biophysical Match</p>
              <p className="text-3xl font-extrabold text-[#14532D] mt-1">{evidence.similarity}</p>
            </div>
            <div className="bg-[#FAF9F6] border border-gray-200 rounded-2xl p-4">
              <p className="text-xs font-bold uppercase text-gray-500">Confidence Tier</p>
              <p className="text-xl font-extrabold text-gray-900 mt-2">{evidence.confidence}</p>
            </div>
          </div>

          <div className="bg-[#FAF9F6] border border-gray-200 rounded-2xl p-4">
            <p className="text-xs font-bold uppercase text-gray-500">Dominant Globulin Family</p>
            <p className="text-base font-bold text-gray-900 mt-1">{evidence.superfamily}</p>
          </div>

          <div className="space-y-2.5">
            <h3 className="text-sm font-bold uppercase tracking-wider text-gray-500">
              Physicochemical &amp; Structural Metrics
            </h3>
            <div className="divide-y divide-gray-200 border border-gray-200 rounded-2xl overflow-hidden">
              {evidence.metrics.map((m) => (
                <div key={m.label} className="px-4 py-3 flex items-center justify-between bg-white">
                  <span className="text-sm font-medium text-gray-600">{m.label}</span>
                  <span className="text-sm font-bold text-gray-900">{m.value}</span>
                </div>
              ))}
            </div>
          </div>

          <p className="text-base text-gray-700 leading-relaxed bg-amber-50/70 border border-amber-200 rounded-2xl p-4">
            {evidence.summary}
          </p>
        </div>

        <button
          type="button"
          onClick={onClose}
          className="w-full py-3.5 px-6 rounded-xl bg-[#14532D] text-white text-base font-bold hover:bg-emerald-900 cursor-pointer"
        >
          Back to Screen
        </button>
      </div>
    </div>
  );
}