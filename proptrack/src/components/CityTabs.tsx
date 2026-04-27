'use client'
import { City } from '@/app/page'

const CITIES: { id: City; label: string }[] = [
  { id: 'gurugram',  label: 'Gurugram'  },
  { id: 'delhi',     label: 'Delhi'     },
  { id: 'bangalore', label: 'Bangalore' },
  { id: 'all',       label: 'All'       },
]

export default function CityTabs({ city, onChange }: { city: City; onChange: (c: City) => void }) {
  return (
    <div className="flex gap-1 p-1 rounded-lg" style={{ background: 'var(--surface)' }}>
      {CITIES.map(c => (
        <button
          key={c.id}
          onClick={() => onChange(c.id)}
          className="px-4 py-1.5 rounded-md text-sm font-medium transition-all"
          style={{
            background: city === c.id ? 'var(--white)' : 'transparent',
            color: city === c.id ? 'var(--ink)' : 'var(--ink-muted)',
            boxShadow: city === c.id ? '0 1px 3px rgba(0,0,0,0.08)' : 'none',
            border: 'none',
            cursor: 'pointer',
          }}
        >
          {c.label}
        </button>
      ))}
    </div>
  )
}
