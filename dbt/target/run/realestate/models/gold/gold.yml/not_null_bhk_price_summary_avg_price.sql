
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select avg_price
from "RealEstateDB"."gold"."bhk_price_summary"
where avg_price is null



  
  
      
    ) dbt_internal_test