class poke:
    def __init__(self,pokeseries,movelist):
        self.poke=pokeseries
        self.name,self.fstyp,self.sctyp,self.hp,\
        self.a,self.d,self.spa,self.spd,self.speed=\
        self.poke.iloc[0][0],self.poke.iloc[0][1],self.poke.iloc[0][2],self.poke.iloc[0][4],\
        self.poke.iloc[0][5],self.poke.iloc[0][6],self.poke.iloc[0][7],self.poke.iloc[0][8],self.poke.iloc[0][9]
    
        self.move1=dfmoves.loc[movelist[0]].copy()
        self.move2=dfmoves.loc[movelist[1]].copy()
        self.move3=dfmoves.loc[movelist[2]].copy()
        self.move4=dfmoves.loc[movelist[3]].copy()
        self.movelist=[self.move1,self.move2,self.move3,self.move4]
        
        self.accuracy_stage=0
        self.evasion_stage=0
        
        self.critical_stage=0
        
        
    
    def __lt__(self, other):
        return self.speed < other.speed

    
stat_stage_multiplier=[2/2,3/2,4/2,5/2,6/2,7/2,8/2,2/8,2/7,2/6,2/5,2/4,2/3] 
ae_stage_multiplier=[3/3,4/3,5/3,6/3,7/3,8/3,9/3,3/9,3/8,3/7,3/6,3/5,3/4]
crit_stage_multiplier=[1/24,1/8,1/2,1,1,1,1,1]


#select character
### each action by user will be tracked using turn variable. 
### When turn==0 and 2, user will be prompted to select two characters 
### on turn==2, program will simulate battle btw two characters and give result
turn=0
def inlist(x):
    '''
    Input poke# or poke name. 
    Print which poke selected. 
    Return poke name. 
    Turn+=1
    '''
    global turn
    try:
        print(f'{dfpoke["Name"][int(x)]} selected')
        turn+=1
        return dfpoke['Name'][int(x)]
    except:
        if x in list(dfpoke['Name']):
            print(f'{x} selected')
            turn+=1
            return x
        else:
            print('invalid value, input index or name')

# damage calculation
# def damage(level=50,power=1,attack=1,defense=1,targets=1,PB=1,weather=1,critical=1,STAB=1,type_=1,burn=1,other=1,ZMove=1):
#     '''
#     damage eq for 5th gen onwards. explanation for each parameter on 
#     https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_V_onward
#     '''
#     if power==-1:
#         return 0
#     else:
#         rand=random.randrange(85,101)/100
#         return round(((level * 2 / 5 + 2) * power * attack / defense / 50 +2) \
#                      * targets * PB * weather * critical * rand * STAB * type_ * burn * other * ZMove)

def damage(power=1,attack=1,defense=1,targets=1,PB=1,weather=1,critical=1,STAB=1,type_=1,burn=1,other=1,ZMove=1):
    '''simple damage function for testing'''
    return power*0.1

def typestab(usedmove,attacker,defender):
    '''
    prints the effective dialogue
    returns type multiplier
    '''
    type_=dftypechart.loc[usedmove.Type][defender.fstyp]*dftypechart.loc[usedmove.Type][defender.sctyp]
    if attacker.fstyp==usedmove.Type or attacker.sctyp==usedmove.Type:
        stab=1.5
    else:
        stab=1
    if type_>=2:
        print("it's super effective!")
    elif type_<=.5:
        print("it's not very effective..")
    return type_,stab

def critmult(attacker):
    if random.randrange(1,101)<=crit_stage_multiplier[attacker.critical_stage]:
        print('Critical Hit!')
        return 1.5
    else:
        return 1

def battle(poke1,poke2):
    '''
    compare speed, use random skill, hp lower, repeat till hp<0
    returns winner name str
    '''
    
    attacker=sorted([poke1,poke2])[1] #comparing speed to choose who attack first
    defender=sorted([poke1,poke2])[0]
    if poke1.speed==poke2.speed: #random poke goes first if speed same
        attacker,defender=random.sample([poke1,poke2],2)
    while True:
        for i,j in [(attacker,defender),(defender,attacker)]:
            if any([x.PP for x in i.movelist])==False: ####.any() and .all() is usefull! #PP check
                usedmove=dfmoves.loc[165] #struggle
            else:
                usedmove=random.choice(i.movelist)
                while usedmove.PP==0: #look for move with PP
                    usedmove=random.choice(i.movelist)
                usedmove.PP-=1 #reduce PP after use confirmed
            print(f"{i.name} used {usedmove.Name}!")
            acc_eva=ae_stage_multiplier[i.accuracy_stage]/ae_stage_multiplier[j.evasion_stage] #limiting hit chance stage diff to 6.
            if acc_eva<3/9:
                acc_eva=3/9
            hitdice=random.randrange(1,101) #apparently 'missed' and 'evaded' dialogs coexist in pokemon
            missdice=random.randrange(1,101) 
            if hitdice<=usedmove.Accuracy and missdice<=acc_eva*100 or usedmove.Accuracy==-1:
                type_,stab=typestab(usedmove=usedmove,attacker=i,defender=j) #type, STAB for damage calculation
                critical=critmult(i) #critical for damage calculation
                if damage(attack=i.a,defense=j.d,power=usedmove.Power,type_=type_,STAB=stab,critical=critical)!=0:
                    j.hp-=damage(attack=i.a,defense=j.d,power=usedmove.Power) #damage opponent
                    print(f"{i.name} attacks {j.name} {j.name}'s HP is lowered to {j.hp}") #this print needs the if damage!=0 condition.
            elif hitdice>usedmove.Accuracy: #passing both probability is same as multiplying percentage.
                print(f"{i.name}'s attack missed!")
            elif missdice>acc_eva*100: 
                print(f"{j.name} evaded the attack!")
            if j.hp<=0:
                print(f'{j.name} fainted!')
                return i.name
                    

while turn==0:
    choice1=inlist(input('choose 1st:').lower()) #each poke name
while turn==1:
    choice2=inlist(input('choose 2nd:').lower()) #
while turn==2:
    pokeseries1=dfpoke[dfpoke['Name']==choice1] #each poke info series
    pokeseries2=dfpoke[dfpoke['Name']==choice2] #
    #poke1 and poke2 learnable move series
    series_learnablemoves1=dflearn[dflearn['pokemon_id']==pokeseries1.index[0]]['move_id']
    series_learnablemoves2=dflearn[dflearn['pokemon_id']==pokeseries2.index[0]]['move_id']
    #movelist1,2 = select random move from learnable moves
    movelist1=[series_learnablemoves1.iloc[random.randrange(len(series_learnablemoves1))] for i in range(4)]
    movelist2=[series_learnablemoves2.iloc[random.randrange(len(series_learnablemoves2))] for i in range(4)]
    
    #first number=player number, second number=poke number
    poke11=poke(pokeseries1,movelist1)
    poke21=poke(pokeseries2,movelist2)
    
    print(f'{battle(poke11,poke21)} wins!')
    break

