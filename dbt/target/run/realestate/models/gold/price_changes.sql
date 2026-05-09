
  create view "neondb"."gold"."price_changes__dbt_tmp"
    
    
  as (
    

select
    h1.listing_hash,
    h1.title,
    h1.city,
    h1.source,
    h1.locality,
    h1.bhk,
    h2.price                                                        as old_price,
    h1.price                                                        as new_price,
    h1.price - h2.price                                             as delta,
    round(
        (h1.price - h2.price)::numeric
        / nullif(h2.price, 0)::numeric * 100, 2
    )                                                               as pct_change,
    h2.effective_from                                               as changed_from_date,
    h1.effective_from                                               as changed_to_date
from "neondb"."silver"."listings_history" h1
join "neondb"."silver"."listings_history" h2
    on  h1.listing_hash   = h2.listing_hash
    and h1.is_current     = true
    and h2.is_current     = false
    and h1.effective_from > h2.effective_from
order by abs(h1.price - h2.price) desc
  );