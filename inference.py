from optparse import OptionParser
import inderRule as Rule
class Driver:
    def __init__(self, inputFile):
        self.file = inputFile
        self.fin = None
        self.linecount = 1
        self.queryCount = None
        self.queries = None
        self.KBCount = None
        self.KB = None

    def run(self):
    	self.fin = open(self.file, 'r')
        self.fout = open('output.txt','w')
        self.__getQueryCount()
        self.__getQueries()

    def __getQueries(self):
        self.queries = []
        for i in range(self.queryCount):
            self.queries.append(self.fin.readline())

    def __getQueryCount(self):
        self.queryCount = int(self.fin.readline())
        self.linecount+=1

    def __processRule(self, rule):
        rule = rule.split('=>')
        #If rule is inference rule
        premise = ''
        if len(r) == 2:
            premise = rule[0]
            ptype = param.PREDICATE_TYPE['PREMISE']
            conclusion = rule[1]
            ctype = param.PREDICATE_TYPE['CC']

        elif len(r) == 1:
            premise = ''
            ptype = param.PREDICATE_TYPE['EMPTY']
            conclusion = rule[0]
            ctype = param.PREDICATE_TYPE['FACT']

        cobj = util.get_pred_object(conclusion, ctype)
        util.pop_premise_objList(premise, cobj)
        util.IndexObj(cobj, ctype)

if __name__=="__main__":
    parser = OptionParser()
    parser.add_option("-i", "--ip",action="store", type="string", dest="input", help="Specify input file")
    (options, args) = parser.parse_args()
    dobj = Driver(options.input)
    __builtins__.IndexRule = {
                                param.PREDICATE_TYPE['FACT']:{},
                                param.PREDICATE_TYPE['CC']:{}
                            }
    dobj.run()