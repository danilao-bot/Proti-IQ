
const ROLES = [
  { id: 'caregiver', label: 'Consumer / Caregiver' },
  { id: 'nutritionist', label: 'Nutritionist' },
  { id: 'manufacturer', label: 'Food Manufacturer' },
];

export default function Navbar({ role, onRoleChange, country, onCountryChange }) {
  return (
    <header className="sticky top-0 z-30 bg-white border-b border-gray-200">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-3">
        {/* Brand */}
        <button
          type="button"
          onClick={() => onRoleChange(role)}
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
                African Protein AI
              </span>
            </div>
            <p className="text-xs text-gray-500 mt-0.5">Africanized Alternative Proteins</p>
          </div>
        </button>

        {/* Country + Role Switcher */}
        <div className="flex flex-wrap items-center gap-2.5">
          <label className="flex items-center gap-1.5 text-sm font-medium text-gray-700 bg-gray-50 border border-gray-300 rounded-xl px-3 py-2">
            <span className="text-gray-500">Country:</span>
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

          <nav aria-label="Persona Switcher" className="flex items-center bg-gray-100 p-1 rounded-xl gap-1">
            {ROLES.map((item) => {
              const active = role === item.id;
              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => onRoleChange(item.id)}
                  className={`px-3.5 py-2 rounded-lg text-sm font-bold whitespace-nowrap transition cursor-pointer ${
                    active
                      ? 'bg-[#14532D] text-white shadow-xs'
                      : 'text-gray-700 hover:bg-gray-200/70'
                  }`}
                >
                  {item.label}
                </button>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
}