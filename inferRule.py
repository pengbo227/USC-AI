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
        '''
            Valid: TRUE
            Invalid: FALSE
        '''

        theta = {}
        print 'infer called'
        theta['_status'] = param.VALID_RULE
        theta_list = FOL_BC_OR(self.pobj, theta)
        print 'theta list:',theta_list
        result = param.INVALID_RULE
        for t in theta_list:
            if t['_status']==param.VALID_RULE:
                return 'TRUE\n'
        return 'FALSE\n'

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
    ruleList = Search_Rule(pobj.name)
    returnList = []
    for rule in ruleList:
        print 'rule',rule.printPredicate()
        print 'theta',theta
        inner_theta = copy.deepcopy(theta)
        #standardize theta
        rule, inner_theta = Standardize(rule, inner_theta)
        #unify will modify inner_theta
        
        returnList.extend(FOL_BC_AND(rule.premiseObjs, Unify(rule.argsList, pobj.argsList, inner_theta)))
    print 'returnList',returnList
    return returnList

def FOL_BC_AND(goals, theta):
    '''

    '''
    print 'And called theta:',theta
    print 'And Goals', goals
    if theta['_status']==param.INVALID_RULE:
        return []
    elif len(goals)==0:
        print 'len goals 0'
        return [theta]
    first, rest = goals[0], goals[1:]
    print 'first object before substitution',first.printPredicate()
    Substitute(first, theta)
    print 'first object after substitution',first.printPredicate()
    theta_d = FOL_BC_OR(first, theta)
    print 'theta d',theta_d
    resultList = []
    for t in theta_d:
        print 't',t
        resultList.extend(FOL_BC_AND(rest, t))
    return resultList


def Substitute(pobj, theta):
    for i in range(len(pobj.argsList)):
        if pobj.argsList[i][0].islower():
            pobj.argsList[i] = theta[pobj.argsList[i]]

def Unify(rhs, goal, theta):
    print 'rhs:',rhs
    print 'goal',goal
    print 'theta', theta
    if theta['_status']==param.INVALID_RULE:
        return theta
    elif len(goal)==1:
        print 'length 1 '
        if rhs[0]==goal[0]:
            return theta
        elif rhs[0][0].islower():  #rhs[0] is variable case 1
            return Unify_Var(rhs[0], goal[0], theta)
        elif goal[0][0].islower(): #goal[0] is variable and rhs[0] is constant case 2
            return Unify_Var(goal[0], rhs[0], theta)
        else:
            theta['_status'] = param.INVALID_RULE
            return theta
    else:
        return Unify(rhs[1:], goal[1:], Unify(rhs[0], goal[0], theta))

def Unify_Var(var, prob_const, theta):
    '''
        in case 1: prob_const can be variable or constant
        in case 2: prob_const is always constant
    '''
    if (var in theta.keys()) and theta[var]:

        return Unify(theta[var], prob_const, theta)
    elif (prob_const in theta.keys()) and theta[prob_const]:
        return Unify(var, theta[prob_const], theta)
    else:
        theta[var] = prob_const
        return theta


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
        chkList = [pobj]
        for elem in pobj.premiseObjs:
            chkList.append(elem)
        for elem in chkList:
            for i in range(elem.argsCount):
                origvar = elem.argsList[i]
                var = origvar
                if origvar in theta and theta[origvar]:
                    unique = False
                    while not unique:
                        var = util.get_new_name(var)
                        unique = var not in theta
                #add var to theta
                theta[var] = None
                #update new_arglist
                replaceMap[origvar] = var

        pobj_c = util.Clone_pobj(pobj, replaceMap)
        return pobj_c, theta

def Search_Rule(name):
    ruleList = []
    ruleList.extend(util.get_kb_list(param.PREDICATE_TYPE['FACT'], name))
    ruleList.extend(util.get_kb_list(param.PREDICATE_TYPE['CC'], name))
    return ruleList
