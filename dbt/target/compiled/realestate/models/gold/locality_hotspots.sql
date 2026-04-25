

select
    city,
    locality,
    count(*)                    as listings_count,
    round(avg(price))           as avg_price,
    round(avg(price_per_sqft))  as avg_price_per_sqft,
    round(min(price)::double precision) as min_price,
    round(max(price)::double precision) as max_price
from "RealEstateDB"."silver"."listings_history"
where
    is_current = true
    and locality is not null
    and price is not null
group by city, locality
having count(*) >= 2
order by city, count(*) desc