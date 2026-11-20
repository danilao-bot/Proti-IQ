
export default function FlowHeader({ flowLabel, step, totalSteps, onBack, onReset }) {
  return (
    <div className="bg-white border border-gray-200 rounded-2xl px-4 sm:px-5 py-3 flex items-center justify-between">
      <button
        type="button"
        onClick={onBack}
        disabled={step === 1}
        className={`text-sm sm:text-base font-bold px-2 py-1 rounded-lg transition ${
          step === 1
            ? 'text-gray-300 cursor-not-allowed'
            : 'text-gray-700 hover:text-gray-900 hover:bg-gray-100 cursor-pointer'
        }`}
      >
        &lt; Back
      </button>

      <div className="text-center">
        <p className="text-[11px] font-bold tracking-wider uppercase text-gray-500">
          {flowLabel}
        </p>
        <div className="flex items-center justify-center gap-1.5 mt-0.5">
          <span className="text-sm sm:text-base font-extrabold text-gray-900">
            Screen {step} of {totalSteps}
          </span>
          <span className="flex items-center gap-1 ml-1">
            {Array.from({ length: totalSteps }, (_, idx) => idx + 1).map((num) => (
              <span
                key={num}
                className={`w-2 h-2 rounded-full ${
                  num === step ? 'bg-[#14532D]' : 'bg-gray-300'
                }`}
              />
            ))}
          </span>
        </div>
      </div>

      <button
        type="button"
        onClick={onReset}
        className="text-sm sm:text-base font-semibold text-gray-600 hover:text-gray-900 px-2 py-1 rounded-lg hover:bg-gray-100 cursor-pointer"
      >
        Start Over
      </button>
    </div>
  );
}