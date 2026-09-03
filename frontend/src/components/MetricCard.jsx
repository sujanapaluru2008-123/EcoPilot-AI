function MetricCard({
  icon: Icon,
  label,
  value,
  unit,
  change,
  positive = true,
}) {
  return (
    <div className="rounded-2xl border border-slate-100 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">

      <div className="flex items-start justify-between">

        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-50">
          <Icon size={20} className="text-emerald-600" />
        </div>

        <span
          className={`rounded-full px-2.5 py-1 text-[11px] font-bold ${
            positive
              ? "bg-emerald-50 text-emerald-600"
              : "bg-amber-50 text-amber-600"
          }`}
        >
          {change}
        </span>

      </div>

      <p className="mt-5 text-sm font-medium text-slate-400">
        {label}
      </p>

      <div className="mt-1 flex items-baseline gap-1">
        <span className="text-2xl font-bold tracking-tight text-slate-900">
          {value}
        </span>

        <span className="text-xs font-medium text-slate-400">
          {unit}
        </span>
      </div>

    </div>
  );
}

export default MetricCard;