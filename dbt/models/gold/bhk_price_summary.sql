{{ config(materialized='view') }}

select
    city,
    bhk,
    count(*)                    as total_listings,
    round(avg(price))           as avg_price,
    round(min(price)::double precision) as min_price,
    round(max(price)::double precision) as max_price,
    round(avg(price_per_sqft))  as avg_price_per_sqft
from {{ source('silver', 'listings_history') }}
where
    is_current = true
    and bhk is not null
    and price is not null
group by city, bhk
order by city, bhk