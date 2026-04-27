'use client'

import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts'

const COLORS: Record<string, string> = {
  magicbricks: '#378ADD',
  '99acres':   '#AFA9EC',
  squareyards: '#1D9E75',
}
const LABELS: Record<string, string> = {
  magicbricks: 'MagicBricks',
  '99acres':   '99acres',
  squareyards: 'SquareYards',
}

export default function SourceDonut({ data, loading }: { data: any[]; loading: boolean }) {
  const total = data.reduce((s, d) => s + Number(d.total_listings), 0)

  return (
    <div className="rounded-xl p-5" style={{ background: 'var(--white)', border: '1px solid var(--ink-faint)', height: 320 }}>
      <div className="text-xs font-medium uppercase tracking-wider mb-4" style={{ color: 'var(--ink-muted)' }}>
        Listings by source
      </div>

      {loading ? (
        <div className="h-40 rounded-full mx-auto w-40 animate-pulse" style={{ background: 'var(--surface)' }} />
      ) : (
        <>
          <div className="relative" style={{ height: 160 }}>
            <ResponsiveContainer width="100%" height={160}>
              <PieChart>
                <Pie
                  data={data}
                  dataKey="total_listings"
                  nameKey="source"
                  cx="50%" cy="50%"
                  innerRadius={50} outerRadius={72}
                  paddingAngle={3}
                  strokeWidth={0}
                >
                  {data.map((d, i) => (
                    <Cell key={i} fill={COLORS[d.source] || '#888'} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(v: number) => [v, 'Listings']}
                  contentStyle={{
                    background: 'var(--ink)', border: 'none', borderRadius: 8,
                    color: '#fff', fontSize: 12,
                  }}
                />
              </PieChart>
            </ResponsiveContainer>
            <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
              <div className="text-2xl font-display font-medium" style={{ color: 'var(--ink)' }}>{total}</div>
              <div className="text-xs" style={{ color: 'var(--ink-muted)' }}>total</div>
            </div>
          </div>

          <div className="mt-4 space-y-2">
            {data.map((d, i) => (
              <div key={i} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full" style={{ background: COLORS[d.source] || '#888' }} />
                  <span className="text-xs" style={{ color: 'var(--ink-muted)' }}>{LABELS[d.source] || d.source}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono" style={{ color: 'var(--ink)' }}>{d.total_listings}</span>
                  <span className="text-xs" style={{ color: 'var(--ink-muted)' }}>
                    {total ? Math.round(d.total_listings / total * 100) : 0}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
