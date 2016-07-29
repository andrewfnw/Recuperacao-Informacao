# -*- coding: latin-1 -*-

import re

arquivo_original = open("ptwiki-v2.trec")   # Abrindo os arquivos e criando novos arquivos necessários
arquivo_limpo = open("arquivo-limpo.txt", 'a')

def limpaCaracteres(linha_suja):        # Função que usa expressões regulares para limpar os dados originais
    linha_suja = linha_suja.lower().strip()
    linha_suja = re.sub("&.{2,4};", " ", linha_suja)
    linha_suja = re.sub("\\{\\{!\\}\\}", " ", linha_suja)
    linha_suja = re.sub("{{.*?}}", " ", linha_suja)
    linha_suja = re.sub("<docno>", " <docno> ", linha_suja)
    linha_suja = re.sub("ref", " ", linha_suja)
    linha_suja = re.sub("[\s,.:;=!?]", " ", linha_suja)
    linha_suja = re.sub("[\/]", " ", linha_suja)
    linha_suja = re.sub("[\[*]", " ", linha_suja)
    linha_suja = re.sub("[\]*]", " ", linha_suja)
    linha_suja = re.sub("[\|*]", " ", linha_suja)
    linha_suja = re.sub("[\{*]", " ", linha_suja)
    linha_suja = re.sub("[\}*]", " ", linha_suja)
    linha_suja = re.sub("[\'*#()_]", " ", linha_suja)
    linha_suja = re.sub("jpg", " ", linha_suja)
    return linha_suja

linha_atual = ' '
while(linha_atual != ''):         # Lendo cada linha do arquivo original e depois escrevendo em arquivo separado
    linha_atual = arquivo_original.readline()
    linhaLimpa = limpaCaracteres(linha_atual)
    arquivo_limpo.writelines(linhaLimpa + "\n")
    print linhaLimpa

arquivo_original.close()
arquivo_limpo.close()

arquivo_limpo = open("arquivo-limpo.txt")
arquivo_indice_invertido = open("arquivo-indice-invertido.txt", 'a')

dicion = dict()

def indexaPalavraDicion(palavra, dicionario, indice):   # Função que indexa o indice de cada linha no dicionario
    if palavra in dicionario:
        if not (indice in dicionario[palavra]):
            dicionario[palavra].append(indice)
    else:
        dicionario[palavra] = [indice]

num_documento = 0
linha_atual = ' '                 # ultima linha lida
while(linha_atual != ''):            # Lê cada linha do arquivo de entrada e depois indexa no dicionario
    linha_atual = arquivo_limpo.readline()
    if linha_atual.split().__contains__('<docno>'):
        num_documento += 1
        print num_documento
    for pal in linha_atual.split():
        indexaPalavraDicion(pal, dicion, num_documento)




for i in dicion.iterkeys():     # Itera sobre o dicionario e escreve os indices invertidos no arquivo
    arquivo_indice_invertido.writelines(str(i) + " : "+ str(dicion.get(i)) + "\n")

arquivo_limpo.close()
arquivo_indice_invertido.close()


def interseccao(dicionario, palavra1, palavra2):    # Função de intersecção entre duas palavras
    resposta = []
    for i in dicionario[palavra1]:
        for j in dicionario[palavra2]:
            if i == j:
                resposta.append(i)
    return resposta

def uniao(dicionario, palavra1, palavra2):      # Função de uniao entre duas palavras
    resposta = set( dicionario[palavra1] + dicionario[palavra2])
    return resposta
