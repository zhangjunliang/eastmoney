cd C:\work\private\eastmoney
python run.py -o=bk -f=save_bk
python run.py -o=info -f=bk_info -limit=5 -fields=id -order=desc
cmd \k