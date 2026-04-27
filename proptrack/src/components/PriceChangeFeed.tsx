'use client'

const SOURCE_STYLE: Record<string, { bg: string; color: string }> = {
  magicbricks: { bg: '#E6F1FB', color: '#185FA5' },
  '99acres':   { bg: '#EEEDFE', color: '#534AB7' },
  squareyards: { bg: '#EAF3DE', color: '#3B6D11' },
}
const SOURCE_LABEL: Record<string, string> = {
  magicbricks: 'MB',
  '99acres':   '99A',
  squareyards: 'SY',
}

function fmt(n: number) {
  if (n >= 10_000_000) return `₹${(n / 10_000_000).toFixed(1)}Cr`
  if (n >= 100_000)    return `₹${(n / 100_000).toFixed(0)}L`
  return `₹${n.toLocaleString('en-IN')}`
}

export default function PriceChangeFeed({ data, loading }: { data: any[]; loading: boolean }) {
  return (
    <div className="rounded-xl p-5" style={{ background: 'var(--white)', border: '1px solid var(--ink-faint)' }}>
      <div className="flex items-center justify-between mb-4">
        <div className="text-xs font-medium uppercase tracking-wider" style={{ color: 'var(--ink-muted)' }}>
          Price changes
        </div>
        <span className="text-xs font-mono px-2 py-0.5 rounded" style={{ background: 'var(--coral-light)', color: 'var(--coral)' }}>
          SCD2 tracked
        </span>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-14 rounded animate-pulse" style={{ background: 'var(--surface)' }} />
          ))}
        </div>
      ) : data.length === 0 ? (
        <div className="py-12 text-center text-sm" style={{ color: 'var(--ink-muted)' }}>No price changes detected yet</div>
      ) : (
        <div className="overflow-y-auto space-y-1" style={{ maxHeight: 320 }}>
          {data.map((d, i) => {
            const pct   = Number(d.pct_change)
            const up    = pct >= 0
            const style = SOURCE_STYLE[d.source] || { bg: '#F1EFE8', color: '#5F5E5A' }

            return (
              <div
                key={i}
                className="flex items-center justify-between py-2.5 px-3 rounded-lg transition-colors"
                style={{ background: i % 2 === 0 ? 'var(--surface)' : 'transparent' }}
              >
                <div className="flex items-center gap-2 min-w-0">
                  <span
                    className="text-xs font-mono font-medium px-1.5 py-0.5 rounded flex-shrink-0"
                    style={{ background: style.bg, color: style.color }}
                  >
                    {SOURCE_LABEL[d.source] || d.source}
                  </span>
                  <div className="min-w-0">
                    <div className="text-xs font-medium truncate" style={{ color: 'var(--ink)', maxWidth: 140 }}>
                      {d.title || `${d.bhk} BHK, ${d.locality}`}
                    </div>
                    <div className="text-xs capitalize" style={{ color: 'var(--ink-muted)' }}>
                      {d.locality} · {d.city}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-3 flex-shrink-0">
                  <div className="text-right">
                    <div className="text-xs line-through" style={{ color: 'var(--ink-muted)' }}>
                      {fmt(Number(d.old_price))}
                    </div>
                    <div className="text-xs font-medium font-mono" style={{ color: 'var(--ink)' }}>
                      {fmt(Number(d.new_price))}
                    </div>
                  </div>
                  <div
                    className="text-xs font-mono font-medium px-2 py-0.5 rounded-full"
                    style={{
                      background: up ? '#E1F5EE' : '#FAECE7',
                      color: up ? '#0F6E56' : '#993C1D',
                      minWidth: 52,
                      textAlign: 'center',
                    }}
                  >
                    {up ? '+' : ''}{pct.toFixed(1)}%
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
