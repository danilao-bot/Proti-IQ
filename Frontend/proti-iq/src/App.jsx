import { useState } from 'react';
import Navbar from './components/Navbar';
import EvidenceDrawer from './components/EvidenceDrawer';
import HubPage from './pages/HubPage';
import StructurePage from './pages/StructurePage';
import EvidencePage from './pages/EvidencePage';
import CropsPage from './pages/CropsPage';
import { COUNTRY_MARKETS } from './data/protiData';

export default function App() {
  const [activePage, setActivePage] = useState('hub'); // 'hub' | 'structure' | 'evidence' | 'crops'
  const [role, setRole] = useState('caregiver'); // 'caregiver' | 'nutritionist' | 'manufacturer'
  const [country, setCountry] = useState('Nigeria');
  const [activeEvidence, setActiveEvidence] = useState(null);

  const market = COUNTRY_MARKETS[country] || COUNTRY_MARKETS['Nigeria'];

  return (
    <div className="min-h-screen bg-[#FAF9F6] text-[#111827] antialiased">
      <Navbar
        role={role}
        onRoleChange={setRole}
        country={country}
        onCountryChange={setCountry}
        activePage={activePage}
        onPageChange={setActivePage}
      />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 py-7">
        {activePage === 'hub' && (
          <HubPage
            role={role}
            country={country}
            market={market}
            onOpenEvidence={setActiveEvidence}
            onSwitchRole={setRole}
          />
        )}

        {activePage === 'structure' && <StructurePage />}

        {activePage === 'evidence' && <EvidencePage />}

        {activePage === 'crops' && <CropsPage />}
      </main>

      {/* Global Evidence Slide-Over Drawer */}
      {activeEvidence && (
        <EvidenceDrawer
          evidence={activeEvidence}
          onClose={() => setActiveEvidence(null)}
        />
      )}
    </div>
  );
}
