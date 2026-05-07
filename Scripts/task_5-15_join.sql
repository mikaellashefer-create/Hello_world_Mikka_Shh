select 
p.name as "Название_товара",
pr.price as "Цена_товара"
from products p
join prices pr 
on p.id = pr.product_id