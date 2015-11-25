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
    pobj = Rule.predicateObj()
    pbj.type = ptype
    p_rule = pred_repr.strip()
    p_rule = p_rule.split('(')
    pobj.name = p_rule[0]
    args = p_rule[1].split(')')[0]
    args = args.split(',')
    args = args.split(',')
    pobj.argsCount = len(args)
    pobj.argsDict, pobj.varCount, pobj.constCount = buildArgs(args)
    
    if (ptype == param.PREDICATE_TYPE['CC']) or (ptype == param.PREDICATE_TYPE['FACT']):
        IndexObj(pobj, ptype)
    
    return pobj

def IndexObj(pobj, ptype):
    idxObj = __builtins__.IndexRule
    if not idxObj[ptype].get(pobj.name, None):
        idxObj[ptype][pobj.name] = [pobj]
    else:
        idxObj[ptype][pobj.name].append(pobj)

def pop_premise_objList(premise_repr, cobj):
    # we need to fill the list of premise in conclusion object: cobj.premiseObjs
    if cobj.type == param.PREDICATE_TYPE['CC']:
        premise = premise_repr.strip()
        p_list = premise.split('^')
        p_len = len(p_list)
        cobj.premiseCount = p_len
        p_type = param.PREDICATE_TYPE['PREMISE']
        for i in range(p_len):
            cobjs.premiseObjs.append(get_pred_object(p_list[i], p_type))

def buildArgs(args):
    base_str = 'arg_'
    vc = 0
    cc = 0
    arg_dict = {}
    for i in range(len(args)):
        arg_dict[base_str+str(i)] = args[i]
        if args[i][0].isupper():
            cc+=1
        else:
            vc+=1

    return arg_dict, vc, cc





