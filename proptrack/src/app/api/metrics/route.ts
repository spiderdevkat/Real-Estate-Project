import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

export async function GET(req: NextRequest) {
  const city = req.nextUrl.searchParams.get('city') || null

  const whereCity = city && city !== 'all' ? `WHERE city = $1` : ''
  const params = city && city !== 'all' ? [city] : []

  const q = `
    SELECT
      round(avg(avg_price))          AS avg_price,
      round(avg(avg_price_per_sqft)) AS avg_ppsf,
      sum(total_listings)::int       AS total_listings,
      max(listing_date)              AS last_updated
    FROM gold_gold.city_price_summary
    ${whereCity}
  `
  const changes = `
    SELECT count(*)::int AS price_changes
    FROM gold_gold.price_changes
    ${city && city !== 'all' ? 'WHERE city = $1' : ''}
  `

  const [r1, r2] = await Promise.all([
    pool.query(q, params),
    pool.query(changes, params),
  ])

  return NextResponse.json({
    avg_price:      r1.rows[0]?.avg_price      ?? 0,
    avg_ppsf:       r1.rows[0]?.avg_ppsf       ?? 0,
    total_listings: r1.rows[0]?.total_listings  ?? 0,
    last_updated:   r1.rows[0]?.last_updated    ?? null,
    price_changes:  r2.rows[0]?.price_changes   ?? 0,
  })
}
