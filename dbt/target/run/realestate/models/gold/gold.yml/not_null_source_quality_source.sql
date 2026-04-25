
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select source
from "RealEstateDB"."gold"."source_quality"
where source is null



  
  
      
    ) dbt_internal_test