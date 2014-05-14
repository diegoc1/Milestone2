import os

for i in range(0, 4):
	n = 3
	if i == 1:
		n = 7
	elif i == 2:
		n = 15
	elif i == 3:
		n = 31

	for j in range(0, 5):

		#3,7,15,31
		for j in range(0, 10):
			command = "python sendrecv.py -f testfiles/random_short.txt -c " + str(1000) +  " -s 256 -q 200 -C " + str(n) + " -b -z " + str(0.1 + j * 0.025)
			os.system(command)
