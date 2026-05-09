
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select listing_hash
from "neondb"."gold"."price_changes"
where listing_hash is null



  
  
      
    ) dbt_internal_test