import csp2 as csp
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to the input json file")
ap.add_argument("-n", "--algorithm_number", required=True,
	help="Select Value algo to be used")
args = vars(ap.parse_args())

num = int(args["algorithm_number"])
pb = csp.csp(args["input"])
if(num==1):
	print pb.genaralisedLookAhead(pb.selectValueFC)
elif(num==2):
	print pb.genaralisedLookAhead(pb.selectValueAC)
elif(num==3):
	print pb.genaralisedLookAhead(pb.selectValueFullAC)
elif(num==4):
	print pb.genaralisedLookAhead(pb.selectValuePartialAC)
else:
	print "Incorrect number for algorithm, please check again"
