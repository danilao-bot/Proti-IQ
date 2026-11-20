import { useState } from 'react';
import ConsumerFlow from '../components/flows/ConsumerFlow';
import NutritionistFlow from '../components/flows/NutritionistFlow';
import ProcessorFlow from '../components/flows/ProcessorFlow';

export default function HubPage({ role, country, market, onOpenEvidence, onSwitchRole }) {
  const [resetKey, setResetKey] = useState(0);

  return (
    <div className="space-y-6">
      {role === 'caregiver' && (
        <ConsumerFlow
          key={`caregiver-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
          onSwitchRole={onSwitchRole}
        />
      )}

      {role === 'nutritionist' && (
        <NutritionistFlow
          key={`nutritionist-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
        />
      )}

      {role === 'manufacturer' && (
        <ProcessorFlow
          key={`manufacturer-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
        />
      )}
    </div>
  );
}
