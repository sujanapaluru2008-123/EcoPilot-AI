import {
  LayoutDashboard,
  Building2,
  BarChart3,
  Sparkles,
  ShieldCheck,
  Leaf,
  Activity,
} from "lucide-react";

function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 z-20 flex h-screen w-64 flex-col border-r border-emerald-100 bg-white px-5 py-6">

      {/* Logo */}
      <div className="flex items-center gap-3 px-2">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-emerald-600 shadow-lg shadow-emerald-200">
          <Leaf size={23} className="text-white" />
        </div>

        <div>
          <h1 className="text-lg font-bold tracking-tight text-emerald-950">
            EcoPilot
          </h1>
          <p className="text-[11px] font-semibold tracking-widest text-emerald-600">
            AI ENERGY INTELLIGENCE
          </p>
        </div>
      </div>

      {/* Navigation */}
      <div className="mt-10">

        <p className="px-3 text-[10px] font-bold tracking-[0.18em] text-slate-400">
          OVERVIEW
        </p>

        <nav className="mt-3 space-y-1">

          <button className="flex w-full items-center gap-3 rounded-xl bg-emerald-50 px-3 py-3 text-sm font-semibold text-emerald-800">
            <LayoutDashboard size={18} />
            Dashboard
          </button>

        </nav>

        <p className="mt-8 px-3 text-[10px] font-bold tracking-[0.18em] text-slate-400">
          MONITOR
        </p>

        <nav className="mt-3 space-y-1">

          <button className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50">
            <Building2 size={18} />
            Buildings
          </button>

          <button className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50">
            <BarChart3 size={18} />
            Analytics
          </button>

        </nav>

        <p className="mt-8 px-3 text-[10px] font-bold tracking-[0.18em] text-slate-400">
          ACTION
        </p>

        <nav className="mt-3 space-y-1">

          <button className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50">
            <Sparkles size={18} />
            Recommendations
          </button>

          <button className="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-sm font-medium text-slate-600 transition hover:bg-slate-50">
            <ShieldCheck size={18} />
            Verification
          </button>

        </nav>
      </div>

      {/* Bottom status */}
      <div className="mt-auto rounded-2xl bg-slate-50 p-4">
        <div className="flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-60" />
            <span className="relative inline-flex h-3 w-3 rounded-full bg-emerald-500" />
          </span>

          <span className="text-xs font-bold text-slate-700">
            System Live
          </span>
        </div>

        <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
          <Activity size={13} />
          Monitoring campus energy
        </div>
      </div>

    </aside>
  );
}

export default Sidebar;