import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

export async function GET(req: NextRequest) {
  const city = req.nextUrl.searchParams.get('city') || null
  const where = city && city !== 'all' ? 'WHERE city = $1' : ''
  const params = city && city !== 'all' ? [city] : []

  const q = `
    SELECT
      bhk,
      round(avg(avg_price))           AS avg_price,
      round(avg(min_price))           AS min_price,
      round(avg(max_price))           AS max_price,
      round(avg(avg_price_per_sqft))  AS avg_ppsf,
      sum(total_listings)::int        AS total_listings
    FROM gold_gold.bhk_price_summary
    ${where}
    GROUP BY bhk
    ORDER BY bhk
  `
  const { rows } = await pool.query(q, params)
  return NextResponse.json(rows)
}
