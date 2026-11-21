import React, { useState, useEffect } from 'react';
import LandingPage from './pages/LandingPage';
import OnboardingPage from './pages/OnboardingPage';
import WorkspacePage from './pages/WorkspacePage';
import LegalPage from './pages/LegalPage';
import DeleteDataPage from './pages/DeleteDataPage';
import HubPage from './pages/HubPage';
import StructurePage from './pages/StructurePage';
import EvidencePage from './pages/EvidencePage';
import CropsPage from './pages/CropsPage';
import CookieConsentBar from './components/CookieConsentBar';
import EvidenceDrawer from './components/EvidenceDrawer';
import { fetchSession, clearStoredToken } from './services/authClient';
import { COUNTRY_MARKETS } from './data/protiData';

export default function App() {
  const [session, setSession] = useState(null);
  const [currentPage, setCurrentPage] = useState('landing'); // 'landing' | 'onboarding' | 'workspace' | 'legal' | 'delete_data'
  const [activeSubView, setActiveSubView] = useState('workspace'); // 'workspace' | 'hub' | 'crops' | 'evidence' | 'structure'
  const [legalDocType, setLegalDocType] = useState('privacy');
  const [activeEvidence, setActiveEvidence] = useState(null);
  const [loadingSession, setLoadingSession] = useState(true);

  // Check existing session token on mount (Returning User Auto-Login)
  useEffect(() => {
    let active = true;
    fetchSession().then((sess) => {
      if (active) {
        if (sess && sess.authenticated) {
          setSession(sess);
          setCurrentPage('workspace');
        } else {
          setCurrentPage('landing');
        }
        setLoadingSession(false);
      }
    });
    return () => { active = false; };
  }, []);

  const handleOnboardingComplete = (newSession) => {
    setSession({
      authenticated: true,
      user_id: newSession.user_id,
      full_name: newSession.full_name,
      age: newSession.age,
      country: newSession.country,
      assigned_role: newSession.assigned_role,
      role_title: newSession.role_title,
      geriatric_mode: newSession.geriatric_mode,
      accessible_routes: newSession.accessible_routes
    });
    setCurrentPage('workspace');
    setActiveSubView('workspace');
  };

  const handleLogOut = () => {
    clearStoredToken();
    setSession(null);
    setCurrentPage('landing');
  };

  const handleOpenLegal = (docType) => {
    if (docType === 'delete') {
      setCurrentPage('delete_data');
    } else {
      setLegalDocType(docType);
      setCurrentPage('legal');
    }
  };

  const handleReturnFromLegal = () => {
    if (session && session.authenticated) {
      setCurrentPage('workspace');
    } else {
      setCurrentPage('landing');
    }
  };

  const handleDeletedData = () => {
    clearStoredToken();
    setSession(null);
    setCurrentPage('landing');
  };

  if (loadingSession) {
    return (
      <div className="min-h-screen bg-[#F9FAFB] flex items-center justify-center text-gray-600 text-base font-semibold">
        Verifying Proti IQ session authentication...
      </div>
    );
  }

  // 1. Landing Page
  if (currentPage === 'landing') {
    return (
      <>
        <LandingPage
          onStartOnboarding={() => setCurrentPage('onboarding')}
          onNavigateLegal={handleOpenLegal}
        />
        <CookieConsentBar onOpenCookiePolicy={() => handleOpenLegal('cookies')} />
      </>
    );
  }

  // 2. Onboarding Page
  if (currentPage === 'onboarding') {
    return (
      <>
        <OnboardingPage
          onOnboardingComplete={handleOnboardingComplete}
          onCancel={() => setCurrentPage('landing')}
        />
        <CookieConsentBar onOpenCookiePolicy={() => handleOpenLegal('cookies')} />
      </>
    );
  }

  // 3. Legal Document Page
  if (currentPage === 'legal') {
    return (
      <>
        <LegalPage docType={legalDocType} onBack={handleReturnFromLegal} />
        <CookieConsentBar onOpenCookiePolicy={() => handleOpenLegal('cookies')} />
      </>
    );
  }

  // 4. Data Deletion Page
  if (currentPage === 'delete_data') {
    return (
      <>
        <DeleteDataPage onBack={handleReturnFromLegal} onDeleted={handleDeletedData} />
        <CookieConsentBar onOpenCookiePolicy={() => handleOpenLegal('cookies')} />
      </>
    );
  }

  // 5. Authenticated Workspace
  const market = COUNTRY_MARKETS[session?.country] || COUNTRY_MARKETS['Nigeria'];

  return (
    <>
      {activeSubView === 'workspace' && (
        <WorkspacePage
          session={session}
          onLogOut={handleLogOut}
          onOpenLegal={handleOpenLegal}
          onNavigateView={setActiveSubView}
          activeSubView={activeSubView}
        />
      )}

      {activeSubView === 'hub' && (
        <div className="min-h-screen bg-[#F9FAFB]">
          <header className="bg-white border-b border-gray-200 px-4 sm:px-8 py-3 flex items-center justify-between">
            <span className="text-xl font-black text-[#14532D]">PROTI IQ DISCOVERY HUB</span>
            <button
              type="button"
              onClick={() => setActiveSubView('workspace')}
              className="px-3.5 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-bold cursor-pointer transition"
            >
              Return to Workspace
            </button>
          </header>
          <div className="max-w-7xl mx-auto p-6">
            <HubPage
              role={session?.assigned_role || 'consumer'}
              country={session?.country || 'Nigeria'}
              market={market}
              onOpenEvidence={setActiveEvidence}
              onSwitchRole={() => {}}
            />
          </div>
        </div>
      )}

      {activeSubView === 'crops' && (
        <div className="min-h-screen bg-[#F9FAFB]">
          <header className="bg-white border-b border-gray-200 px-4 sm:px-8 py-3 flex items-center justify-between">
            <span className="text-xl font-black text-[#14532D]">PAN-AFRICAN CROP CATALOG</span>
            <button
              type="button"
              onClick={() => setActiveSubView('workspace')}
              className="px-3.5 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-bold cursor-pointer transition"
            >
              Return to Workspace
            </button>
          </header>
          <div className="max-w-7xl mx-auto p-6">
            <CropsPage />
          </div>
        </div>
      )}

      {activeSubView === 'evidence' && (
        <div className="min-h-screen bg-[#F9FAFB]">
          <header className="bg-white border-b border-gray-200 px-4 sm:px-8 py-3 flex items-center justify-between">
            <span className="text-xl font-black text-[#14532D]">PRETORIA WET-LAB EVIDENCE</span>
            <button
              type="button"
              onClick={() => setActiveSubView('workspace')}
              className="px-3.5 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-bold cursor-pointer transition"
            >
              Return to Workspace
            </button>
          </header>
          <div className="max-w-7xl mx-auto p-6">
            <EvidencePage />
          </div>
        </div>
      )}

      {activeSubView === 'structure' && (
        <div className="min-h-screen bg-[#F9FAFB]">
          <header className="bg-white border-b border-gray-200 px-4 sm:px-8 py-3 flex items-center justify-between">
            <span className="text-xl font-black text-[#14532D]">3D ALPHAFOLD MOLECULAR VIEWER</span>
            <button
              type="button"
              onClick={() => setActiveSubView('workspace')}
              className="px-3.5 py-1.5 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-800 text-xs font-bold cursor-pointer transition"
            >
              Return to Workspace
            </button>
          </header>
          <div className="max-w-7xl mx-auto p-6">
            <StructurePage />
          </div>
        </div>
      )}

      {/* Slide-over Evidence Drawer */}
      {activeEvidence && (
        <EvidenceDrawer
          evidence={activeEvidence}
          onClose={() => setActiveEvidence(null)}
        />
      )}

      <CookieConsentBar onOpenCookiePolicy={() => handleOpenLegal('cookies')} />
    </>
  );
}
