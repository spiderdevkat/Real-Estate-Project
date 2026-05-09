
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select total_listings
from "neondb"."gold"."bhk_price_summary"
where total_listings is null



  
  
      
    ) dbt_internal_test