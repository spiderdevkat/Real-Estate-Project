import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

export async function GET(req: NextRequest) {
  const city = req.nextUrl.searchParams.get('city') || null
  const where = city && city !== 'all' ? 'WHERE city = $1' : ''
  const params = city && city !== 'all' ? [city] : []

  const q = `
    SELECT
      source,
      sum(total_listings)::int        AS total_listings,
      round(avg(price_coverage_pct),1) AS price_coverage_pct
    FROM gold_gold.source_quality
    ${where}
    GROUP BY source
    ORDER BY total_listings DESC
  `
  const { rows } = await pool.query(q, params)
  return NextResponse.json(rows)
}
