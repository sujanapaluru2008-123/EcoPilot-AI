import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const data = [
  { time: "08:00", energy: 82 },
  { time: "10:00", energy: 96 },
  { time: "12:00", energy: 108 },
  { time: "14:00", energy: 101 },
  { time: "16:00", energy: 94 },
  { time: "18:00", energy: 87 },
];

function EnergyChart() {
  return (
    <div className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">

      <div className="flex items-center justify-between">

        <div>
          <h3 className="font-bold text-slate-900">
            Energy trend
          </h3>

          <p className="mt-1 text-xs text-slate-400">
            Today's campus consumption
          </p>
        </div>

        <span className="rounded-lg bg-emerald-50 px-3 py-1.5 text-xs font-bold text-emerald-600">
          kWh
        </span>

      </div>

      <div className="mt-6 h-64">

        <ResponsiveContainer width="100%" height="100%">

          <LineChart data={data}>

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

            <Line
              type="monotone"
              dataKey="energy"
              stroke="#059669"
              strokeWidth={3}
              dot={false}
              activeDot={{ r: 5 }}
            />

          </LineChart>

        </ResponsiveContainer>

      </div>

    </div>
  );
}

export default EnergyChart;