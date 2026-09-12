log_file = "/root/cyberlab/logs/boot.log"
with open(log_file, "r") as file:
#open the file stored in log_file in read mode, other modes are "w" and "a" - append
#with let's us to close the file without explicitly using 'close()'
#as file: file is another variable. so file -s basically the opened log file
	error_count=0
	count=0
	for line in file:
		print(line, end="")
		count +=1
		if "ERROR" in line:
			error_count +=1
	print(f"\n total lines: {count}")
	print(f"\n total error: {error_count}")

