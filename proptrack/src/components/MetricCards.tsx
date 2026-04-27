'use client'

function fmt(n: number) {
  if (!n) return '—'
  if (n >= 10_000_000) return `₹${(n / 10_000_000).toFixed(1)} Cr`
  if (n >= 100_000)    return `₹${(n / 100_000).toFixed(0)} L`
  return `₹${n.toLocaleString('en-IN')}`
}

function Skeleton() {
  return <div className="h-8 w-24 rounded animate-pulse" style={{ background: 'var(--ink-faint)' }} />
}

export default function MetricCards({ data, loading }: { data: any; loading: boolean }) {
  const cards = [
    {
      label: 'Avg listing price',
      value: loading ? null : fmt(data?.avg_price),
      sub: 'across all BHK types',
      accent: 'var(--teal)',
    },
    {
      label: 'Avg price / sqft',
      value: loading ? null : (data?.avg_ppsf ? `₹${Math.round(data.avg_ppsf).toLocaleString('en-IN')}` : '—'),
      sub: 'per square foot',
      accent: 'var(--teal)',
    },
    {
      label: 'Active listings',
      value: loading ? null : (data?.total_listings ?? 0).toLocaleString('en-IN'),
      sub: 'scraped today',
      accent: 'var(--ink)',
    },
    {
      label: 'Price changes',
      value: loading ? null : (data?.price_changes ?? 0).toString(),
      sub: 'tracked via SCD2',
      accent: 'var(--coral)',
    },
  ]

  return (
    <div className="grid grid-cols-4 gap-4">
      {cards.map((c, i) => (
        <div key={i} className="rounded-xl p-5" style={{ background: 'var(--white)', border: '1px solid var(--ink-faint)' }}>
          <div className="text-xs font-medium uppercase tracking-wider mb-3" style={{ color: 'var(--ink-muted)' }}>
            {c.label}
          </div>
          {loading ? <Skeleton /> : (
            <div className="text-3xl font-display font-medium" style={{ color: 'var(--ink)', letterSpacing: '-0.02em' }}>
              {c.value}
            </div>
          )}
          <div className="text-xs mt-2" style={{ color: 'var(--ink-muted)' }}>{c.sub}</div>
          <div className="mt-3 h-0.5 rounded-full w-8" style={{ background: c.accent }} />
        </div>
      ))}
    </div>
  )
}
