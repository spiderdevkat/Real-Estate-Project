
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select bhk
from "RealEstateDB"."gold"."bhk_price_summary"
where bhk is null



  
  
      
    ) dbt_internal_test