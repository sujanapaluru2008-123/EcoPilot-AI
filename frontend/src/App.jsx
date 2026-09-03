import { useEffect, useState } from "react";

import {
  Zap,
  Leaf,
  IndianRupee,
  Users,
  Clock,
} from "lucide-react";

import Sidebar from "./components/sidebar";
import MetricCard from "./components/MetricCard";
import RecommendationCard from "./components/RecommendationCard";
import EnergyChart from "./components/EnergyChart";
import CarbonChart from "./components/CarbonChart";

import {
  getBuildings,
  getDashboard,
  getHistory,
} from "./services/api";


function App() {
  // ============================================================
  // STATE
  // ============================================================

  const [buildings, setBuildings] = useState([]);

  const [selectedBuilding, setSelectedBuilding] =
    useState("Innovation Centre");

  const [dashboard, setDashboard] = useState(null);

  const [history, setHistory] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");


  // ============================================================
  // LOAD BUILDING LIST
  // ============================================================

  useEffect(() => {
    async function loadBuildings() {
      try {
        const data = await getBuildings();

        setBuildings(data.buildings);
      } catch (err) {
        console.error(err);

        setError(
          "Unable to load campus buildings."
        );
      }
    }

    loadBuildings();
  }, []);


  // ============================================================
  // LOAD SELECTED BUILDING DATA
  // ============================================================

  useEffect(() => {
    async function loadBuildingData() {
      if (!selectedBuilding) {
        return;
      }

      try {
        setLoading(true);

        setError("");

        const [dashboardData, historyData] =
          await Promise.all([
            getDashboard(selectedBuilding),
            getHistory(selectedBuilding),
          ]);

        setDashboard(dashboardData);

        setHistory(historyData.history);
      } catch (err) {
        console.error(err);

        setError(
          "Unable to load building data."
        );
      } finally {
        setLoading(false);
      }
    }

    loadBuildingData();
  }, [selectedBuilding]);


  // ============================================================
  // LOADING SCREEN
  // ============================================================

  if (loading && !dashboard) {
    return (
      <div className="min-h-screen bg-[#f4f8f5]">

        <Sidebar />

        <main className="ml-64 flex min-h-screen items-center justify-center">

          <div className="text-center">

            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-emerald-100">

              <Leaf
                size={28}
                className="animate-pulse text-emerald-600"
              />

            </div>

            <h2 className="text-xl font-bold text-slate-800">
              EcoPilot is thinking...
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Loading campus energy intelligence
            </p>

          </div>

        </main>

      </div>
    );
  }


  // ============================================================
  // ERROR SCREEN
  // ============================================================

  if (error && !dashboard) {
    return (
      <div className="min-h-screen bg-[#f4f8f5]">

        <Sidebar />

        <main className="ml-64 flex min-h-screen items-center justify-center">

          <div className="rounded-2xl border border-red-100 bg-white p-8 text-center shadow-sm">

            <h2 className="text-xl font-bold text-slate-800">
              Something went wrong
            </h2>

            <p className="mt-2 text-sm text-red-500">
              {error}
            </p>

          </div>

        </main>

      </div>
    );
  }


  // ============================================================
  // DATA FROM BACKEND
  // ============================================================

  const conditions =
    dashboard?.current_conditions;

  const recommendation =
    dashboard?.recommendation;


  // ============================================================
  // ENERGY
  // ============================================================

  const energy =
    conditions?.current_energy_kwh ?? 0;


  // ============================================================
  // CARBON
  // ============================================================

  const carbon =
    conditions
      ? (
          energy *
          conditions.grid_carbon_intensity
        ) / 1000
      : 0;


  // ============================================================
  // ESTIMATED COST
  // Prototype tariff = ₹8/kWh
  // ============================================================

  const cost =
    energy * 8;


  // ============================================================
  // OCCUPANCY
  // ============================================================

  const occupancy =
    conditions?.occupancy_percent ?? 0;


  // ============================================================
  // MAIN UI
  // ============================================================

  return (
    <div className="min-h-screen bg-[#f4f8f5]">

      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <Sidebar />


      {/* ======================================================
          MAIN CONTENT
      ====================================================== */}

      <main className="ml-64 min-h-screen px-8 py-7">


        {/* ====================================================
            HEADER
        ==================================================== */}

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

              <select
                value={selectedBuilding}
                onChange={(event) =>
                  setSelectedBuilding(event.target.value)
                }
                className="cursor-pointer bg-transparent text-sm font-semibold text-slate-700 outline-none"
              >

                {buildings.map((building) => (
                  <option
                    key={building}
                    value={building}
                  >
                    {building}
                  </option>
                ))}

              </select>

            </div>


            {/* Live status */}

            <div className="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-xs font-medium text-slate-500 shadow-sm">

              <Clock size={14} />

              {loading
                ? "Updating..."
                : "Live data"}

            </div>

          </div>

        </header>


        {/* ====================================================
            ERROR MESSAGE
        ==================================================== */}

        {error && (
          <div className="mt-4 rounded-xl border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-600">

            {error}

          </div>
        )}


        {/* ====================================================
            METRICS
        ==================================================== */}

        <section className="mt-8 grid grid-cols-4 gap-5">

          <MetricCard
            icon={Zap}
            label="Energy consumption"
            value={energy.toFixed(1)}
            unit="kWh"
            change="Live"
          />

          <MetricCard
            icon={Leaf}
            label="Carbon emissions"
            value={carbon.toFixed(1)}
            unit="kg CO₂"
            change="Live"
          />

          <MetricCard
            icon={IndianRupee}
            label="Estimated cost"
            value={Math.round(cost).toLocaleString("en-IN")}
            unit="INR"
            change="Live"
          />

          <MetricCard
            icon={Users}
            label="Current occupancy"
            value={occupancy.toFixed(0)}
            unit="%"
            change="Live"
            positive={false}
          />

        </section>


        {/* ====================================================
            REAL OPTIMIZATION RECOMMENDATION
        ==================================================== */}

        <section className="mt-6">

          <RecommendationCard
            recommendation={recommendation}
          />

        </section>


        {/* ====================================================
            CHARTS
        ==================================================== */}

        <section className="mt-6 grid grid-cols-2 gap-5">

          <EnergyChart />

          <CarbonChart />

        </section>


        {/* ====================================================
            BOTTOM INFO
        ==================================================== */}

        <section className="mt-6 rounded-2xl border border-emerald-100 bg-emerald-50/60 px-5 py-4">

          <div className="flex items-center gap-3">

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white">

              <Leaf
                size={18}
                className="text-emerald-600"
              />

            </div>

            <div>

              <p className="text-sm font-bold text-emerald-900">
                EcoPilot is continuously evaluating energy decisions
              </p>

              <p className="mt-0.5 text-xs text-emerald-700/70">
                Recommendations consider occupancy, weather,
                daylight, energy usage and grid carbon intensity.
              </p>

            </div>

          </div>

        </section>


      </main>

    </div>
  );
}


export default App;