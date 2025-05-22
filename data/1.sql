update stock set is_option = 0 where type = 1;

SET @diff_price_rate = 0.88;
SET @bz_diff_price_rate = 0.88;
SET @max_price = 10;
SET @max_flow_price = 46;
SET @top_flow_price = 150;
SET @min_profit_price = -1;
SET @price_market = 0.49;
set @today_time = '2025-05-21';
set @min_rate = 0.2;


-- select @max_price;

# 趋势-10 
update stock set is_option = 10
where 1 = 1  
	AND price >= price_5
	AND price_5 >= price_10 
	AND price_10 >= price_20 
	AND price_5 != 0 
	AND price_10 != 0 
	AND price_20 != 0 
	AND FORMAT((GREATEST(price_5, price_10, price_20 ) - LEAST( price_5, price_10, price_20 )) / (price_5 + price_10 + price_20 ) / 3 * 100,3) < @diff_price_rate
	AND flow_price < @max_flow_price
	AND price <  @max_price
	AND weight >= 0 
	AND type = 1
	-- and market_type != 2
	and gross_price > 0 
	and profit_price > 0
  and dividend_ratio > 0
	# 不算银行
	and code not in (select code from stock_bk where bk_code = 'BK0475')
	# bk
	and code in (select code from stock_bk where bk_code in (select b.bk_code from bk as b where b.is_option = 100))
	and rate >= @min_rate;
	
update stock set is_option = 20
where 1 = 1  
	AND price >= price_5
	AND price_5 >= price_10 
	AND price_10 >= price_20 
	AND price_5 != 0 
	AND price_10 != 0 
	AND price_20 != 0 
	-- AND FORMAT((GREATEST( price, price_5, price_10, price_20 ) - LEAST( price, price_5, price_10, price_20 )) / ( price + price_5 + price_10 + price_20 ) / 4 * 100,3) < @diff_price_rate
	AND FORMAT((GREATEST(price_5, price_10, price_20 ) - LEAST( price_5, price_10, price_20 )) / (price_5 + price_10 + price_20 ) / 3 * 100,3) < @diff_price_rate
		AND flow_price < @max_flow_price
	AND price <  @max_price
	AND weight >= 0 
	AND type = 1
	-- and market_type != 2
	and is_option not in (10)
	# 不算银行
	and code not in (select code from stock_bk where bk_code = 'BK0475')
	# bk
	and code in (select code from stock_bk where bk_code in (select b.bk_code from bk as b where b.is_option = 100))
	and rate >= @min_rate;
	
# 趋势-30 
	update stock set is_option = 30
	where 1 = 1  
	AND price >= price_5
	AND price_5 >= price_10 
	AND price_10 >= price_20 
	AND price_5 != 0 
	AND price_10 != 0 
	AND price_20 != 0 
	AND weight >= 0 
	AND type = 1
	-- and market_type != 2
	and is_option not in (10,20)
	# 不算银行
	and code not in (select code from stock_bk where bk_code = 'BK0475')
	# bk
	and code in (select code from stock_bk where bk_code in (select b.bk_code from bk as b where b.is_option = 100))
	and rate >= @min_rate;

# 涨停 < 46
update stock set is_option = 40
where 1 = 1 
--   and flow_price < @max_flow_price 
-- 	AND price < @max_price
-- 	AND weight >= 0 
-- 	AND type = 1
-- 	-- and market_type != 2
-- 	and profit_price > @min_profit_price
	AND price >= price_5
	AND price_5 >= price_10 
	AND price_10 >= price_20 
	AND price_5 != 0 
	AND price_10 != 0 
	AND price_20 != 0
	# bk
	and code in (select code from stock_bk where bk_code in (select b.bk_code from bk as b where b.is_option = 100))
	and code in (
		select code from stock_dbk where day_time = @today_time and is_t0 = '成' 
	);

# 涨停 > 46
update stock set is_option = 50
where is_option not in (40)
and code in (
	select code from stock_dbk where day_time = @today_time and is_t0 = '成' 
);


# 本质 
update stock set weight = 0 where weight >= 0 and type = 1;

update stock set weight = 100
where type = 1 
and dividend_ratio > 2.5
and profit_rate > 1 and gross_rate > 1
and rate >= 0
and gross_price > 0 and profit_price > 0
AND price >= price_5
AND price_5 >= price_10 
AND price_10 >= price_20 
AND price_5 != 0 
AND price_10 != 0 
AND price_20 != 0 
AND type = 1
-- and market_type != 2
and weight >= 0
# 不算银行
and code not in (select code from stock_bk where bk_code = 'BK0475')
-- AND FORMAT((GREATEST( price, price_5, price_10, price_20 ) - LEAST( price, price_5, price_10, price_20 )) / ( price + price_5 + price_10 + price_20 ) / 4 * 100,3) < @bz_diff_price_rate
# bk
and code in (select code from stock_bk where bk_code in (select b.bk_code from bk as b where b.is_option = 100))
AND FORMAT((GREATEST(price_5, price_10, price_20 ) - LEAST( price_5, price_10, price_20 )) / (price_5 + price_10 + price_20 ) / 3 * 100,3) < @bz_diff_price_rate;

# 本质 银行
update stock set weight = 200
where type = 1 
and rate >= 0
AND price >= price_5
AND price_5 >= price_10 
AND price_10 >= price_20 
AND price_5 != 0 
AND price_10 != 0 
AND price_20 != 0 
AND type = 1
-- and market_type != 2
and weight >= 0
# bk
and code in (select code from stock_bk where bk_code in (select b.bk_code from bk as b where b.is_option = 100))	
# 银行
and code in (select code from stock_bk where bk_code = 'BK0475');

