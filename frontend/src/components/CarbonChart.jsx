import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { time: "08:00", carbon: 420 },
  { time: "10:00", carbon: 465 },
  { time: "12:00", carbon: 510 },
  { time: "14:00", carbon: 490 },
  { time: "16:00", carbon: 450 },
  { time: "18:00", carbon: 430 },
];

function CarbonChart() {
  return (
    <div className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">

      <div className="flex items-center justify-between">

        <div>
          <h3 className="font-bold text-slate-900">
            Carbon intensity
          </h3>

          <p className="mt-1 text-xs text-slate-400">
            Grid carbon signal
          </p>
        </div>

        <span className="rounded-lg bg-teal-50 px-3 py-1.5 text-xs font-bold text-teal-600">
          gCO₂/kWh
        </span>

      </div>

      <div className="mt-6 h-64">

        <ResponsiveContainer width="100%" height="100%">

          <AreaChart data={data}>

            <CartesianGrid
              strokeDasharray="3 3"
              vertical={false}
              stroke="#e2e8f0"
            />

            <XAxis
              dataKey="time"
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
            />

            <YAxis
              axisLine={false}
              tickLine={false}
              tick={{ fontSize: 11, fill: "#94a3b8" }}
            />

            <Tooltip />

            <Area
              type="monotone"
              dataKey="carbon"
              stroke="#0d9488"
              fill="#ccfbf1"
              strokeWidth={2}
            />

          </AreaChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default CarbonChart;