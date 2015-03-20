import os, sys, re

def download_html_pages(output_path):
	os.chdir(output_path)
	skip = 0

	while skip <= 137150:
		os.system('curl -i http://www.dominiopublico.gov.br/pesquisa/ResultadoPesquisaObraForm.do?first=50\&skip=' + str(skip) + '\&ds_titulo=\&co_autor=\&no_autor=\&co_categoria=\&pagina=2\&select_action=Submit\&co_midia=2\&co_obra=\&co_idioma=1\&colunaOrdenar=null\&ordem=null | iconv -f iso8859-1 -t utf-8 > ' + str(skip))
		skip = skip + 50

# vai retornar um set com os links e o nome dos arquivos separados por tab (\t)
# por exemplo: link \t nome_do_arquivo
def get_links_list_from_html_pages(input_path):
	os.chdir(input_path)

	link_pattern = re.compile(r'^.*\/pesquisa\/DetalheObraForm\.do\?select_action=&co_obra=(\d+).*$')
	unwanted_line_pattern = re.compile(r'(?!.*\<\/a\>.*\<\/td\>)')
	links = set()

	for filename in os.listdir(input_path):
		lines = open(filename, 'r').readlines()
		maximum = len(lines)

		for i in range(0, maximum):
			line = lines[i]
			m = link_pattern.match(line)
			if m and unwanted_line_pattern.match(lines[i + 2]):
				links.add(
					'http://www.dominiopublico.gov.br/pesquisa/DetalheObraDownload.do?select_action=\&co_obra=' +
					m.group(1) + '\&co_midia=2\t' + lines[i + 2].strip()
				)

	return links

# espera uma lista (ou um set) com os links e o nome dos arquivos separados por tab (\t)
# por exemplo: link \t nome_do_arquivo
def download_pdfs(path_to_cookies, output_path, links):
	os.chdir(output_path)

	for link in links:
		aux = link.split('\t')
		url = aux[0]
		filename = "'" + aux[1] + "'"

		os.system(
			'wget --load-cookies ' +
			path_to_cookies + ' -O ' + filename +
			'.pdf -R ico,gif,png,jpg,jpeg,jsp,asp,js,css,html -l 1 -nd ' + url
		)

def convert_pdfs_to_txts(input_path, output_path):
	os.chdir(input_path)

	for filename in os.listdir(input_path):
		os.system(
			'pdf2txt.py ' + filename + ' > ' + output_path + filename.replace('.pdf', '') + '.txt'
		)

def create_compendium_of_unique_words(input_path, output_path, output_file):
	os.chdir(input_path)

	# o padrão das palavras que quero (precisa ser melhorado)
	valid_word_pattern = re.compile(r'^[a-zãõçâêôáéíóúàü]+.*$')
	unique_words = set()
	for filename in os.listdir(input_path):
		for line in open(filename, 'r').readlines():
			for word in line.rstrip().split(' '):
				if valid_word_pattern.match(word):

					# retirando caracteres indesejados, como: , . " ' ) (
					word = re.sub(r'[^a-zãõçâêôáéíóúàü\-]', '', word)
					unique_words.add(word)

	f = open(output_path + output_file, 'w')
	for word in unique_words:
		f.write(word + '\n')

option = -1

while not(0 <= option <= 4):
	print('Estes são os métodos disponíveis e seus valores:')
	print('1 - Download páginas html do dominiopublico.gov.br de livos em Português: <output_path>')
	print('2 - Download todos os PDFs a partir das páginas html: <input_path> <output_path> <path_to_cookies (absolute)>')
	print('3 - Converter todos os PDFs para TXTs: <input_path> <output_path>')
	print('4 - Criar o Compêndio a partir dos arquivos TXT: <input_path> <output_path> [output_file (default: compendio.txt)]')
	print('0 - Sair!')

	args = input('Digite o código do método desejado e os argumentos esperados: ').split(' ')
	option = int(args[0])

	if option is 0:
		sys.exit()
	elif option is 1:
		if len(args) >= 2:
			download_html_pages(args[1])
		else:
			option = -1
	elif option is 2:
		if len(args) >= 4:
			links = get_links_list_from_html_pages(args[1])
			download_pdfs(args[3], args[2], links)
		else:
			option = -1
	elif option is 3:
		if len(args) >= 3:
			convert_pdfs_to_txts(args[1], args[2])
		else:
			option = -1
	elif option is 4:
		if len(args) >= 3:
			output_file = args[3] if len(args) >= 4 else 'compendio.txt'
			create_compendium_of_unique_words(args[1], args[2], output_file)
		else:
			option = -1
