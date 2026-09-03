import {
  Sparkles,
  ArrowUpRight,
  Zap,
  Leaf,
  IndianRupee,
  ChevronRight,
} from "lucide-react";

function RecommendationCard() {
  return (
    <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-emerald-950 via-emerald-900 to-teal-900 p-7 text-white shadow-xl shadow-emerald-100">

      {/* Decorative glow */}
      <div className="absolute -right-16 -top-16 h-48 w-48 rounded-full bg-emerald-400/10 blur-3xl" />

      <div className="relative">

        {/* Header */}
        <div className="flex items-center justify-between">

          <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-white/10">
              <Sparkles size={18} className="text-emerald-300" />
            </div>

            <span className="text-xs font-bold tracking-[0.15em] text-emerald-200">
              OPTIMIZATION OPPORTUNITY
            </span>
          </div>

          <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs font-semibold text-emerald-200">
            92% confidence
          </span>

        </div>

        {/* Recommendation */}
        <div className="mt-7">

          <p className="text-sm text-emerald-200">
            Recommended action
          </p>

          <h2 className="mt-1 text-3xl font-bold tracking-tight">
            Reduce lighting load
          </h2>

          <p className="mt-3 max-w-2xl text-sm leading-6 text-emerald-100/75">
            High daylight and moderate occupancy make lighting
            reduction a suitable low-impact action right now.
          </p>

        </div>

        {/* Impact */}
        <div className="mt-7 grid grid-cols-3 gap-3">

          <div className="rounded-2xl bg-white/10 p-4 backdrop-blur-sm">
            <Zap size={17} className="text-emerald-300" />
            <p className="mt-3 text-xl font-bold">
              12.4 kWh
            </p>
            <p className="mt-1 text-xs text-emerald-200/60">
              Energy saving
            </p>
          </div>

          <div className="rounded-2xl bg-white/10 p-4 backdrop-blur-sm">
            <Leaf size={17} className="text-emerald-300" />
            <p className="mt-3 text-xl font-bold">
              6.2 kg
            </p>
            <p className="mt-1 text-xs text-emerald-200/60">
              CO₂ reduction
            </p>
          </div>

          <div className="rounded-2xl bg-white/10 p-4 backdrop-blur-sm">
            <IndianRupee size={17} className="text-emerald-300" />
            <p className="mt-3 text-xl font-bold">
              ₹99
            </p>
            <p className="mt-1 text-xs text-emerald-200/60">
              Cost saving
            </p>
          </div>

        </div>

        {/* Action */}
        <button className="mt-6 flex items-center gap-2 rounded-xl bg-white px-4 py-3 text-sm font-bold text-emerald-900 transition hover:bg-emerald-50">
          View optimization details
          <ChevronRight size={16} />
          <ArrowUpRight size={14} />
        </button>

      </div>
    </div>
  );
}

export default RecommendationCard;