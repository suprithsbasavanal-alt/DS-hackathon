import React from 'react';
import {
  Wind,
  LayoutDashboard,
  LineChart,
  Target,
  ShieldAlert,
  FileCheck2,
  Calendar,
  WifiOff,
  Sparkles
} from 'lucide-react';

interface HeaderProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  latestDate?: string;
}

export const Header: React.FC<HeaderProps> = ({ activeTab, setActiveTab, latestDate = '2024-10-31' }) => {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'explorer', label: 'Explorer', icon: LineChart },
    { id: 'forecast', label: 'Forecast Arena', icon: Target },
    { id: 'ai-insights', label: 'AI Insights', icon: Sparkles },
    { id: 'health', label: 'Health Advisory', icon: ShieldAlert },
    { id: 'transparency', label: 'Data Transparency', icon: FileCheck2 },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-slate-200">
      {/* Historical Data Notice Banner */}
      <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-1.5 text-xs text-amber-900 flex items-center justify-between">
        <div className="flex items-center gap-2 max-w-7xl mx-auto w-full">
          <Calendar className="w-3.5 h-3.5 text-amber-600 shrink-0" />
          <span className="font-medium">
            <strong className="font-semibold text-amber-800">Historical Archive:</strong> Verified CPCB observations (Jan 1, 2023 – Oct 31, 2024). Latest available record: <span className="font-mono font-semibold">{latestDate}</span>. This is an offline data science product; not real-time conditions.
          </span>
          <div className="ml-auto hidden md:flex items-center gap-1.5 text-[11px] text-amber-700 font-mono">
            <WifiOff className="w-3 h-3 text-amber-600" />
            <span>100% Offline-First</span>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActiveTab('overview')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-teal-500 flex items-center justify-center text-white shadow-md shadow-sky-500/20">
              <Wind className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-bold text-lg text-slate-900 tracking-tight">BreatheWise</span>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-1.5 py-0.5 rounded bg-sky-100 text-sky-800 border border-sky-200">Bengaluru</span>
              </div>
              <p className="text-xs text-slate-500 font-medium">Air Quality & Meteorology Intelligence</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 sm:gap-2">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-sky-50 text-sky-700 shadow-sm ring-1 ring-sky-200'
                      : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-sky-600' : 'text-slate-400'}`} />
                  <span className="hidden md:inline">{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>
    </header>
  );
};
