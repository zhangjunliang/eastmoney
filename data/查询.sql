-- update stock set bk_snatch_time = '2025-05-16 22:11:28' where bk_snatch_time is null and type =1;

set @snatch_time_diff = DATE_SUB(NOW(), INTERVAL 12 HOUR);

select sum(if(snatch_time < @snatch_time_diff,1,0)) as num,sum(if(bk_snatch_time < @snatch_time_diff,1,0)) as bk_num from stock_v2.stock where type = 1;
