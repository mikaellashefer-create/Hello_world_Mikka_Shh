select category, count(*) as product_count
from products 
group by category;
select category, count(*) as product_count
from products 
group by category 
order by product_count desc;