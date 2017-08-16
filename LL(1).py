# 1. --- Removing Left Recursion ------

def remove_left_recur(nonTerminals):
    nT = list(nonTerminals.keys())
    nT.sort()
    #print(nT)
    newTer = dict()
    for i in range(len(nT)):
        rule = nonTerminals[nT[i]]
        #print(nT[i],rule,sep = '--> ')
        newRule = []
        for j in range(len(rule)):
            flag  = False
            if((rule[j][0] is not nT[i]) and (nonTerminals.__contains__(rule[j][0]))):
                toCheck = nonTerminals[rule[j][0]]
                for k in range(len(toCheck)):
                    if(toCheck[k][0] == nT[i]):
                        flag = True
                        break
                if(flag):
                    for k in range(len(toCheck)):
                        if(toCheck[k] is '@'):
                            newRule.append(rule[j][1:])
                            continue
                        newRule.append(toCheck[k] + rule[j][1:])
            if(not flag):
                newRule.append(rule[j])
            #print(newRule)

        # --- To Remove Direct Left Recursion ----

        flag = False
        for j in range(len(newRule)):
            if(newRule[j][0] == nT[i]):
                flag = True
                break
        if(flag):
            ch = 'A'
            while(ch<='Z'):
                if(not nonTerminals.__contains__(ch)):
                    break
                ch = chr(ord(ch)+1)
            newT1 = []
            newT1.append('@')
            newT = []
            for j in newRule:
                if(j[0] == nT[i]):
                    newT1.append(j[1:] + ch)
                else:
                    if(j[0] is '@' ):
                        newT.append(ch)
                    else:
                        newT.append(j + ch)
            nonTerminals[nT[i]] = newT

            newTer[ch] = newT1

        # --- Method completes -----

    #print(newTer)
    for i,j in newTer.items():
        nonTerminals[i] = j

    nonTerminals = newTer


# ----------  ENDS (left _ Recur ) ----------------------





# 2. -------------- First and Follow --------------------
First = dict()
Follow = dict()

 # (i) ------ First ---------
def first4pro(str):
    fir = []
    flag = False
    for i in str:
        if('@' not in First[i]):
            fir += First[i]
            flag = True
            break
        else:
            fir+=First[i]
            fir.remove('@')
    if(not flag):
        fir+=['@']

    return fir

def first(nT,nonT,checked):
    if(checked[nT]):
        return
    else:
        for i in nonT[nT]:
            #print("production" ,i)
            last = True
            for j in i:
                if(checked[j]):
                    if('@' not in First[j]):
                        First[nT] += First[j]
                        last = False
                        break
                    else:
                        First[nT] += First[j]
                        First[nT].remove('@')
                else:
                    first(j,nonT,checked)
                    if('@' not in First[j]):
                        First[nT] += First[j]
                        last = False
                        break
                    else:
                        First[nT] += First[j]
                        First[nT].remove('@')
            if(last):
                First[nT].append('@')
        checked[nT] = True
                    
        
              

def createFirst(ter , nonT ):
    checked = dict()
    # --- initialising the checked
    for i in ter:
        checked[i] = True
        First[i] = [i]
    for i in list(nonT.keys()):
        checked[i] = False
        First[i] = []

    #---- first --------
    for i in list(nonT.keys()):
        if(not checked[i]):
            first(i,nonT,checked)
            First[i] = list(set(First[i]))

    #(ii) ------- Follow------------

def follow(nT,nonT,checked):
    if(checked[nT]):
        return
    else:
        for i in nonT.keys():
            pro = list(nonT[i])
            for j in pro:
               # print(i," -- > ",pro , " to check ",nT , " from : ", j)
                if(nT in j):
                    ind = j.index(nT) + 1
                    while(ind<len(j)):
                        if('@' not in First[j[ind]]):
                            Follow[nT] += First[j[ind]]
                            break
                        else:
                            Follow[nT] += First[j[ind]]
                        ind+=1
                    if(ind == len(j)):
                        if(i == nT):
                            continue
                        follow(i,nonT,checked)
                        Follow[nT] += Follow[i]
        checked[nT] = True
            
    
    
def createFollow(ter , nonT ,S):
    checked = dict()
    # --- Initialising the checked ---
    for i in list(nonT.keys()):
        checked[i] = False
        Follow[i] = []
    Follow[S] = ['$']

    #calling the follow

    for i in list(nonT.keys()):
        if(not checked[i]):
            follow(i,nonT,checked)
            if(len(Follow[i]) == 0):
                checked[i] = False
    for i in list(nonT.keys()):
        Follow[i] = list(set(Follow[i]))
        if('@' in Follow[i]):
            Follow[i].remove('@')
    
    '''for i in list(nonT.keys()):
        if( not checked[i]):
            follow(i,nonT,checked)
            Follow[i] = list(set(Follow[i]))
            if(len(Follow[i]) == 0):
                checked[i] = False
       ''' 
    

# ----------------- ENDS(F and F) ------------------------





# 3. --------------------- Parse Table --------------------
parseTable = list()
terMap = dict()
nonTMap = dict()
def createParseTable(ter , nonT , First , Follow):
    for i in nonT.keys():
        for j in nonT[i]:
            fir = first4pro(j)
            #print(fir)
            #print(i,"-->",j)
            for k in fir:
                #print(k)
                if(k is not '@'):
                    parseTable[nonTMap[i]][terMap[k]] = str(i)+str(j)
                else:
                   # print(Follow[i])
                    for tr in Follow[i]:
                        #print(tr)
                        parseTable[nonTMap[i]][terMap[tr]] = str(i) + str('@')

                
                    
    

    

# ----------------------------ENDS(Parse Table) -----------






# 4. ------------------------Traversal ---------------

# (i) ----- Stack -----------------
class Stack:
    def __init__(self):
        self.__storage = []

    def isEmpty(self):
        return len(self.__storage) == 0

    def push(self,p):
        self.__storage.append(p)

    def pop(self):
        return self.__storage.pop()
    def top(self):
        return self.__storage[len(self.__storage) - 1]
    def __str__(self):
        """
        Because of using list as parent class for stack, our last element will
        be first for stack, according to FIFO principle. So, if we will use
        parent's implementation of str(), we will get reversed order of
        elements.
        """
        #: You can reverse elements and use supper `__str__` method, or 
        #: implement it's behavior by yourself.
        #: I choose to add 'stack' in the begging in order to differ list and
        #: stack instances.
        return 'stack [{}]'.format(', '.join([ str(i) for i in reversed(self.__storage) ]))
    
#----------------------ENDS(Traversal) --------------------







#---------------- Driver Program ------------------------
terminals = []
nonTerminals = dict()
terminals = input("Enter Terminals (,) : ").split(",")
n = int(input("No. of Non - Terminals  : "))

for i in range(n):
    ch = input("NonTerminals : ").strip()
    rules = input("Productions (,) : ").split(",")
    nonTerminals[ch] = rules

# --- Old Rules-------

S = input("Start Symbol :  ")
terminals+=['$']
print("Productions : ")
for i in nonTerminals.keys():
    print(i,"-->",end=' ')
    for j in nonTerminals[i]:
        print(j,end= ' | ')
    print()

# --- Calling Remove_LeftRecur ----

remove_left_recur(nonTerminals)

# ---- After left Recursions -------
print("\nAfter Left Recurions Productions : ")

for i in nonTerminals.keys():
    print(i,"-->",end = ' ' )
    for j in nonTerminals[i]:
        print(j,end = ' | ')
    print()

# --- First and Follow ----


createFirst(terminals,nonTerminals)


createFollow(terminals,nonTerminals,S)

print("{}\t\t\t\t{}\t\t\t\t{}".format('Grammar Rule','First','Follow'))
for i in nonTerminals.keys():
    print("{}\t\t\t\t{}\t\t\t\t{}".format(i,First[i],Follow[i]))



#-------- Parse Table ----------------



        #---- Intialisation of parseTable--------


for count,i in enumerate(terminals):
    terMap[i] = count+1
for count,i in enumerate(nonTerminals.keys()):
    nonTMap[i] = count+1

parseTable = [ [ 0 for i in range(len(terminals)+1) ] for j in range(len(nonTerminals.keys())+1)]
print(terMap,"\n",nonTMap)

        # -----Intailisation Done -------------




createParseTable(terminals,nonTerminals,First,Follow)
print(end = '\t\t ')
for i in terminals:
    print(i,end = '\t\t  ')
print()
'''for i in list(nonTerminals.keys()):
    #print(i,end = '\t\t')
    for j in terminals:
        print(i,j,nonTMap[i],terMap[j])
        #print(parseTable[nonTMap[i]][terMap[j]],end = '\t\t')
    #print()   
print(parseTable)'''
for i in list(nonTerminals.keys()):
    print(i,end = '\t\t')
    for j in terminals:
        #print(i,j,nonTMap[i],terMap[j])
        print(parseTable[nonTMap[i]][terMap[j]],end = '\t\t')
    print()


#--------------- Parse Table Done ---------------




#------------ Traversals :-----------------------

string = input("String to Parse :  ")

st = Stack()

st.push('$')
st.push(S)  # Start Symbol

i = 0
while(i<len(string)):
    print(st," Exp : ",string[i])
    if( string[i] not in terminals):
        break
    elif(not st.isEmpty() and st.top() is '@'):
        st.pop()
    elif(not st.isEmpty() and st.top() is string[i]):
        st.pop()
        i+=1
    elif(not st.isEmpty() and st.top() in nonTerminals.keys()):
        if(parseTable[nonTMap[st.top()]][terMap[string[i]]] == 0):
            break
        else:
            c = st.pop()
            for j in str(str(parseTable[nonTMap[c]][terMap[string[i]]])[1:])[::-1]:
                st.push(j)
if(st.isEmpty()):
    print("Successfully Parsed")
else:
    print("Unsuccessful Attempt")
    
                
        
    
