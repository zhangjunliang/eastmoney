cd C:\work\work_py\eastmoney
python run.py -o=bk -f=save_bk
python run.py -o=stock -f=save_stock
python run.py -o=stock -f=save_daily_top
python run.py -o=stock -f=save_daily_hot
python run.py -o=rank -f=save_lhb
python run.py -o=rank -f=save_lhb_list
python run.py -o=stock -f=save_stock_bk
python run.py -o=info -f=bk_info -limit=5 -fields=id -order=desc
cmd \k