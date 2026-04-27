import { NextRequest, NextResponse } from 'next/server'
import pool from '@/lib/db'

export async function GET(req: NextRequest) {
  const city = req.nextUrl.searchParams.get('city') || null
  const where = city && city !== 'all' ? 'WHERE city = $1' : ''
  const params = city && city !== 'all' ? [city] : []

  const q = `
    SELECT
      listing_hash, title, city, source, locality, bhk,
      old_price, new_price, delta, pct_change,
      changed_from_date, changed_to_date
    FROM gold_gold.price_changes
    ${where}
    ORDER BY abs(delta) DESC
    LIMIT 15
  `
  const { rows } = await pool.query(q, params)
  return NextResponse.json(rows)
}
