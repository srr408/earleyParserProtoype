# import sys
import copy
import time
# sys.setrecursionlimit(1500)
# - * - Coding: UTF-8 - * - 

def predictor(sequence,dot,grammarset,ori,renew_state):
    newsequence = []
    done = 0
    minnewsequence = []
    for grammar in grammarset:
        temp = []
        for i in grammar:
            temp.append(i)
        if temp != sequence[0:3] or renew_state == 0:
            if temp == sequence[0:3]:
                renew_state = 1
            minnewsequence = []
            if grammar[0] == sequence[dot][0]:
                idx = 0
                for letter in range(len(grammar)):
                    if grammar[letter] == "T":
                        minnewsequence.append(grammar[idx:idx+2])
                        idx += 2
                    else:
                        minnewsequence.append(grammar[idx])
                        idx += 1
                    if idx == (len(grammar)):
                        break
                if ori == 0:
                    minnewsequence.append(sequence[-3] + 1)
                    minnewsequence.append(sequence[-3] + 1)
                else:
                    minnewsequence.append(sequence[-3])
                    minnewsequence.append(sequence[-3])
                # minnewsequence.append(0)
                minnewsequence.append(1)
                newsequence.append(minnewsequence)
    return newsequence,renew_state

def scanner(sequence,dot,state,curr_state):
    new_curr = copy.deepcopy(curr_state)

    seq = copy.deepcopy(sequence)

    dot += 1
    seq[-3] += 1
    seq[-1] = dot
    if dot == len(seq[0:-3]):
        if len(new_curr) > 0:
            for i in new_curr[:-1]:
                if i[i[-1]] == seq[0]:
                    i[-3] += 1
                    i[-1] += 1
                state[-1].append(i)
    state[-1].append(seq)
    return dot,state,seq

def parser(sequence,dot,curr_state,state,grammarset,flag,traversed_flag,word,renew_state):
    if traversed_flag == len(word):
        if dot == (len(sequence[0:-3])):
            for i in range(len(state[-2])):
                if state[-2][i] == sequence:
                    cur = i
            state[-2][cur-1][-1] = state[-2][cur-1][-1] + 1
        n = copy.deepcopy(state[0][0])
        n[-1] = n[-1] + 1
        state[-2].append(n)
        return state[:-1]
    if dot == (len(sequence[0:-3])): #COMPLETER RULE
        if len(state[-1]) == 0:
            return state[:-1]
        if sequence[-4][1] == word[traversed_flag]:
            traversed_flag += 1
        new_sequence = state[-1][-2]
        new_dot = state[-1][-2][-1]
        curr_state = state[-1][:-1]
        state.append([])
        renew_state = 0
        return (parser(new_sequence,new_dot,curr_state,state,grammarset,flag,traversed_flag,word,renew_state))
    elif sequence[dot][0] == "T":
        if len(curr_state) > 0 and flag == 0:
            if len(state) > 1:
                state = state[:-1] #get rid of the last empty string
            for i in curr_state[1:]:
                state[-1].append(i)
            state.append([])
        dot,state,new_seq = scanner(sequence,dot,state,curr_state)
        if dot < (len(new_seq[0:-3])):
            state.append([])
        return(parser(new_seq,dot,curr_state,state,grammarset,flag,traversed_flag,word,renew_state))
    else:
        ori = 0
        for i in curr_state: #remove the Earley items that are parsed (dot at the end)
            if i[-1] == len(i[0:-3]):
                curr_state.remove(i)  
        if (len(curr_state) == 0):
            current_state = []
            current_state.append(sequence)
        else:
            current_state = copy.deepcopy(curr_state)
            ori = 1
        new_sequence,renew_state = predictor(sequence,dot,grammarset,ori,renew_state)
        for i in new_sequence:
            current_state.append(i)
        new_sequence = current_state[-1]
        return(parser(new_sequence,1,current_state,state,grammarset,flag,traversed_flag,word,renew_state))


def main():
    print("PROFESSOR'S EXAMPLE:")
    sequence = []
    state = [[]]
    j = 0
    dot = 1
    flag = 0
    word = "aaa"
    traversed_flag = 0
    sequence.append("S'")
    sequence.append("S")
    sequence.append(0)
    sequence.append(j)
    sequence.append(dot)

    grammarset = []
    grammarset.append("SSS")
    grammarset.append("STa")
    curr_state = []
    curr_state.append(sequence)

    state[-1].append(sequence)

    renew_state = 0
    
    result = []
    result = parser(sequence,dot,curr_state,state,grammarset,flag,traversed_flag,word,renew_state)
    for i in range(len(result)):
        print("S",i,": ",end="")
        for j in range(len(result[i])):
            print("[",end="")
            for z in range(len(result[i][j]) - 2):
                dot_posi = result[i][j][-1] 
                if z == 0:
                    print(result[i][j][0],"->",end="")
                elif z > 0 and z < dot_posi:
                    print(result[i][j][z],end="")
                elif z == dot_posi:
                    print(".",end="")
                    if dot_posi != (len(result[i][j]) - 3):
                        print(result[i][j][z],end="")
                else:
                    if z != len(result[i][j]) - 3:
                        print(result[i][j][z],end="")
            print(" ,",result[i][j][-2],end="")
            print("], ",end="")
        print("\n")

    print("---------------------------------------------------------------------------------")
    print("PAPER'S EXAMPLE")
    sequence = []
    state = [[]]
    j = 0
    dot = 1
    flag = 0
    word = "n"*2
    traversed_flag = 0
    sequence.append("S'")
    sequence.append("E")
    sequence.append(0)
    sequence.append(j)
    sequence.append(dot)

    grammarset = []
    grammarset.append("EEE")
    grammarset.append("ETn")
    curr_state = []
    curr_state.append(sequence)

    state[-1].append(sequence)

    renew_state = 0
    
    result = []
    st = time.time()
    result = parser(sequence,dot,curr_state,state,grammarset,flag,traversed_flag,word,renew_state)
    et = time.time()
    for i in range(len(result)):
        print("S",i,": ",end="")
        for j in range(len(result[i])):
            print("[",end="")
            for z in range(len(result[i][j]) - 2):
                dot_posi = result[i][j][-1] 
                if z == 0:
                    print(result[i][j][0],"->",end="")
                elif z > 0 and z < dot_posi:
                    print(result[i][j][z],end="")
                elif z == dot_posi:
                    print(".",end="")
                    if dot_posi != (len(result[i][j]) - 3):
                        print(result[i][j][z],end="")
                else:
                    if z != len(result[i][j]) - 3:
                        print(result[i][j][z],end="")
            print(" ,",result[i][j][-2],end="")
            print("], ",end="")
        print("\n")
    print("Time:",(et-st)*1000,"miliseconds")

    print("---------------------------------------------------------------------------------")
    print("CHINESE EXAMPLE")
    sequence = []
    state = [[]]
    j = 0
    dot = 1
    flag = 0
    word = "我叫D"
    print("Parsing word:",word)
    traversed_flag = 0
    sequence.append("S'")
    sequence.append("S")
    sequence.append(0)
    sequence.append(j)
    sequence.append(dot)

    grammarset = []
    grammarset.append("SPVN")
    grammarset.append("PT我")
    grammarset.append("VT叫")
    grammarset.append("NTD")
    curr_state = []
    curr_state.append(sequence)

    state[-1].append(sequence)

    renew_state = 0
    
    result = []
    st = time.time()
    result = parser(sequence,dot,curr_state,state,grammarset,flag,traversed_flag,word,renew_state)
    et = time.time()
    for i in range(len(result)):
        print("S",i,": ",end="")
        for j in range(len(result[i])):
            print("[",end="")
            for z in range(len(result[i][j]) - 2):
                dot_posi = result[i][j][-1] 
                if z == 0:
                    print(result[i][j][0],"->",end="")
                elif z > 0 and z < dot_posi:
                    print(result[i][j][z],end="")
                elif z == dot_posi:
                    print(".",end="")
                    if dot_posi != (len(result[i][j]) - 3):
                        print(result[i][j][z],end="")
                else:
                    if z != len(result[i][j]) - 3:
                        print(result[i][j][z],end="")
            print(" ,",result[i][j][-2],end="")
            print("], ",end="")
        print("\n")

    print("Time:",(et-st)*1000,"miliseconds")


if __name__ == "__main__":
    main()
