-- qushi-10 ---
select 
	name,
	code,
	price,
	rate,
	flow_price,
	FORMAT(price/flow_price,2) as p_f,
	FORMAT((GREATEST(price,price_5,price_10,price_20) - LEAST(price,price_5,price_10,price_20)) / (price+price_5+price_10+price_20)/4*100,3) AS diff_price_rate 
from stock 
where is_option = 10
and type = 1
order by diff_price_rate asc;

-- qushi-20 ---
select 
	name,
	code,
	rate,
	price,
	flow_price,
	FORMAT(price/flow_price,2) as p_f,
	FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate 
from stock 
where is_option = 20
and type = 1
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) < 0.5
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) > 0.1
order by diff_price_rate asc;

-- qushi-30 ---
select 
	name,
	code,
	rate,
	price,
	flow_price,
	FORMAT(price/flow_price,2) as p_f,
	gross_price,gross_rate,profit_price,profit_rate,dividend_ratio,
	FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate 
from stock 
where is_option = 30
and type = 1
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) < 0.5
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) > 0.1
order by diff_price_rate asc;

-- qushi-40 --
select 
	name,
	code,
	rate,
	price,
	flow_price,
	FORMAT(price/flow_price,2) as p_f,
	gross_price,gross_rate,profit_price,profit_rate,dividend_ratio,
	FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate 
from stock 
where is_option = 40
and type = 1
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) < 0.5
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) > 0.1
order by diff_price_rate asc;


-- qushi-50 --
select 
	name,
	code,
	rate,
	price,
	flow_price,
	FORMAT(price/flow_price,2) as p_f,
	gross_price,gross_rate,profit_price,profit_rate,dividend_ratio,
	FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate 
from stock 
where is_option = 50
and type = 1
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) < 0.5
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) > 0.1
order by diff_price_rate asc;

-- bezhi --
select 
	name,
	code,
	rate,
	price,
	flow_price,
	FORMAT(price/flow_price,2) as p_f,
	gross_price,gross_rate,profit_price,profit_rate,dividend_ratio,
	FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate
from stock 
where weight = 200
and type = 1
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) < 0.5
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) > 0.1
order by diff_price_rate asc;

select 
	name,
	code,
	rate,
	price,
	flow_price,
	FORMAT(price/flow_price,2) as p_f,
	gross_price,gross_rate,profit_price,profit_rate,dividend_ratio,
	FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) AS diff_price_rate
from stock 
where weight = 100
and type = 1
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) < 0.5
-- and FORMAT((GREATEST(price_5,price_10,price_20) - LEAST(price_5,price_10,price_20)) / (price_5+price_10+price_20)/3*100,3) > 0.1
order by diff_price_rate asc;
