'use client'

function fmt(n: number) {
  if (n >= 10_000_000) return `₹${(n / 10_000_000).toFixed(1)} Cr`
  if (n >= 100_000)    return `₹${(n / 100_000).toFixed(0)} L`
  return `₹${n.toLocaleString('en-IN')}`
}

export default function LocalityTable({ data, loading }: { data: any[]; loading: boolean }) {
  return (
    <div className="rounded-xl p-5" style={{ background: 'var(--white)', border: '1px solid var(--ink-faint)' }}>
      <div className="flex items-center justify-between mb-4">
        <div className="text-xs font-medium uppercase tracking-wider" style={{ color: 'var(--ink-muted)' }}>
          Locality hotspots
        </div>
        <span className="text-xs font-mono px-2 py-0.5 rounded" style={{ background: 'var(--surface)', color: 'var(--ink-muted)' }}>
          by listing count
        </span>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-10 rounded animate-pulse" style={{ background: 'var(--surface)' }} />
          ))}
        </div>
      ) : data.length === 0 ? (
        <div className="py-12 text-center text-sm" style={{ color: 'var(--ink-muted)' }}>No locality data</div>
      ) : (
        <div className="overflow-y-auto" style={{ maxHeight: 320 }}>
          <table className="w-full">
            <thead>
              <tr style={{ borderBottom: '1px solid var(--ink-faint)' }}>
                <th className="text-left pb-2 text-xs font-medium" style={{ color: 'var(--ink-muted)' }}>Locality</th>
                <th className="text-right pb-2 text-xs font-medium" style={{ color: 'var(--ink-muted)' }}>Listings</th>
                <th className="text-right pb-2 text-xs font-medium" style={{ color: 'var(--ink-muted)' }}>Avg price</th>
                <th className="text-right pb-2 text-xs font-medium" style={{ color: 'var(--ink-muted)' }}>₹/sqft</th>
              </tr>
            </thead>
            <tbody>
              {data.map((d, i) => (
                <tr
                  key={i}
                  style={{ borderBottom: '1px solid var(--ink-faint)' }}
                  className="transition-colors hover:bg-gray-50"
                >
                  <td className="py-3">
                    <div className="text-sm font-medium" style={{ color: 'var(--ink)' }}>{d.locality}</div>
                    <div className="text-xs capitalize" style={{ color: 'var(--ink-muted)' }}>{d.city}</div>
                  </td>
                  <td className="py-3 text-right">
                    <span className="text-xs font-mono px-2 py-0.5 rounded" style={{ background: 'var(--teal-light)', color: 'var(--teal-dark)' }}>
                      {d.listings_count}
                    </span>
                  </td>
                  <td className="py-3 text-right text-sm font-medium font-mono" style={{ color: 'var(--ink)' }}>
                    {fmt(Number(d.avg_price))}
                  </td>
                  <td className="py-3 text-right text-xs font-mono" style={{ color: 'var(--ink-muted)' }}>
                    {d.avg_price_per_sqft ? `₹${Math.round(Number(d.avg_price_per_sqft)).toLocaleString('en-IN')}` : '—'}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
