'use client'

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts'

function fmtPrice(n: number) {
  if (n >= 10_000_000) return `₹${(n / 10_000_000).toFixed(1)}Cr`
  if (n >= 100_000)    return `₹${(n / 100_000).toFixed(0)}L`
  return `₹${n.toLocaleString('en-IN')}`
}

const COLORS = ['#9FE1CB', '#5DCAA5', '#1D9E75', '#0F6E56', '#085041']

export default function BhkChart({ data, loading }: { data: any[]; loading: boolean }) {
  const chartData = data.map(d => ({
    name: `${d.bhk} BHK`,
    avg_price: Number(d.avg_price),
    min_price: Number(d.min_price),
    max_price: Number(d.max_price),
    listings:  d.total_listings,
  }))

  return (
    <div className="rounded-xl p-5" style={{ background: 'var(--white)', border: '1px solid var(--ink-faint)', height: 320 }}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <div className="text-xs font-medium uppercase tracking-wider" style={{ color: 'var(--ink-muted)' }}>
            Avg price by BHK type
          </div>
        </div>
        <span className="text-xs font-mono px-2 py-0.5 rounded" style={{ background: 'var(--teal-light)', color: 'var(--teal-dark)' }}>
          {data.length} segments
        </span>
      </div>

      {loading ? (
        <div className="h-52 rounded-lg animate-pulse" style={{ background: 'var(--surface)' }} />
      ) : data.length === 0 ? (
        <div className="h-52 flex items-center justify-center text-sm" style={{ color: 'var(--ink-muted)' }}>
          No data for this selection
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={chartData} margin={{ top: 4, right: 8, left: 0, bottom: 0 }} barSize={40}>
            <CartesianGrid vertical={false} stroke="var(--ink-faint)" strokeDasharray="3 3" />
            <XAxis
              dataKey="name"
              tick={{ fontSize: 12, fill: 'var(--ink-muted)', fontFamily: 'DM Sans' }}
              axisLine={false} tickLine={false}
            />
            <YAxis
              tickFormatter={v => fmtPrice(v)}
              tick={{ fontSize: 11, fill: 'var(--ink-muted)', fontFamily: 'DM Mono' }}
              axisLine={false} tickLine={false} width={68}
            />
            <Tooltip
              formatter={(v: number) => [fmtPrice(v), 'Avg price']}
              contentStyle={{
                background: 'var(--ink)', border: 'none', borderRadius: 8,
                color: '#fff', fontSize: 12, fontFamily: 'DM Sans',
              }}
              itemStyle={{ color: '#9FE1CB' }}
              labelStyle={{ color: '#fff', fontWeight: 500 }}
              cursor={{ fill: 'rgba(0,0,0,0.04)' }}
            />
            <Bar dataKey="avg_price" radius={[6,6,0,0]}>
              {chartData.map((_, i) => (
                <Cell key={i} fill={COLORS[Math.min(i, COLORS.length - 1)]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}
    </div>
  )
}
