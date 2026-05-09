
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select locality
from "neondb"."gold"."locality_hotspots"
where locality is null



  
  
      
    ) dbt_internal_test