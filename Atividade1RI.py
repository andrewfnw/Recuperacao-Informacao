# -*- coding: latin-1 -*-

import re

arquivo_original = open("ptwiki-v2.trec")   # Abrindo os arquivos e criando novos arquivos necess�rios
arquivo_limpo = open("arquivo-limpo.txt", 'a')

def limpaCaracteres(linha_suja):        # Fun��o que usa express�es regulares para limpar os dados originais
    linha_suja = linha_suja.lower().strip()
    linha_suja = re.sub("&.{2,4};", " ", linha_suja)
    linha_suja = re.sub("\\{\\{!\\}\\}", " ", linha_suja)
    linha_suja = re.sub("{{.*?}}", " ", linha_suja)
    linha_suja = re.sub("<.*?>", " ", linha_suja)
    linha_suja = re.sub("ref", " ", linha_suja)
    linha_suja = re.sub("[\s,.:;=!?]", " ", linha_suja)
    linha_suja = re.sub("[\/]", " ", linha_suja)
    linha_suja = re.sub("[\[*]", " ", linha_suja)
    linha_suja = re.sub("[\]*]", " ", linha_suja)
    linha_suja = re.sub("[\|*]", " ", linha_suja)
    linha_suja = re.sub("[\{*]", " ", linha_suja)
    linha_suja = re.sub("[\}*]", " ", linha_suja)
    linha_suja = re.sub("[\'*#()_]", " ", linha_suja)
    linha_suja = re.sub("[\d+]", " ", linha_suja)
    linha_suja = re.sub("jpg", " ", linha_suja)
    return linha_suja

linha = ' '
while(linha != ''):         # Lendo cada linha do arquivo original e depois escrevendo em arquivo separado
    linha = arquivo_original.readline()
    linhaLimpa = limpaCaracteres(linha)
    arquivo_limpo.writelines(linhaLimpa + "\n")
    print linhaLimpa

arquivo_original.close()
arquivo_limpo.close()

arquivo_limpo = open("arquivo-limpo.txt")
arquivo_indice_invertido = open("arquivo-indice-invertido.txt", 'a')

dicion = dict()

def indexaPalavraDicion(palavra, dicionario, indice):   # Fun��o que indexa o indice de cada linha no dicionario
    if palavra in dicionario:
        if not (indice in dicionario[palavra]):
            dicionario[palavra].append(indice)
    else:
        dicionario[palavra] = [indice]

num_linha = 0
linha = ' '
while(linha != ''):            # L� cada linha do arquivo de entrada e depois indexa no dicionario
    linha = arquivo_limpo.readline()
    for pal in linha.split():
        print num_linha
        indexaPalavraDicion(pal, dicion, num_linha)
    num_linha += 1


for i in dicion.iterkeys():     # Itera sobre o dicionario e escreve os indices invertidos no arquivo
    arquivo_indice_invertido.writelines(str(i) + " : "+ str(dicion.get(i)) + "\n")

arquivo_limpo.close()
arquivo_indice_invertido.close()


def interseccao(dicionario, palavra1, palavra2):    # Fun��o de intersec��o entre duas palavras
    resposta = []
    for i in dicionario[palavra1]:
        for j in dicionario[palavra2]:
            if i == j:
                resposta.append(i)
    return resposta

def uniao(dicionario, palavra1, palavra2):      # Fun��o de uniao entre duas palavras
    resposta = set( dicionario[palavra1] + dicionario[palavra2])
    return resposta
