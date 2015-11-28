import string
import inferParam as param
import inferRule as Rule

def isFact(rule):
    if rule.type == param.RULE_TYPE['FACT']:
        return True
    return False

def length(goalList):
    return len(goalList)

def get_pred_object(pred_repr, ptype):
    #print 'pred_repr', pred_repr
    pobj = Rule.Predicate()
    pobj.type = ptype
    p_rule = pred_repr.strip()
    p_rule = p_rule.split('(')
    #print 'p_rule',p_rule
    pobj.name = p_rule[0]
    args = p_rule[1].split(')')[0]
    pobj.argsList = args.split(',')
    pobj.argsCount = len(pobj.argsList)
    
    if (ptype == param.PREDICATE_TYPE['CC']) or (ptype == param.PREDICATE_TYPE['FACT']):
        IndexObj(pobj, ptype)
    
    return pobj

def IndexObj(pobj, ptype):
    idxObj = __builtins__['KB']
    if not idxObj[ptype].get(pobj.name, None):
        idxObj[ptype][pobj.name] = [pobj]
    else:
        idxObj[ptype][pobj.name].append(pobj)

def get_kb_list(ptype, name):
    flist = __builtins__['KB'][ptype]
    if flist.get(name, None):
        return flist[name]
    return []

def pop_premise_objList(premise_repr, cobj):
    # we need to fill the list of premise in conclusion object: cobj.premiseObjs
    if cobj.type == param.PREDICATE_TYPE['CC'] and premise_repr:
        premise = premise_repr.strip()
        p_list = premise.split('^')
        p_len = len(p_list)
        cobj.premiseCount = p_len
        p_type = param.PREDICATE_TYPE['PREMISE']
        for i in range(p_len):
            cobj.premiseObjs.append(get_pred_object(p_list[i], p_type))

# def buildArgs(args):
#     base_str = param.ARGS_BASE_STR
#     vc = 0
#     cc = 0
#     arg_dict = {}
#     for i in range(len(args)):
#         arg_dict[base_str+str(i)] = args[i]
#         if args[i][0].isupper():
#             cc+=1
#         else:
#             vc+=1

#     return arg_dict, vc, cc

def get_new_name(name):
    i=1
    return name+str(i)

def Clone_pobj(pobj, replaceMap):
    newObj = Rule.Predicate()
    newObj.name = pobj.name
    newObj.type = pobj.type
    newObj.argsList = replaceArgs(pobj.argsList, replaceMap)
    newObj.argsCount = pobj.argsCount
    self.result = False
    for obj in pobjs.premiseObjs:
        newObj.premiseObjs.append(Clone_pobj(obj, replaceMap))
    return newObj

def ReplaceArgs(argsList, replaceMap):
    n_argsList = copy.deepcopy(argsList)
    for i in range(len(n_argsList)):
        if n_argsList[i] in replaceMap:
            n_argsList[i] = replaceMap[n_argsList[i]]

    return n_argsList


