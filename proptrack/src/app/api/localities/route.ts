import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

export async function GET(req: NextRequest) {
  const city = req.nextUrl.searchParams.get('city') || null
  const where = city && city !== 'all' ? 'WHERE city = $1' : ''
  const params = city && city !== 'all' ? [city] : []

  const q = `
    SELECT city, locality, listings_count, avg_price, avg_price_per_sqft, min_price, max_price
    FROM gold_gold.locality_hotspots
    ${where}
    ORDER BY listings_count DESC
    LIMIT 20
  `
  const { rows } = await pool.query(q, params)
  return NextResponse.json(rows)
}
