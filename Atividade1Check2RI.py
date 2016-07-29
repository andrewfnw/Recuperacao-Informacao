# -*- coding: latin-1 -*-
import math
from warnings import catch_warnings

arquivo_limpo = open("arquivo-limpo.txt")
arquivo_indice_invertido = open("arquivo-indice-invertido.txt", 'w')

dicionIndiceInvertido = dict()

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
    for palavra in linha_atual.split():
        indexaPalavraDicion(palavra, dicionIndiceInvertido, num_documento)
arquivo_limpo.close()

arquivo_indice_invertido.write( "Palavra | Numero Indices | Indices documentos " + "\n" )
for i in dicionIndiceInvertido.iterkeys():     # Itera sobre o dicionario e escreve os indices invertidos no arquivo
    arquivo_indice_invertido.writelines(str(i) + " : " + str(len(dicionIndiceInvertido.get(i))) + " : " + str(dicionIndiceInvertido.get(i)) + "\n")

def calcula_idf(total_documentos, frequencia_total_documentos):
    indice_idf = math.log10(total_documentos + 1/frequencia_total_documentos)
    return indice_idf

def conta_palavras_documento(pal, num_doc):
    arquivo_limpo = open("arquivo-limpo.txt")
    cont_palavra = 0
    num_documento = 0
    linha_atual = ' '  # ultima linha lida
    while (linha_atual != ''):  # Lê cada linha do arquivo de entrada e depois indexa no dicionario
        linha_atual = arquivo_limpo.readline()
        if linha_atual.split().__contains__('<docno>'):
            num_documento += 1
        if num_documento == num_doc:
            for palavra in linha_atual.split():
                if str(palavra) == str(pal):
                    cont_palavra += 1
    arquivo_limpo.close()
    return cont_palavra

def pesquisa(query, dicionario_indice_invertido, total_documentos):
    palavras_chave = query.split()
    lista_resposta = []
    k = 1.2
    for palavra_chave in palavras_chave:
        if dicionario_indice_invertido.has_key(palavra_chave):
            for doc in dicionario_indice_invertido.get(palavra_chave):
                resposta = (((k+1)*conta_palavras_documento(palavra_chave, doc))/(conta_palavras_documento(palavra_chave, doc) + k)) * calcula_idf(total_documentos, len(dicionario_indice_invertido.get(palavra_chave)))
                if (doc in [d[0] for d in lista_resposta]):
                    try:
                        resposta_anterior = lista_resposta.pop(lista_resposta.index((doc, resposta)))
                    except ValueError:
                        pass
                    else:
                        lista_resposta.append((doc, resposta + resposta_anterior[1]))
                else:
                    lista_resposta.append((doc, resposta))
    lista_ordenada = sorted(lista_resposta,key=lambda resposta: resposta[1], reverse=True)
    return lista_ordenada

print "Resultado da consulta primeira guerra mundial: " + str(pesquisa("primeira guerra mundial", dicionIndiceInvertido, num_documento))

print "Resultado da consulta espaço e tempo: " pesquisa("espaço e tempo", dicionIndiceInvertido, num_documento)

print "Resultado da consulta minha terra tem palmeiras onde canta o sabiá: " pesquisa("minha terra tem palmeiras onde canta o sabiá", dicionIndiceInvertido, num_documento)

print "Resultado da consulta grupo raça negra: " pesquisa("grupo raça negra", dicionIndiceInvertido, num_documento)

arquivo_indice_invertido.close()