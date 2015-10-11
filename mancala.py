class Driver:
	def __init__(self, inputFile):
		print 'inputfile', inputFile


if __name__=="__main__":
	parser = OptionParser()
    parser.add_option("-i", "--ip",action="store", type="string", dest="input", help="Specify input file")
	(options, args) = parser.parse_args()
    dobj = Driver(options.input)
    dobj.run()