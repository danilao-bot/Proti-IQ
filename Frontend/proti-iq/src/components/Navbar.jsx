const ROLES = [
  { id: 'caregiver', label: 'Consumer / Caregiver' },
  { id: 'nutritionist', label: 'Nutritionist' },
  { id: 'manufacturer', label: 'Food Manufacturer' },
];

const PAGES = [
  { id: 'hub', label: 'Discovery Hub' },
  { id: 'structure', label: '3D Structures' },
  { id: 'evidence', label: 'Wet-Lab Evidence' },
  { id: 'crops', label: 'Crop Catalog' },
];

export default function Navbar({
  role,
  onRoleChange,
  country,
  onCountryChange,
  activePage,
  onPageChange,
}) {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-3">
        {/* Brand */}
        <button
          type="button"
          onClick={() => onPageChange('hub')}
          className="flex items-center gap-2.5 text-left shrink-0 cursor-pointer"
        >
          <div className="w-10 h-10 rounded-xl bg-[#14532D] text-white font-extrabold flex items-center justify-center text-lg">
            P
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg sm:text-xl tracking-tight text-gray-900 leading-none">
                PROTI IQ
              </span>
              <span className="text-[11px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full bg-amber-100 text-amber-900 whitespace-nowrap">
                Challenge 1 AI
              </span>
            </div>
            <p className="text-xs text-gray-500 mt-0.5">Pan-African Plant-Protein Decision Engine</p>
          </div>
        </button>

        {/* Page Navigation Tabs */}
        <nav aria-label="Main Pages" className="flex items-center gap-1 bg-gray-50 p-1 rounded-xl border border-gray-200">
          {PAGES.map((p) => {
            const isCurrent = activePage === p.id;
            return (
              <button
                key={p.id}
                type="button"
                onClick={() => onPageChange(p.id)}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition cursor-pointer ${
                  isCurrent
                    ? 'bg-[#059669] text-white shadow-xs'
                    : 'text-gray-600 hover:text-gray-900 hover:bg-gray-200/60'
                }`}
              >
                {p.label}
              </button>
            );
          })}
        </nav>

        {/* Country & Persona Selector (Active when on Hub page) */}
        <div className="flex flex-wrap items-center gap-2">
          <label className="flex items-center gap-1.5 text-xs font-medium text-gray-700 bg-gray-50 border border-gray-300 rounded-lg px-2.5 py-1.5">
            <span className="text-gray-500">Region:</span>
            <select
              value={country}
              onChange={(e) => onCountryChange(e.target.value)}
              className="bg-transparent font-bold text-gray-900 focus:outline-none cursor-pointer"
            >
              <option value="Nigeria">Nigeria (₦)</option>
              <option value="Ghana">Ghana (GH₵)</option>
              <option value="Kenya">Kenya (KSh)</option>
              <option value="South Africa">South Africa (R)</option>
            </select>
          </label>

          {activePage === 'hub' && (
            <div className="flex items-center bg-gray-100 p-0.5 rounded-lg gap-0.5">
              {ROLES.map((item) => {
                const active = role === item.id;
                return (
                  <button
                    key={item.id}
                    type="button"
                    onClick={() => onRoleChange(item.id)}
                    className={`px-2.5 py-1.5 rounded-md text-xs font-bold transition cursor-pointer ${
                      active
                        ? 'bg-[#14532D] text-white shadow-xs'
                        : 'text-gray-700 hover:bg-gray-200/70'
                    }`}
                  >
                    {item.label}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
