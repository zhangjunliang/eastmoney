select *,FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate 
from bk
where 1 = 1  
AND is_option = 100
and bk_type = 2
order by diff_price_rate asc;

select *,FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate 
from bk
where 1 = 1  
AND is_option = 100
and bk_type = 3
order by diff_price_rate asc;


	
update bk set is_option = 0;

update bk set is_option = 100
where 1 = 1  
	AND price >= price_5
	AND price_5 >= price_10 
	AND price_10 >= price_20 
	AND price_5 != 0 
	AND price_10 != 0 
	AND price_20 != 0 
	and weight >= 0
	and rate >= 0
	and bk_type in (2,3);
	

	
select code from stock_bk where bk_code in (select b.bk_code from bk as b where b.is_option = 100 and bk_type = 3) group by code;