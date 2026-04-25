

select
    source,
    city,
    effective_from                                          as scrape_date,
    count(*)                                               as total_listings,
    count(price)                                           as listings_with_price,
    round(
        count(price)::numeric / nullif(count(*), 0) * 100, 1
    )                                                      as price_coverage_pct,
    count(locality)                                        as listings_with_locality,
    count(bhk)                                             as listings_with_bhk
from "RealEstateDB"."silver"."listings_history"
where is_current = true
group by source, city, effective_from
order by scrape_date desc, source, city