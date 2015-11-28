import inferParam as param
import inferUtil as util
import copy

class Predicate:
    def __init__(self):
        self.name = ''
        self.type = None
        self.argsList = None
        self.argsCount = None
        self.premiseObjs = []
        self.premiseCount = 0
        self.result = False

    def printPredicate(self):
        i = 1
        pre_str = ''
        for pobj in self.premiseObjs:
            pre_str = pre_str + pobj.printPredicate()
        if self.type == param.PREDICATE_TYPE['CC']:
            pre_str += '=>' 
        pre_str+= self.name+'(' + str(self.argsList) + ')'
        return pre_str
      
class Query:
    def __init__(self, rule):
        self.pobj = util.get_pred_object(rule, param.PREDICATE_TYPE['QUERY'])

    def infer(self):
        theta = {}
        theta['_status'] = True
        theta_list = FOL_BC_OR(self.pobj, theta)
        result = 'FALSE'
        for t in theta_list:
            if t['_status']:
                return 'TRUE'
        return 'FALSE'




def FOL_BC_OR(pobj, theta):
    '''
        Input:
        0. pobj: It will be just a single predicate object
        1. Theta will be just single theta and not list of thetas

        Output:
        will be the list of theta returned by the appending from
        the result of getting from inner and call
    '''
    #1 Get the rule list
    ruleList = Search_rule(pobj.name)
    returnList = []
    for rule in ruleList:
        inner_theta = copy.deepcopy(theta)
        #standardize theta
        rule, inner_theta = Standardize(rule, inner_theta)
        #unify will modify inner_theta
        Unify(rule, pobj, inner_theta)
        return_list.extend(FOL_BC_AND( None, None, inner_theta))
        
    return returnList


def Standardize(pobj, theta):
    '''
        1 checck if there are is any conflict by comparing theta and pobject variables
        2 if conflict then 
            #create copy of of pobj with modified argument list
            #add newly introduced variables to inner theta which should be passed to parent calling function
            #parent should not modify pobj from __builtins__
        else:
            just add all the variables of pobj to inner_theta.
    '''

    if pobj.type==param.PREDICATE_TYPE['FACT']:
        return pobj, theta
    else:
        replaceMap = {}
        for i in range(pobj.argsCount):
            origvar = pobj.argsList[i]
            if origvar in theta:
                unique = False
                var = origvar
                while not unique:
                    var = util.get_new_name(var)
                    unique = var not in theta
            #add var to theta
            theta[var] = None
            #update new_arglist
            replaceMap[origvar] = var

        #if there is a conflict then create a new pobj
        pobj_c = pobj   
        if replaceMap:
            pobj_c = util.Clone_pobj(pobj, replaceMap)
        return pobj_c, theta


def FOL_BC_AND( a,b , theta):
    if theta is None:
        return None

    #if length of premise is 0 then return true


def Search_Rule(name):
    ruleList = []
    ruleList.extend(util.get_kb_list(param.PREDICATE_TYPE['FACT'], name))
    ruleList.extend(util.get_kb_list(param.PREDICATE_TYPE['CC'], name))
    return ruleList

def Standardize(argList, argCnt, theta):
    #cloning the argList as it will be referenced for fruther queries
    args = copy.deepcopy(argList)

    #will check if there exists identical variables in argList.
    #if duplicate variables found in argList then rename that variable
    base_repr = param.ARGS_BASE_STR
    for i in range(argCnt):
        arg = base_repr+str(i)
        if args[arg] in theta:
            unique = False
            while not unique:
                new_name = util.get_new_name(args[arg])
                unique = new_name in theta
            theta[new_name] = None
        else:
            theta[args[arg]] = None
    return theta

def Unify(rhs, goal, theta):
    if theta is None:
        return None
    elif len(goal)==1:
        if rhs[0]==goal[0]:
            return theta
        elif rhs[0][0].islower():  #rhs[0] is variable case 1
            return Unify_Var(rhs[0], goal[0], theta)
        elif goal[0][0].islower(): #goal[0] is variable and rhs[0] is constant case 2
            return Unify_Var(goal[0], rhs[0], theta)
        else:
            return None
    else:
        return Unify(rhs[1:], goal[1:], Unify(rhs[0], goal[0], theta))

def Unify_Var(var, prob_const, theta):
    '''
        in case 1: prob_const can be variable or constant
        in case 2: prob_const is always constant
    '''
    if var in theta.keys():
        return Unify(theta[var], prob_const, theta)
    elif prob_const in theta.keys():
        return Unify(var, theta[prob_const], theta)
    else:
        theta[var] = prob_const
        return theta
