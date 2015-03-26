import os, sys, re, time
from pprint import pprint

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
    links = set()

    for filename in os.listdir(input_path):
        lines = open(filename, 'r').readlines()
        maximum = len(lines)

        for i in range(0, maximum):
            line = lines[i]
            m = link_pattern.match(line)
            if m:
                links.add('http://www.dominiopublico.gov.br/pesquisa/DetalheObraDownload.do?select_action=&co_obra=' + m.group(1) + '&co_midia=2')

    return links

# baixa os pdfs a partir dos links html utilizando o selenium para emular navegação dentro do dominiopublico.org.br (e por isso é necessário o email e a senha)
def download_pdfs(output_path, links, email, password):
    from selenium import webdriver

    profile = webdriver.firefox.firefox_profile.FirefoxProfile()
    profile.set_preference('pdfjs.disabled', True)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/pdf')
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', output_path)
    driver = webdriver.Firefox(firefox_profile = profile)

    for link in links:
        try:
            driver.get(link)

            email = driver.find_element_by_name('ds_email')
            password = driver.find_element_by_name('ds_senha')
            url = driver.find_element_by_name('ds_url')
            destination = url.get_attribute('value')

            email.send_keys(email)
            password.send_keys(password)

            driver.find_element_by_css_selector('tbody tbody a').click()
            driver.get('http://www.dominiopublico.gov.br/' + destination)
        except:
            pass

def convert_pdfs_to_txts(input_path, output_path):
    os.chdir(input_path)

    for filename in os.listdir(input_path):
        os.system('pdf2txt.py ' + filename + ' > ' + output_path + filename.replace('.pdf', '') + '.txt')

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

print('------------------------------------------------------------------------------------------------------\n')
print('Utilização: python3 main.py <código_opção> [<parâmetro1> ...]\n')
print('Estes são os métodos disponíveis e seus códigos:\n')
print('1 - Download páginas html do dominiopublico.gov.br de livos em Português: <OUTPUT_PATH>')
print('2 - Download todos os PDFs a partir das páginas html: <INPUT_PATH> <OUTPUT_PATH> <EMAIL> <PASSWORD>')
print('3 - Converter todos os PDFs para TXTs: <INPUT_PATH> <OUTPUT_PATH>')
print('4 - Criar o Compêndio a partir dos arquivos TXT: <INPUT_PATH> <OUTPUT_PATH> [OUTPUT_FILE (default: compendio.txt)]\n')
print('------------------------------------------------------------------------------------------------------')

args = sys.argv
option = int(args[1]) if len(args) >= 2 else 0

if option is 1:
    if len(args) >= 3:
        download_html_pages(args[2])
    else:
        option = -1
elif option is 2:
    if len(args) >= 6:
        links = get_links_list_from_html_pages(args[2])
        download_pdfs(args[3], links, args[4], args[5])
    else:
        option = -1
elif option is 3:
    if len(args) >= 4:
        convert_pdfs_to_txts(args[2], args[3])
    else:
        option = -1
elif option is 4:
    if len(args) >= 4:
        output_file = args[4] if len(args) >= 5 else 'compendio.txt'
        create_compendium_of_unique_words(args[2], args[3], output_file)
    else:
        option = -1
