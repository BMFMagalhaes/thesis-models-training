import pandas as pd
pd.set_option('display.max_rows', 300)
data = pd.read_csv("./datasets/oficial.csv", header=0, index_col=False)
print(data.columns)
print(data["IDVolunt"].unique)
#print(data.isnull().any())
#print(data.isna().any())
#print(data.dtypes)
#print(data.head())
print(data.shape)
data.columns = data.columns.str.strip() # Leading and trailing

#Diana Rito
#Remoção da entrada número 1 e substituição pelo IDVolunt 16
data = data.drop(data[(data["IDVolunt"] == 1)].index)
data.loc[data['IDVolunt'] == 16, 'IDVolunt'] = 1
#Remoção de erros no IDPergu 0 - Trial 2 removido
data = data.drop(data[(data["IDVolunt"] == 1) & (data["IDPergu"] == 0) & (data["IDTrial"] == 2)].index)
#Remoção de erros no IDPergu 8 - Trial 0 removido - Trial 2 nunca chegou a existir
data = data.drop(data[(data["IDVolunt"] == 1) & (data["IDPergu"] == 8) & (data["IDTrial"] == 0)].index)
#Remoção de erros no IDPergu 12 - Trial 1
data = data.drop(data[(data["IDVolunt"] == 1) & (data["IDPergu"] == 12) & (data["IDTrial"] == 1)].index)


#João Martins
#Remoção da entrada número 2 e substituição do ID 10
data = data.drop(data.index[(data["IDVolunt"] == 2)], axis=0)
data.loc[data['IDVolunt'] == 10, 'IDVolunt'] = 2


#Luís Martins
#Remoção do IDPergu 3 porque os gestos estão errados
data = data.drop(data[(data["IDVolunt"] == 5) & (data["IDPergu"] == 3)].index)
#Substituição do IDPergu 4 para 3 porque fez um gesto certo na pergunta errada
data.loc[(data['IDVolunt'] == 5) & (data['IDPergu'] == 4), 'IDPergu'] = 3
#Remoção do IDPergu 11 porque os gestos estão errados
data = data.drop(data[(data["IDVolunt"] == 5) & (data["IDPergu"] == 11)].index)
#Alteração do IDPergu 1 para IDPergu 4 da repetição do gesto no IDVolun 17
data.loc[(data['IDVolunt'] == 17) & (data['IDPergu'] == 1), 'IDPergu'] = 4
#Alteração do IDPergu 2 para IDPergu 11 da repetição do gesto no IDVolun 17
data.loc[(data['IDVolunt'] == 17) & (data['IDPergu'] == 2), 'IDPergu'] = 11
#Acrescento dos gestos repetidos guardados no IDVolunt 17 para o IDVolunt 5
data.loc[(data['IDVolunt'] == 17), 'IDVolunt'] = 5

#Roberto Barbosa
#Remoção dos erros na pergunta 0 - Trial 5 removido
data = data.drop(data[(data["IDVolunt"] == 6) & (data["IDPergu"] == 0) & (data["IDTrial"] == 5)].index)
#Remoção dos erros na pergunta 7 - Trial 0 removido - Trial 2 nunca chegou a existir
data = data.drop(data[(data["IDVolunt"] == 6) & (data["IDPergu"] == 7) & (data["IDTrial"] == 0)].index)


#José Pereira - Não há Trial 1 para o IDPergunta 1 o que está ok
#Remoção do Trial 5 para o IDPergu 1
data = data.drop(data[(data["IDVolunt"] == 7) & (data["IDPergu"] == 1) & (data["IDTrial"] == 5)].index)
#Remoção do gesto errado no IDPergunta 11 para os trials 3,4,5
data = data.drop(data[(data["IDVolunt"] == 7) & (data["IDPergu"] == 11) & (data["IDTrial"] == 3)].index)
data = data.drop(data[(data["IDVolunt"] == 7) & (data["IDPergu"] == 11) & (data["IDTrial"] == 4)].index)
data = data.drop(data[(data["IDVolunt"] == 7) & (data["IDPergu"] == 11) & (data["IDTrial"] == 5)].index)
#Adição do gesto correto no IDPergunta 11 para os trials 3,4,5
data.loc[(data['IDVolunt'] == 0) & (data['IDPergu'] == 4) & (data['IDTrial'] == 0), 'IDTrial'] = 3
data.loc[(data['IDVolunt'] == 0) & (data['IDPergu'] == 4) & (data['IDTrial'] == 1), 'IDTrial'] = 4
data.loc[(data['IDVolunt'] == 0) & (data['IDPergu'] == 4) & (data['IDTrial'] == 2), 'IDTrial'] = 5
data.loc[(data['IDVolunt'] == 0) & (data['IDPergu'] == 4), 'IDPergu'] = 11
data.loc[(data['IDVolunt'] == 0), 'IDVolunt'] = 7

#João Lopes
# Remoção do Trial 4 para o IDPergunta 7
data = data.drop(data[(data["IDVolunt"] == 8) & (data["IDPergu"] == 7) & (data["IDTrial"] == 4)].index)


#Sara Cerqueira
# Remoção do Trial 0 para o IDPergunta 8 - não chegou a guardar nada


#João Martins - ID 10 convertido para 2 anteriormente
# Remoção do Trial 2 para o IDPergunta 8 - não chegou a guardar nada


#Luís Moreira
#Remoção do Trial 6 e 7 do IDPergu 10
data = data.drop(data[(data["IDVolunt"] == 12) & (data["IDPergu"] == 10) & (data["IDTrial"] == 6)].index)
data = data.drop(data[(data["IDVolunt"] == 12) & (data["IDPergu"] == 10) & (data["IDTrial"] == 7)].index)
#print(data.shape)


#Simão Carvalho
#Remoção do Trial 3 do IDPergu 0 - Nunca existiu
#Remoção do Trial 4 do IDPergu 0 - Nunca existiu
data = data.drop(data[(data["IDVolunt"] == 13) & (data["IDPergu"] == 0) & (data["IDTrial"] == 4)].index)
#Remoção do Trial 3 do IDPergu 8 - Nunca existiu
#Remoção do Trial 3 do IDPergu 10 - Nunca existiu
#Remoção do Trial 3 do IDPergu 11
data = data.drop(data[(data["IDVolunt"] == 13) & (data["IDPergu"] == 11) & (data["IDTrial"] == 3)].index)
#Remoção do Trial 8 do IDPergu 0 porque há um a mais
data = data.drop(data[(data["IDVolunt"] == 13) & (data["IDPergu"] == 0) & (data["IDTrial"] == 8)].index)


#Joana Figueiredo
#Remoção do Trial 1 do IDPergu 4
data = data.drop(data[(data["IDVolunt"] == 14) & (data["IDPergu"] == 4) & (data["IDTrial"] == 1)].index)


#Rita Oliveira
#Remoção do Trial 2 do IDPergu 8
data = data.drop(data[(data["IDVolunt"] == 18) & (data["IDPergu"] == 8) & (data["IDTrial"] == 2)].index)
#Remoção do Trial 3 do IDPergu 8 - Nunca existiu


#André Veloso
#Remoção do Trial 0 do IDPergu 0
data = data.drop(data[(data["IDVolunt"] == 22) & (data["IDPergu"] == 0) & (data["IDTrial"] == 0)].index)
#Remoção do Trial 4 do IDPergu 0 - Nunca existiu


#Nuno Ribeiro
#Remoção do Trial 4 do IDPergu 0 - Nunca existiu
#Remoção do Trial 0 do IDPergu 1 - Janela apanhava muito nas imagens
data = data.drop(data[(data["IDVolunt"] == 23) & (data["IDPergu"] == 1) & (data["IDTrial"] == 0)].index)
#Remoção do Trial 3 do IDPergu 3
data = data.drop(data[(data["IDVolunt"] == 23) & (data["IDPergu"] == 3) & (data["IDTrial"] == 3)].index)


#João André
#Remoção do Trial 5 do IDPergu 11 - Trocou de gestos a meio do gesto
data = data.drop(data[(data["IDVolunt"] == 24) & (data["IDPergu"] == 11) & (data["IDTrial"] == 5)].index)

# ID 25 - Clique muito mau
data = data.drop(data[(data["IDVolunt"] == 25) & (data["IDPergu"] == 0) & (data["IDTrial"] == 4)].index)
data = data.drop(data[(data["IDVolunt"] == 25) & (data["IDPergu"] == 5) & (data["IDTrial"] == 1)].index)
#data.to_csv("oficial-limpo.csv", index=False)
print(data.loc[(data['IDVolunt'] == 0) & (data['IDPergu'] == 4) & (data['IDTrial'] == 2)])

#Substituir o ID das Perguntas 7,8,9,10,11,12 para 0,1,2,3,4,5 respetivamente para haver apenas 6 classes de classificação
data.loc[(data['IDPergu'] == 7), 'IDPergu'] = 0
data.loc[(data['IDPergu'] == 8), 'IDPergu'] = 1
data.loc[(data['IDPergu'] == 9), 'IDPergu'] = 2
data.loc[(data['IDPergu'] == 10), 'IDPergu'] = 3
data.loc[(data['IDPergu'] == 11), 'IDPergu'] = 4
data.loc[(data['IDPergu'] == 12), 'IDPergu'] = 5
print(data.shape)
data.to_csv("oficial-limpo.csv", index=False)