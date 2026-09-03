
import {
  Sparkles,
  ArrowUpRight,
  Zap,
  Leaf,
  IndianRupee,
  ChevronRight,
} from "lucide-react";


function RecommendationCard({ recommendation }) {

  // ============================================================
  // LOADING / FALLBACK STATE
  // ============================================================

  if (!recommendation) {

    return (
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-950 via-emerald-900 to-teal-900 p-7 text-white shadow-xl shadow-emerald-100">

        <div className="absolute -right-16 -top-16 h-48 w-48 rounded-full bg-emerald-400/10 blur-3xl" />

        <div className="relative">

          <div className="flex items-center gap-2">

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/10">

              <Sparkles
                size={18}
                className="text-emerald-300"
              />

            </div>

            <span className="text-xs font-bold tracking-[0.15em] text-emerald-200">
              OPTIMIZATION OPPORTUNITY
            </span>

          </div>


          <div className="mt-7">

            <p className="text-sm text-emerald-200">
              EcoPilot is analyzing...
            </p>

            <h2 className="mt-1 text-3xl font-bold tracking-tight">
              Finding the best action
            </h2>

            <p className="mt-3 max-w-2xl text-sm leading-6 text-emerald-100/75">
              Our optimization engine is evaluating the
              current building conditions.
            </p>

          </div>

        </div>

      </div>
    );
  }


  // ============================================================
  // BACKEND RECOMMENDATION DATA
  // ============================================================

  const {
    action,
    confidence,
    energy_saving_kwh,
    carbon_reduction_kg,
    cost_saving_inr,
    comfort_impact,
    reason,
  } = recommendation;


  // ============================================================
  // MAIN CARD
  // ============================================================

  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-950 via-emerald-900 to-teal-900 p-7 text-white shadow-xl shadow-emerald-100">

      {/* Decorative glow */}

      <div className="absolute -right-16 -top-16 h-48 w-48 rounded-full bg-emerald-400/10 blur-3xl" />


      <div className="relative">


        {/* ====================================================
            HEADER
        ==================================================== */}

        <div className="flex items-center justify-between">

          <div className="flex items-center gap-2">

            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/10">

              <Sparkles
                size={18}
                className="text-emerald-300"
              />

            </div>

            <span className="text-xs font-bold tracking-[0.15em] text-emerald-200">
              OPTIMIZATION OPPORTUNITY
            </span>

          </div>


          {/* Confidence */}

          <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-semibold text-emerald-200">

            {confidence}% confidence

          </span>

        </div>


        {/* ====================================================
            RECOMMENDED ACTION
        ==================================================== */}

        <div className="mt-7">

          <p className="text-sm text-emerald-200">
            Recommended action
          </p>

          <h2 className="mt-1 text-3xl font-bold tracking-tight">
            {action}
          </h2>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-emerald-100/75">
            {reason}
          </p>

        </div>


        {/* ====================================================
            IMPACT CARDS
        ==================================================== */}

        <div className="mt-7 grid grid-cols-3 gap-3">


          {/* Energy */}

          <div className="rounded-2xl bg-white/10 p-4 backdrop-blur-sm">

            <Zap
              size={17}
              className="text-emerald-300"
            />

            <p className="mt-3 text-xl font-bold">

              {Number(energy_saving_kwh).toFixed(1)} kWh

            </p>

            <p className="mt-1 text-xs text-emerald-200/60">
              Energy saving
            </p>

          </div>


          {/* Carbon */}

          <div className="rounded-2xl bg-white/10 p-4 backdrop-blur-sm">

            <Leaf
              size={17}
              className="text-emerald-300"
            />

            <p className="mt-3 text-xl font-bold">

              {Number(carbon_reduction_kg).toFixed(1)} kg

            </p>

            <p className="mt-1 text-xs text-emerald-200/60">
              CO₂ reduction
            </p>

          </div>


          {/* Cost */}

          <div className="rounded-2xl bg-white/10 p-4 backdrop-blur-sm">

            <IndianRupee
              size={17}
              className="text-emerald-300"
            />

            <p className="mt-3 text-xl font-bold">

              ₹{Math.round(
                Number(cost_saving_inr)
              ).toLocaleString("en-IN")}

            </p>

            <p className="mt-1 text-xs text-emerald-200/60">
              Cost saving
            </p>

          </div>

        </div>


        {/* ====================================================
            COMFORT IMPACT
        ==================================================== */}

        <div className="mt-4">

          <span className="text-xs text-emerald-200/70">

            Comfort impact:{" "}

            <span className="font-semibold text-emerald-100">

              {comfort_impact}

            </span>

          </span>

        </div>


        {/* ====================================================
            DETAILS BUTTON
        ==================================================== */}

        <button
          type="button"
          className="mt-6 flex items-center gap-2 rounded-xl bg-white px-4 py-3 text-sm font-bold text-emerald-900 transition hover:bg-emerald-50"
        >

          View optimization details

          <ChevronRight size={16} />

          <ArrowUpRight size={14} />

        </button>


      </div>

    </div>
  );
}


export default RecommendationCard;