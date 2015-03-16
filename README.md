# Compêndio de Palavras em Português
Com este projeto eu pretendo criar o maior compêndio de palavras do idioma Português possível.

## Por quê ?
Me parece que um compêndio free de palavras em Português é algo que as pessoas poderiam utilizar, então por que não né ?!

O maior compêndio free que encontrei por enquanto é o [br.ispell](http://www.ime.usp.br/~ueda/br.ispell/) da USP, com mais de 260.000 palavras (se você souber de um maior, por favor me avise!).

E além disso, também quero fazer algumas análises estatísticas com as palavras conforme vou juntando elas. Coisas como:

* a frequência com que cada letra do alfabeto Português aparece nas palavras;
* o tamanho médio das palavras:
* a maior palavra;
* etc...

E notei que esse tipo de informação estatística do Português é difícil de ser encontrada na internet ([trabalhos relacionados estão listados aqui](#trabalhos-relacionados)).

## Como ?
Eu quero baixar TODOS os mais de 137 mil livros disponíveis no portal [Domínio Público](http://www.dominiopublico.gov.br/) e utilizar eles para criar o compêndio.

Minha ideia inicial é baixar os livros em PDF, convertê-los para texto puro (sem nenhuma forma de tratamento por enquanto) e filtrar as palavras desejadas de dentro dos arquivos de texto utilizando Python.

## O que já foi feito!
Utilizei o comando `wget` para baixar os livros do [Domínio Público](www.dominiopublico.gov.br). O comando completo foi:
`wget -R gif,png,jpg,jpeg,jsp,asp,js,css,html -r -l 4 -nd http://www.dominiopublico.gov.br/pesquisa/PesquisaObraForm.do`.

Dessa forma consegui baixar pouco mais de 1.000 livros, somando 1,8 GB, em PDF. Por causa da forma como utilizei o comando `wget` acima, além dos arquivos PDF foram baixados vários outros arquivos irrelevantes (como mp3, wmv e outros), os quais precisei deletar manualmente (isso precisa ser melhorado). Depois disso fiquei apenas com os mil e poucos arquivos PDF no diretório.

No próximo passo, utilizei o [pdfminer](https://github.com/euske/pdfminer/) para converter todos os arquivos de PDF para texto puro e depois executei o arquivo [`main.py`](https://github.com/tayllan/compendio-de-palavras-em-Portugues/blob/master/main.py) para pegar todas as palavras únicas, as quais podem ser visualizadas [aqui](https://github.com/tayllan/compendio-de-palavras-em-Portugues/blob/master/compendio.txt)

## Considerações Finais
O portal [Domínio Público](www.dominiopublico.gov.br) possui centenas de milhares de livros gratuítos em Português (também em outros idiomas, mas isso não é relevante para este projeto) disponíveis para download. Entre estes livros estão também documentos governamentais, TCCs e teses de mestrado e doutorado, entre diversos outros tipos de documentos e livros.

Um ponto importante a ser levado em consideração é que, por enquanto, estou convertendo os livros de PDF para puro texto sem nenhuma forma de tratamento, o que significa que palavras em outros idiomas e outros tipos de poluição acabam sendo utilizados na geração do compêndio final.

## Trabalhos Relacionados
*[Frequência de ocorrência de letras no Português](http://www.numaboa.com.br/criptografia/criptoanalise/310-frequencia-portugues?showall=&limitstart=) - Uma análisa bacana, mas com muito poucas palavras e sem levar em consideração letras acentuadas (á, ê, etc...).
*[Análise de Frequências da Língua Portuguesa](www.mat.uc.pt/~pedro/lectivso/CodigosCriptografia1011/interTIC07pqap.pdf) - Um bom artigo com uma análise mais profunda e com maiores motivações, mas ainda assim com poucas palavras.
*[Análise de Frequências de Línguas](http://www.lockabit.coppe.ufrj.br/sites/lockabit.coppe.ufrj.br/files/publicacoes/lockabit/analise_freq.pdf) - Um artigo similar ao anterior, e também com poucas palavras.
*[Dicionário br.ispell](http://www.ime.usp.br/~ueda/br.ispell/) - Compêndio com mais de 260 mil palavras em Português brasileiro.

## Licença
[![Creative Commons License](http://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)

Este trabalho está sob [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
