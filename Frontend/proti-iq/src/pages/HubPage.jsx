import { useState } from 'react';
import ConsumerFlow from '../components/flows/ConsumerFlow';
import NutritionistFlow from '../components/flows/NutritionistFlow';
import ProcessorFlow from '../components/flows/ProcessorFlow';

export default function HubPage({ role, country, market, onOpenEvidence, onSwitchRole }) {
  const [resetKey, setResetKey] = useState(0);

  const r = (role || 'consumer').toLowerCase();
  const isNutritionist = r.includes('nutri') || r.includes('diet') || r.includes('clinical');
  const isProcessor = r.includes('process') || r.includes('manufactur') || r.includes('factory');
  const isResearcher = r.includes('research') || r.includes('scien') || r.includes('academic') || r.includes('lab');

  return (
    <div className="space-y-6">
      {isNutritionist ? (
        <NutritionistFlow
          key={`nutritionist-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
        />
      ) : (isProcessor || isResearcher) ? (
        <ProcessorFlow
          key={`processor-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
        />
      ) : (
        <ConsumerFlow
          key={`consumer-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
          onSwitchRole={onSwitchRole}
        />
      )}
    </div>
  );
}
