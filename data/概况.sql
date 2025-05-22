-- select count(*),
-- sum(market_price),sum(flow_price),
-- sum(profit_price),sum(gross_price),
-- sum(profit_price)/sum(gross_price) as avg_grate,
-- (sum(dividend_ratio)/count(*)) as avg_drate,
-- (sum(profit_rate)/count(*)) as avg_profit_rate,
-- (sum(gross_rate)/count(*)) as avg_gross_rate
-- from stock where 
-- type = 1 and name like '%银行%';

set @today_time = '2025-05-19';

select 
name,code,price,flow_price,rate,price_5,price_10,price_20,
IF(price >= price_5 and price_5 >= price_10 and price_10 >= price_20,1,0) as up,
FORMAT((GREATEST(price,price_5,price_10,price_20) - LEAST(price,price_5,price_10,price_20)) / (price+price_5+price_10+price_20)/4*100,3) AS diff_price_rate 
from stock 
where 1 = 1 
and code in (
	select code from stock_dbk where day_time = @today_time and is_t0 = '成' and top_num != '首板'
) order by up;
	

select 
count(*),
sum(flow_price)/count(*) as flow_price,
count(*) as total,
sum(IF(flow_price < 15.1,1,0)) as price_total,
sum(IF(flow_price < 42,1,0)) as flow_total,
sum(IF(price >= price_5 and price_5 >= price_10 and price_10 >= price_20,1,0)) as up_total,
sum(IF(gross_price > 0 and profit_price > 0 and dividend_ratio > 0,1,0)) as dividend_total,
sum(IF(price >= price_5 and price_5 >= price_10 and price_10 >= price_20 and gross_price > 0 and profit_price > 0 and dividend_ratio > 0,1,0)) as up_dividend_total,
FORMAT(sum(FORMAT((GREATEST(price,price_5,price_10,price_20) - LEAST(price,price_5,price_10,price_20)) / (price+price_5+price_10+price_20)/4*100,3))/count(*),3) AS diff_price_rate,
FORMAT(sum(price)/count(*),3) as price,
FORMAT(sum(dividend_ratio)/count(*),3) as dividend_ratio,
Format(sum(Format(price/flow_price,2))/count(*),2) as p_f
from stock 
where 1=1
and market_price < 95 
and type = 1
and weight >= 0 
and market_type != 2
and code in (
	select code from stock_dbk where day_time = @today_time and is_t0 = '成' and top_num = '首板'
);

select Format(sum(Format(price/flow_price,2))/count(*),2) from  stock_dbk where day_time = @today_time and is_t0 = '成' and flow_price < 100;

select Format(sum(Format(price/flow_price,2))/count(*),2) from  stock where type = 1;
