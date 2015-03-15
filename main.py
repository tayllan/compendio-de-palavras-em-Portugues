import os, re, sys

if len(sys.argv) is not 3:
	print('Utilização: python3 main.py <input_path> <output_file>')
else:
	INPUT_PATH = sys.argv[1]
	OUTPUT_FILE = sys.argv[2]

	# o padrão das palavras que quero (precisa ser melhorado)
	GOOD_PATTERN = re.compile(r'^[a-zãõçâêôáéíóúàü]+.*$')
	unique_words = set()

	for filename in os.listdir(INPUT_PATH):
		for line in open(INPUT_PATH + filename, 'r').readlines():
			for word in line.rstrip().split(' '):
				if GOOD_PATTERN.match(word):

					# retirando caracteres indesejados, como: , . " ' ) (
					word = re.sub(r'[^a-zãõçâêôáéíóúàü\-]', '', word)
					unique_words.add(word)
					
	f = open(OUTPUT_FILE, 'w')
	f.write('Total de palavras únicas no Compêndio: ' + str(len(unique_words)) + '\n')

	for word in unique_words:
		f.write(word + '\n')

