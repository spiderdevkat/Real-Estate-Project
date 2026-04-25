
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select listings_count
from "RealEstateDB"."gold"."locality_hotspots"
where listings_count is null



  
  
      
    ) dbt_internal_test