all:
	echo '' | cat > Results.out 
	echo '' | cat > DVS_logs.out 
	echo '' | cat > DVS_Priority_logs.out 
	echo '' | cat > DVS_DPM_logs.out 

	python3.10 main.py --file set_test_copy.sch
	python3.10 main.py --file set_test2_copy.sch
	python3.10 main.py --file set_test3_copy.sch
	python3.10 main.py --file set_test4_copy.sch
	python3.10 main.py --file set_test5_copy.sch
	python3.10 main.py --file set_test6_copy.sch


Parametrize:
	echo '' | cat > Results_param.out 
	echo '' | cat > DVS_logs.out 
	echo '' | cat > DVS_Priority_logs.out 
	echo '' | cat > DVS_DPM_logs.out 

	python3.10 main.py Parametrize

DPM_time:
	echo '' | cat > Results_param.out 
	echo '' | cat > DVS_logs.out 
	echo '' | cat > DVS_Priority_logs.out 
	echo '' | cat > DVS_DPM_logs.out 

	python3.10 main.py DPM_time
