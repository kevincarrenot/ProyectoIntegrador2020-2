import  requests
from bs4 import BeautifulSoup
import pandas as pd

def get_page(url):
    response = requests.get(url)
    if not response.ok:
        print('Server responded: ', response.status_code)
    else:
        soup=BeautifulSoup(response.text, 'html.parser')
    return soup

def get_index_data(soup):
    div=soup.find_all('div', class_='catalogue-product row')
    baner=[]
    for item in range(0,len(div)):
        a=div[item].find('a')
        baner.append(a)
    urls=['https://www.linio.com.co'+item.get('href') for item in baner]
    return urls



def main():
    datos=[]
    url = 'https://www.linio.com.co/c/computacion'
    productos=get_index_data(get_page(url)) #urls

    for link in productos:
        soup=get_page(link)
        try:
            titulo=soup.find('h1', class_='col-xs-12 product-title-box').text.strip()
        except:
             titulo=' '
        try:
            precio=soup.find('span', class_='price-main-md').text.strip()
        except:
            precio=' '
        autores=soup.find_all('div', class_='review-author')
        comentarios=soup.find_all('div', class_='review-text')
        calificaiones=soup.find_all('span', class_='star-rating')
        autor=""
        coment=""
        valor=""
        data=""
        for i in range(0,len(comentarios)):
            autor=autores[i].text.strip()
            coment=comentarios[i].text.strip()
            aux=calificaiones[i]
            meta=aux.find('meta')
            if meta==None:
                pass
            else:
                valor=meta.get('content')
            data = [titulo,precio,coment,valor, autor]
            datos.append(data)
        df = pd.DataFrame(datos, columns=['Titulo', 'Precio', 'Reseñas', 'Estrellas', 'Autor'])
        print(df)
        #df.to_csv('linio.csv', index = False)
   
 
if __name__=='__main__':
    main()