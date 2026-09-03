import {
  Zap,
  Leaf,
  IndianRupee,
  Users,
  ChevronDown,
  Clock,
} from "lucide-react";

import Sidebar from "./components/sidebar";
import MetricCard from "./components/MetricCard";
import RecommendationCard from "./components/RecommendationCard";
import EnergyChart from "./components/EnergyChart";
import CarbonChart from "./components/CarbonChart";

function App() {
  return (
    <div className="min-h-screen bg-[#f4f8f5]">

      {/* Sidebar */}
      <Sidebar />

      {/* Main content */}
      <main className="ml-64 min-h-screen px-8 py-7">

        {/* Header */}
        <header className="flex items-center justify-between">

          <div>
            <p className="text-sm font-medium text-emerald-600">
              Sustainability Command Center
            </p>

            <h1 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
              Good evening, Facility Manager 👋
            </h1>

            <p className="mt-2 text-sm text-slate-500">
              Here's what's happening across your campus today.
            </p>
          </div>

          {/* Building selector */}
          <div className="flex items-center gap-3">

            <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 shadow-sm">

              <span className="h-2 w-2 rounded-full bg-emerald-500" />

              <select className="cursor-pointer bg-transparent text-sm font-semibold text-slate-700 outline-none">
                <option>Engineering Block</option>
                <option>Library</option>
                <option>Admin Block</option>
                <option>Innovation Centre</option>
                <option>Hostel Block</option>
              </select>

              <ChevronDown size={15} className="text-slate-400" />

            </div>

            <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-medium text-slate-500 shadow-sm">
              <Clock size={14} />
              Updated 2 min ago
            </div>

          </div>

        </header>

        {/* Metrics */}
        <section className="mt-8 grid grid-cols-4 gap-5">

          <MetricCard
            icon={Zap}
            label="Energy consumption"
            value="487"
            unit="kWh"
            change="↓ 8.4%"
          />

          <MetricCard
            icon={Leaf}
            label="Carbon emissions"
            value="231"
            unit="kg CO₂"
            change="↓ 6.2%"
          />

          <MetricCard
            icon={IndianRupee}
            label="Estimated cost"
            value="3,896"
            unit="INR"
            change="↓ 5.8%"
          />

          <MetricCard
            icon={Users}
            label="Current occupancy"
            value="68"
            unit="%"
            change="Live"
            positive={false}
          />

        </section>

        {/* Main recommendation */}
        <section className="mt-6">

          <RecommendationCard />

        </section>

        {/* Charts */}
        <section className="mt-6 grid grid-cols-2 gap-5">

          <EnergyChart />

          <CarbonChart />

        </section>

        {/* Bottom info */}
        <section className="mt-6 rounded-2xl border border-emerald-100 bg-emerald-50/60 px-5 py-4">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white">
              <Leaf size={18} className="text-emerald-600" />
            </div>

            <div>
              <p className="text-sm font-bold text-emerald-900">
                EcoPilot is continuously evaluating energy decisions
              </p>

              <p className="mt-0.5 text-xs text-emerald-700/70">
                Recommendations consider occupancy, weather, daylight,
                energy usage and grid carbon intensity.
              </p>
            </div>

          </div>

        </section>

      </main>

    </div>
  );
}

export default App;