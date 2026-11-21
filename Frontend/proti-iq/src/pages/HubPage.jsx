import { useState } from 'react';
import ConsumerFlow from '../components/flows/ConsumerFlow';
import NutritionistFlow from '../components/flows/NutritionistFlow';
import ProcessorFlow from '../components/flows/ProcessorFlow';

export default function HubPage({ role, country, market, onOpenEvidence, onSwitchRole }) {
  const [resetKey, setResetKey] = useState(0);

  const normalizedRole = (role || 'consumer').toLowerCase();

  return (
    <div className="space-y-6">
      {(normalizedRole === 'consumer' || normalizedRole === 'caregiver') && (
        <ConsumerFlow
          key={`consumer-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
          onSwitchRole={onSwitchRole}
        />
      )}

      {normalizedRole === 'nutritionist' && (
        <NutritionistFlow
          key={`nutritionist-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
        />
      )}

      {(normalizedRole === 'processor' || normalizedRole === 'manufacturer') && (
        <ProcessorFlow
          key={`processor-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
        />
      )}

      {normalizedRole === 'researcher' && (
        <ProcessorFlow
          key={`researcher-${resetKey}`}
          country={country}
          market={market}
          onOpenEvidence={onOpenEvidence}
        />
      )}
    </div>
  );
}
