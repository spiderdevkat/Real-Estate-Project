

select
    city,
    source,
    effective_from              as listing_date,
    count(*)                    as total_listings,
    round(avg(price))           as avg_price,
    round(min(price)::double precision) as min_price,
    round(max(price)::double precision) as max_price,
    round(avg(price_per_sqft))  as avg_price_per_sqft
from "neondb"."silver"."listings_history"
where
    is_current = true
    and price is not null
group by city, source, effective_from
order by city, effective_from desc