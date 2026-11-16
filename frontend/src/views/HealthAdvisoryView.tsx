import React, { useState } from 'react';
import {
  ShieldAlert,
  Heart,
  Users,
  Baby,
  Activity,
  AlertTriangle,
  Clock,
  Compass,
  CheckCircle2,
  Info
} from 'lucide-react';
import { DiurnalData } from '../types';

interface HealthAdvisoryViewProps {
  currentAqi?: number;
  currentCategory?: string;
  diurnalData: DiurnalData | null;
}

export const HealthAdvisoryView: React.FC<HealthAdvisoryViewProps> = ({
  currentAqi = 141,
  currentCategory = 'Moderate',
  diurnalData
}) => {
  const [selectedTier, setSelectedTier] = useState<string>(currentCategory);

  const cpcbTiers = [
    {
      name: 'Good',
      range: '0 – 50',
      color: '#10b981',
      bgClass: 'bg-emerald-50 border-emerald-200 text-emerald-950',
      badgeClass: 'bg-emerald-100 text-emerald-800 border-emerald-300',
      impact: 'Minimal health impact.',
      generalAdvice: 'Air quality is considered satisfactory, and air pollution poses little or no risk.',
      sensitiveAdvice: 'Enjoy outdoor activities without restrictions.'
    },
    {
      name: 'Satisfactory',
      range: '51 – 100',
      color: '#84cc16',
      bgClass: 'bg-lime-50 border-lime-200 text-lime-950',
      badgeClass: 'bg-lime-100 text-lime-800 border-lime-300',
      impact: 'Minor breathing discomfort to sensitive people.',
      generalAdvice: 'Air quality is acceptable for most citizens.',
      sensitiveAdvice: 'Unusually sensitive individuals should monitor respiratory symptoms during prolonged outdoor exertion.'
    },
    {
      name: 'Moderate',
      range: '101 – 200',
      color: '#eab308',
      bgClass: 'bg-amber-50 border-amber-200 text-amber-950',
      badgeClass: 'bg-amber-100 text-amber-800 border-amber-300',
      impact: 'Breathing discomfort to people with lung disease, asthma, and heart conditions.',
      generalAdvice: 'Most healthy individuals can continue ordinary routines, but prolonged high-intensity outdoor workouts may cause fatigue.',
      sensitiveAdvice: 'People with asthma, COPD, and cardiovascular conditions should take breaks and carry prescribed rescue medication.'
    },
    {
      name: 'Poor',
      range: '201 – 300',
      color: '#f97316',
      bgClass: 'bg-orange-50 border-orange-200 text-orange-950',
      badgeClass: 'bg-orange-100 text-orange-800 border-orange-300',
      impact: 'Breathing discomfort to most people on prolonged exposure.',
      generalAdvice: 'Everyone may begin to experience minor throat irritation or coughing during extended outdoor exertion.',
      sensitiveAdvice: 'Children, the elderly, and individuals with respiratory conditions should significantly reduce strenuous outdoor exercise.'
    },
    {
      name: 'Very Poor',
      range: '301 – 400',
      color: '#ef4444',
      bgClass: 'bg-red-50 border-red-200 text-red-950',
      badgeClass: 'bg-red-100 text-red-800 border-red-300',
      impact: 'Respiratory illness on prolonged exposure; pronounced effect on vulnerable groups.',
      generalAdvice: 'Avoid outdoor exercise in early mornings and late evenings. Use N95 masks when commuting near heavy arterial traffic.',
      sensitiveAdvice: 'Vulnerable groups should remain indoors in well-ventilated or filtered rooms. Avoid all outdoor exertion.'
    },
    {
      name: 'Severe',
      range: '401 – 500',
      color: '#991b1b',
      bgClass: 'bg-rose-50 border-rose-200 text-rose-950',
      badgeClass: 'bg-rose-200 text-rose-900 border-rose-300',
      impact: 'Affects healthy people and seriously impacts those with existing medical conditions.',
      generalAdvice: 'Public health emergency category. Restrict outdoor movement, close windows during peak hours, and follow municipal health advisories.',
      sensitiveAdvice: 'Strict indoor confinement for all vulnerable groups. Seek prompt medical care if experiencing respiratory distress.'
    }
  ];

  const activeTier = cpcbTiers.find((t) => t.name === selectedTier) || cpcbTiers[2];

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-sky-100 text-sky-800 border border-sky-200">
            CPCB Regulatory Standard
          </span>
          <span className="text-xs text-slate-500">6-Tier Health Guidance System</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Public Health Advisory & Vulnerable Population Safeguards
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Evidence-based guidance aligned with official Central Pollution Control Board (CPCB) health impact descriptors.
        </p>
      </div>

      {/* CPCB 6-Tier Interactive Selector */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {cpcbTiers.map((tier) => {
          const isSelected = tier.name === selectedTier;
          return (
            <button
              key={tier.name}
              onClick={() => setSelectedTier(tier.name)}
              className={`p-3.5 rounded-xl border text-left transition-all ${
                isSelected
                  ? 'ring-2 ring-slate-900 shadow-md font-bold'
                  : 'bg-white hover:bg-slate-50 border-slate-200'
              }`}
            >
              <div className="flex items-center justify-between mb-1">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: tier.color }}></span>
                <span className="font-mono text-[11px] text-slate-400">{tier.range}</span>
              </div>
              <div className="font-bold text-sm text-slate-900">{tier.name}</div>
              <div className="text-[10px] text-slate-500 mt-0.5 line-clamp-1">{tier.impact}</div>
            </button>
          );
        })}
      </div>

      {/* Active Tier Advisory Detail Card */}
      <div className={`rounded-2xl border p-6 sm:p-8 ${activeTier.bgClass} space-y-6 shadow-sm`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-black/10">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`text-xs font-bold px-2.5 py-0.5 rounded-full border ${activeTier.badgeClass}`}>
                AQI Index: {activeTier.range}
              </span>
              {activeTier.name === currentCategory && (
                <span className="text-xs font-semibold px-2 py-0.5 rounded bg-black/5 text-slate-800">
                  Matches Latest Observation (Oct 31, 2024: AQI {currentAqi})
                </span>
              )}
            </div>
            <h2 className="text-2xl font-black tracking-tight">{activeTier.name} Category Advisory</h2>
            <p className="text-sm font-medium mt-1 opacity-90">{activeTier.impact}</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white/80 rounded-xl p-5 border border-black/5 space-y-2">
            <div className="flex items-center gap-2 font-bold text-sm text-slate-900">
              <Users className="w-4 h-4 text-sky-600" />
              <span>General Citizen Guidance</span>
            </div>
            <p className="text-xs text-slate-700 leading-relaxed">{activeTier.generalAdvice}</p>
          </div>

          <div className="bg-white/80 rounded-xl p-5 border border-black/5 space-y-2">
            <div className="flex items-center gap-2 font-bold text-sm text-slate-900">
              <Heart className="w-4 h-4 text-rose-500" />
              <span>Sensitive & Vulnerable Populations</span>
            </div>
            <p className="text-xs text-slate-700 leading-relaxed">{activeTier.sensitiveAdvice}</p>
          </div>
        </div>
      </div>

      {/* Vulnerable Groups Protective Protocols */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-4">
        <h3 className="font-bold text-slate-900 text-base flex items-center gap-2">
          <ShieldAlert className="w-4 h-4 text-teal-600" />
          <span>Vulnerable Population Protective Measures</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-2">
            <div className="flex items-center gap-2 font-bold text-slate-800">
              <Baby className="w-4 h-4 text-sky-600" />
              <span>Children & Infants</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              Children have higher minute-ventilation rates per body mass and narrower airways. Avoid placing play areas near high-density traffic junctions during peak hours.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-2">
            <div className="flex items-center gap-2 font-bold text-slate-800">
              <Activity className="w-4 h-4 text-rose-500" />
              <span>Asthma & COPD Patients</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              Maintain emergency bronchodilators at hand. On days exceeding AQI 150 (Moderate upper bracket), shift high-aerobic exercise indoors away from direct roadways.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 space-y-2">
            <div className="flex items-center gap-2 font-bold text-slate-800">
              <Users className="w-4 h-4 text-amber-600" />
              <span>Outdoor Gig & Delivery Workers</span>
            </div>
            <p className="text-slate-600 leading-relaxed">
              Prolonged road exposure requires certified N95 or FFP2 respirators with tight facial seals to mitigate respirable fine particle inhalation during commute peaks.
            </p>
          </div>
        </div>
      </div>

      {/* Station-Specific Commuter Diurnal Guidance */}
      <div className="bg-white rounded-2xl border border-slate-200/80 shadow-sm p-6 space-y-3">
        <div className="flex items-center gap-2 font-bold text-slate-900 text-base">
          <Clock className="w-4 h-4 text-sky-600" />
          <span>Historical Commute Elevation Patterns (BTM Layout & Peenya)</span>
        </div>

        <div className="space-y-2 text-xs text-slate-600 leading-relaxed">
          <p>
            • <strong>Morning Transit Window (07:00 – 09:00):</strong> NO2 averages demonstrate historical peaks during these hours at BTM Layout (reaching ~36 µg/m³), coinciding with morning commuter vehicular movements.
          </p>
          <p>
            • <strong>Late Evening Window (20:00 – 23:00):</strong> PM10 and PM2.5 concentrations are historically elevated (averaging ~72–77 µg/m³ PM10) at both BTM Layout and Peenya.
          </p>
          <p>
            • <strong>Midday Window (12:00 – 16:00):</strong> Both stations historically observe lower particulate concentrations (~47 µg/m³ at BTM).
          </p>
        </div>

        <div className="mt-2 p-3 bg-amber-50/70 rounded-xl border border-amber-200/60 text-[11px] text-amber-900">
          <strong>Important Scientific Disclaimer:</strong> These diurnal patterns represent historical descriptive observations recorded specifically at the BTM Layout and Peenya monitoring stations. They are not universal citywide generalizations and do not constitute individualized medical advice.
        </div>
      </div>
    </div>
  );
};
