import  requests
from bs4 import BeautifulSoup
import pandas as pd

def get_total_page(totalpaginas):
    paginas=[]
    for i in range(1, totalpaginas +1 ):
        url = "https://www.linio.com.co/c/computacion?page="+str(i)
        paginas.append(url)
    return paginas

def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_index_data(soup):
    div = soup.find_all('div', class_='catalogue-product row')
    baner = []
    for item in range(0, len(div)):
        a = div[item].find('a')
        baner.append(a)
    urls = ['https://www.linio.com.co' + item.get('href') for item in baner]
    return urls



def Main():
    datos = []
    id = 0
    #url = "https://www.linio.com.co/p/aio-todo-en-uno-hp-20-c412la-intel-dual-core-disc1tb-ram-4gb-bluetooth-w10-onxhog?qid=7692bb02e2d83d52433a241018b04a8c&oid=HP071EL14RSXWLCO&position=1&sku=HP071EL14RSXWLCO"
    #productos = get_index_data(get_page(url))  # urls
    #soup = get_page(url)
    urls = get_total_page(7)
    for i in range(0,len(urls)):
        url = urls[i]
        productos = get_index_data(get_page(url))
        for links in productos:
            soup = get_page(links)
            try:
                titulo = soup.find('h1', class_='col-xs-12 product-title-box').text.strip()
                id = id + 1;
            except:
                titulo = ' '
            try:
                precio = soup.find('span', class_='price-main-md').text.strip()
            except:
                precio = ' '
            autores = soup.find_all('div', class_='review-author')
            comentarios = soup.find_all('div', class_='review-text')
            calificaiones = soup.find_all('div', class_='review-item')
            autor = ""
            coment = ""
            valor = ""
            data = ""
            for i in range(0, len(comentarios)):
                autor = autores[i].text.strip()
                coment = comentarios[i].text.strip()
                aux = calificaiones[i].find('span', class_='star-rating').find('meta')
                if aux == None:
                    pass
                else:
                    valor = aux.get('content')
                data = [id,titulo, precio, coment, valor, autor]
                datos.append(data)
    df = pd.DataFrame(datos, columns=['Id Producto','Titulo', 'Precio', 'Reseñas', 'Estrellas', 'Autor'])
    df.to_csv('linio3.5.csv', index=False, encoding="utf-8-sig")


if __name__ == '__main__':
    Main()