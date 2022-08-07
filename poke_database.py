import pandas as pd

# dfpoke has poke stat
dfpoke=pd.read_csv('./Pokemon.csv')
dfpoke['Name']=dfpoke['Name'].str.lower()
dfpoke['Type 1']=dfpoke['Type 1'].str.lower()
dfpoke['Type 2']=dfpoke['Type 2'].str.lower()
dfpoke.set_index('#',inplace=True) #poke number == index
dfpoke=dfpoke[dfpoke['Name'].str.contains('mega')==False] #megapoke deleted

# dfpoke[dfpoke.index.duplicated(False)==True] #repeated index for some poke should be fixed. will cause error in future

# dfmoves has move stat
dfmoves=pd.read_csv('./pokemon_moves.csv')
dfmoves=dfmoves.astype('str') #*표시 지우기위해 일단 str으로
dfmoves['Name']=dfmoves['Name'].str.strip('*').str.lower()
dfmoves['Type']=dfmoves['Type'].str.strip('*').str.lower()
dfmoves['PP']=dfmoves['PP'].str.strip('*')
dfmoves['Category']=dfmoves['Category'].str.strip('*').str.lower()
dfmoves['Accuracy']=dfmoves['Accuracy'].str.strip('*').str.strip('%')
dfmoves['Power']=dfmoves['Power'].str.strip('*')
dfmoves['Gen']=dfmoves['Gen'].str.strip('*')
#changed all '?' in power and accuracy columns to -1. 
#-1 power will cause damage to be 0, -1 accuracy will cause attack to not miss.
dfmoves.replace('?','-1',inplace=True)
dfmoves=dfmoves.astype({'#':'int64','Type':'category','Category':'category','PP':'int64','Power':'int64','Accuracy':'int64','Gen':'category'})
dfmoves.set_index('#',inplace=True)

# dflearn has learnable move for all poke
dflearn=pd.read_csv('./pokemon_wholearns.csv')
dflearn.drop(['order'],axis=1,inplace=True) #don't know what this column is..
dflearn=dflearn.astype({'version_group_id':'category','pokemon_move_method_id':'category'})

# dftypechart is the famous poke type effective/weakness chart
dftypechart=pd.read_csv('./pokemon_typechart.csv')
dftypechart.set_index(dftypechart.columns,inplace=True)
