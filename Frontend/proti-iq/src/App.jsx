
import { useState } from 'react';
import Navbar from './components/Navbar';
import EvidenceDrawer from './components/EvidenceDrawer';
import ConsumerFlow from './components/flows/ConsumerFlow';
import NutritionistFlow from './components/flows/NutritionistFlow';
import ProcessorFlow from './components/flows/ProcessorFlow';
import { COUNTRY_MARKETS } from './data/protiData';

export default function App() {
  const [role, setRole] = useState('caregiver'); // 'caregiver' | 'nutritionist' | 'manufacturer'
  const [country, setCountry] = useState('Nigeria');
  const [resetKey, setResetKey] = useState(0);
  const [activeEvidence, setActiveEvidence] = useState(null);

  const handleRoleChange = (nextRole) => {
    setRole(nextRole);
    setResetKey((k) => k + 1);
  };

  const market = COUNTRY_MARKETS[country];

  return (
    <div className="min-h-screen bg-[#FAF9F6] text-[#111827] antialiased">
      <Navbar
        role={role}
        onRoleChange={handleRoleChange}
        country={country}
        onCountryChange={setCountry}
      />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-7">
        {role === 'caregiver' && (
          <ConsumerFlow
            key={`caregiver-${resetKey}`}
            country={country}
            market={market}
            onOpenEvidence={setActiveEvidence}
            onSwitchRole={handleRoleChange}
          />
        )}

        {role === 'nutritionist' && (
          <NutritionistFlow
            key={`nutritionist-${resetKey}`}
            country={country}
            market={market}
            onOpenEvidence={setActiveEvidence}
          />
        )}

        {role === 'manufacturer' && (
          <ProcessorFlow
            key={`manufacturer-${resetKey}`}
            country={country}
            market={market}
            onOpenEvidence={setActiveEvidence}
          />
        )}
      </main>

      <EvidenceDrawer
        evidence={activeEvidence}
        onClose={() => setActiveEvidence(null)}
      />
    </div>
  );
}