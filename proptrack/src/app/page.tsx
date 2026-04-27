'use client'

import { useState, useEffect, useCallback } from 'react'
import MetricCards from '@/components/MetricCards'
import BhkChart from '@/components/BhkChart'
import SourceDonut from '@/components/SourceDonut'
import LocalityTable from '@/components/LocalityTable'
import PriceChangeFeed from '@/components/PriceChangeFeed'
import CityTabs from '@/components/CityTabs'

export type City = 'all' | 'gurugram' | 'delhi' | 'bangalore'

export default function Dashboard() {
  const [city, setCity] = useState<City>('gurugram')
  const [metrics, setMetrics]       = useState<any>(null)
  const [bhk, setBhk]               = useState<any[]>([])
  const [localities, setLocalities] = useState<any[]>([])
  const [changes, setChanges]       = useState<any[]>([])
  const [sources, setSources]       = useState<any[]>([])
  const [loading, setLoading]       = useState(true)

  const fetchAll = useCallback(async (c: City) => {
    setLoading(true)
    const qs = `city=${c}`
    const [m, b, l, ch, s] = await Promise.all([
      fetch(`/api/metrics?${qs}`).then(r => r.json()),
      fetch(`/api/bhk?${qs}`).then(r => r.json()),
      fetch(`/api/localities?${qs}`).then(r => r.json()),
      fetch(`/api/price-changes?${qs}`).then(r => r.json()),
      fetch(`/api/source-quality?${qs}`).then(r => r.json()),
    ])
    setMetrics(m); setBhk(b); setLocalities(l); setChanges(ch); setSources(s)
    setLoading(false)
  }, [])

  useEffect(() => { fetchAll(city) }, [city, fetchAll])

  const handleCity = (c: City) => { setCity(c) }

  return (
    <div className="min-h-screen" style={{ background: 'var(--surface)' }}>
      {/* Header */}
      <header style={{ background: 'var(--white)', borderBottom: '1px solid var(--ink-faint)' }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div style={{ width: 32, height: 32, background: 'var(--ink)', borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M8 1L1 7h2v7h4v-4h2v4h4V7h2L8 1z" fill="#1D9E75"/>
              </svg>
            </div>
            <div>
              <span className="font-display font-semibold text-lg" style={{ color: 'var(--ink)', letterSpacing: '-0.02em' }}>PropTrack</span>
              <span className="ml-1 text-sm" style={{ color: 'var(--ink-muted)' }}>India</span>
            </div>
          </div>

          <CityTabs city={city} onChange={handleCity} />

          <div className="flex items-center gap-2">
            <div className="pulse-dot w-2 h-2 rounded-full" style={{ background: 'var(--teal)' }} />
            <span className="text-xs font-mono" style={{ color: 'var(--ink-muted)' }}>
              {loading ? 'Fetching…' : 'Live data'}
            </span>
          </div>
        </div>
      </header>

      {/* City label */}
      <div className="max-w-7xl mx-auto px-6 pt-8 pb-2">
        <div className="flex items-baseline gap-4">
          <h1 className="font-display text-4xl font-medium fade-up" style={{ color: 'var(--ink)', letterSpacing: '-0.03em' }}>
            {city === 'all' ? 'All Cities' : city.charAt(0).toUpperCase() + city.slice(1)}
          </h1>
          <span className="text-sm fade-up delay-1" style={{ color: 'var(--ink-muted)' }}>
            Real estate intelligence · updated daily at 2 AM IST
          </span>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-6 pb-16 space-y-6 pt-4">
        {/* Metric cards */}
        <div className="fade-up delay-1">
          <MetricCards data={metrics} loading={loading} />
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-3 gap-5 fade-up delay-2">
          <div className="col-span-2">
            <BhkChart data={bhk} loading={loading} />
          </div>
          <div>
            <SourceDonut data={sources} loading={loading} />
          </div>
        </div>

        {/* Bottom row */}
        <div className="grid grid-cols-2 gap-5 fade-up delay-3">
          <LocalityTable data={localities} loading={loading} />
          <PriceChangeFeed data={changes} loading={loading} />
        </div>
      </main>
    </div>
  )
}
