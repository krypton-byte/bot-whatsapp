from selenium import webdriver
import selenium, random
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests, json, time, datetime, wikipedia
from googletrans import Translator
from datetime import date
import spam, pyqrcode, xerox
#inisialisasi
wikipedia.set_lang('id')
tra=Translator()
newline=Keys.SHIFT+Keys.ENTER+Keys.SHIFT
#membuka jendela chrome
driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com')
input('enter jika sudah scan barcode : ')
import sqlite3
class datatoken:
    def __init__(self, token=None, url=None):
        self.token = token
        self.token = token
        self.url   = url
    def buat(self):
        db=sqlite3.connect('data.db')
        c=db.cursor()
        c.execute('INSERT INTO LIRIK VALUES ("%s","%s")'%(self.token, self.url))
        db.commit()
        return True
    def cari(self):
        db=sqlite3.connect('data.db')
        c=db.cursor()
        hasil=c.execute("SELECT * FROM LIRIK WHERE ID='%s'"%(self.token)).fetchall()
        return hasil
def cekduplikat(arr):
    setArr = set()
    for cek in arr:
        if cek in setArr:
            return True
        else:
            setArr.add(cek)
    return False
def jumlahBelumTerbaca():
    jum=0
    for angka in driver.find_elements_by_xpath('//span[@class="_31gEB"]'):
        jum+=int(angka.text)
    return jum
def kirimTextMedia(pesan, path):
    driver.find_element_by_css_selector('span[data-icon="clip"]').click()
    driver.find_element_by_css_selector('input[type="file"]').send_keys(path)
    time.sleep(3)
    driver.find_element_by_xpath('//span[@data-testid="emoji-input"]').click()
    form_pesan=driver.find_element_by_xpath('//div[@class="_2FVVk _3WjMU _1C-hz"]')
    form_pesan.click()
    xerox.copy(pesan)
    form_pesan.send_keys(Keys.CONTROL+'v')
    driver.find_element_by_xpath('//span[@data-testid="send"]').click()
def kirimMedia(path):
    driver.find_element_by_css_selector('span[data-icon="clip"]').click()
    driver.find_element_by_css_selector('input[type="file"]').send_keys(path)
    time.sleep(2)
    driver.find_element_by_xpath('//span[@data-testid="send"]').click() #data-icon="send" data-testid="send"
def kirim(pesan):
    form_pesan=driver.find_element_by_class_name('_3uMse')
    xerox.copy(pesan)
    form_pesan.send_keys(Keys.CONTROL+'v')
    driver.find_element_by_class_name('_1U1xa').click()
def cari():
    body = driver.find_elements_by_xpath('//span[@class="_3ko75 _5h6Y_ _3Whw5"]')
    for hasilCari in enumerate(body):
        perintah=hasilCari[1].text.lower().split(' ')
        if perintah[0] in ['.help','.menu']:
            body[hasilCari[0]].click()
            kirim('''
<=======> *MENU* <=======>
=> .covid19
=> .rename
=> .love
=> .editdesk
=> .intro
=> .all
=> .dump2txt
=> .spamx <num> <jum>
=> .spamas <num1> <num2>
=> .cari <query>
=> .film <query>
=> .header <url>
=> .wikipedia <query>
=> .author
=> .qrmaker
<======================>
''')
        elif perintah[0] in ['.showlrc','.showlyrics']:
            body[hasilCari[0]].click()
            if len(perintah) == 1:
                kirim('contoh: .showlrc <ID>')
            else:
                car=datatoken(token=perintah[1]).cari()
                if car:
                    print(car[0][1])
                    pars=BeautifulSoup(requests.get(car[0][1],headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}).text,'html.parser')
                    pesan=pars.title.text+'\n'
                    if pars.find_all('span',class_="lyrics__content__ok"):
                        for i in pars.find_all('span',class_="lyrics__content__ok"):
                            pesan+="\n%s"%i.text
                            print(str(i.text))
                        kirim(pesan)
                    elif pars.find_all('span', class_='lyrics__content__warning'):
                        for i in pars.find_all('span',class_="lyrics__content__ok"):
                            pesan+="\n%s"%i.text
                            print(str(i.text))
                        kirim(pesan)
                    else:
                        kirim(pesan+'\n lirik Tidak Ada')
                else:
                    kirim('ID : *%s* Tidak Tersedia'%perintah[1])
        elif perintah[0] in ['.lrc','.lyric']:
            body[hasilCari[0]].click()
            if len(perintah) == 1:
                kirim('contoh : .lrc <judul>')
            else:
                body[hasilCari[0]].click()
                url='https://api.musixmatch.com/ws/1.1/track.search'
                params={
                    'apikey':'f009dbb46a73fd4cdf7fe2cc8d7d8648',
                    'q':' '.join(perintah[1:])
                }
                pars=json.loads(requests.get(url, params=params).text)['message']['body']['track_list']
                textpesan=''
                if pars:
                    for i in pars:
                        textpesan+='Judul : *%s*\nID : *%s*\n'%(i['track']['track_name'] ,i['track']['track_id'])
                        datatoken(token=i['track']['track_id'], url=i['track']['track_share_url']).buat()
                    kirim(textpesan)
                else:
                    kirim('*Lirik %s Tidak Ada*'%(' '.join(perintah[1:])))
        elif perintah[0] in ['.movie','.film']:
            body[hasilCari[0]].click()
            if len(perintah) == 1:
                kirim('Format : .film <query>')
            else:
                params={
                    'api_key':'c777b356fbafb9de37782825f2b2340b',
                    'query':' '.join(perintah[1:])
                }
                hasil=requests.get('https://api.themoviedb.org/3/search/movie',params=params).json()
                if hasil['results']:
                    pesan='''
Judul       : %s
Jumlah Vote : %s
Vote Rata2  : %s
Video       : %s
Tgl Rilis   : %s
Synopsis[En]: %s
Synopsis[Id]: %s
'''%(hasil['results'][0]['title'], hasil['results'][0]['vote_count'], hasil['results'][0]['vote_average'], str(hasil['results'][0]['video']), hasil['results'][0]['release_date'], hasil['results'][0]['overview'], tra.translate(text=hasil['results'][0]['overview'], dest='id').text)
                    img=requests.get('http://image.tmdb.org/t/p/w200%s'%hasil['results'][0]['poster_path'])
                    if img.status_code == 200:
                        open('poster.jpg','wb').write(img.content)
                        kirimTextMedia(pesan,'D:/bot-admin/poster.jpg')
                    else:
                        kirimTextMedia(pesan,'D:/bot-admin/no_poster.png')
                else:
                    kirim('*MA\'AF FILM "%s" BELUM TERSEDIA*'%' '.join(perintah[1:]))
        elif perintah[0] in ['.covid','.covid19']:
            body[hasilCari[0]].click()
            par=BeautifulSoup(requests.get('https://kawalcorona.com/').text,'html.parser')
            hasil=par.find_all('p', class_='text-white mb-0')[6:][0].text.replace('POSITIF','').replace('MENINGGAL','').replace('SEMBUH','').split(' , ')
            print(str(hasil))
            waktu = time.asctime(time.localtime(time.time())).replace('Sun','Min').replace('Min','Sen').replace('Tue','Sel').replace('Wed','Rab').replace('Thu','Kam').replace('Fri','Jum').replace('Sat','Sab').split(' ')
            kirimTextMedia('''
=======> *INDONESIA* <=======
=> Date : %s
=> Positif   : %s 👥
=> Meninggal : %s 👥
=> Sembuh    : %s 👥
===========================

'''%(' '.join([waktu[0], waktu[2], waktu[1], waktu[4]]), hasil[0],  hasil[2], hasil[1]),'D:/bot-admin/%s'%random.choice(['covid.png','covid2.png','covid3.png','covid4.png']))
        elif perintah[0] in ['.love','.lope']:
            body[hasilCari[0]].click()
            kirim('❤️')
        elif perintah[0] in ['.rename','.ubahnama']:
            body[hasilCari[0]].click()
            driver.find_element_by_xpath('//span[@class="_3-cMa _3Whw5"]').click()
            try:
                driver.find_element_by_xpath('//span[@data-testid="pencil"]').click()
                driver.find_element_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]').clear()
                xe=(' '.join(hasilCari[1].text.split(' ')[1:])).replace('\n',newline)
                print(' '.join(hasilCari[1].text.split(' ')[1:])+'      ya')
                driver.find_element_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]').send_keys(xe)
                driver.find_element_by_xpath('//span[@data-testid="checkmark"]').click()
                driver.find_element_by_xpath('//span[@data-testid="x"]').click()
                kirim(f'*grup* berhasil di ubah kenama {" ".join(hasilCari[1].text.split(" ")[1:])}')
            except (selenium.common.exceptions.InvalidElementStateException, selenium.common.exceptions.NoSuchElementException):
                driver.find_element_by_xpath('//span[@data-testid="x"]').click()
                kirim(f'*gagal* mengubah nama grup ke {" ".join(hasilCari[1].text.split(" ")[1:])}')
        elif perintah[0] in ['.deskedit','.editdesk']:
            body[hasilCari[0]].click()
            driver.find_element_by_xpath('//span[@class="_3-cMa _3Whw5"]').click()
            try:
                driver.find_elements_by_xpath('//span[@data-testid="pencil"]')[1].click()
                time.sleep(2)
                driver.find_elements_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]')[1].clear()
                print(hasilCari[1].text)
                xerox.copy(driver.find_elements_by_xpath('//div[@class="eRacY"]/span[@class="_3Whw5 selectable-text invisible-space copyable-text"]')[-1].text[10:].replace(Keys.SHIFT+Keys.CONTROL,'\n'))
                driver.find_elements_by_xpath('//div[@class="_3FRCZ copyable-text selectable-text"]')[1].send_keys(Keys.CONTROL+'v')
                driver.find_elements_by_xpath('//span[@data-testid="checkmark"]')[0].click()
                driver.find_element_by_xpath('//span[@data-testid="x"]').click()
                kirim('*Berhasil Mengubah Deskripsi*')
            except (selenium.common.exceptions.InvalidElementStateException, selenium.common.exceptions.NoSuchElementException, IndexError):
                kirim('*Gagal Mengubah Deskripsi*')
        elif perintah[0] in ['.cari','.search']:
            body[hasilCari[0]].click()
            if len(perintah) == 1:
                kirim("*MASUKAN QUERY DENGAN BENAR*")
            else:
                hasil=wikipedia.search(' '.join(perintah[1:]))
                kirim('Hasil Penelusuran : \n => '+'\n => '.join(hasil))
        elif perintah[0] in ['.header','.head']:
            body[hasilCari[0]].click()
            if len(perintah) == 2:
                try:
                    pesan=''
                    jso=requests.get(perintah[1]).headers
                    hasil=dict(jso).keys()
                    for ar in hasil:
                        pesan+='%s:%s\n'%(ar,jso[ar])
                    kirim(pesan)
                except (requests.exceptions.ConnectionError, requests.exceptions.MissingSchema):
                    kirim('*MASUKAN URL DENGAN BENAR*')
            else:
                kirim('format : \n.header <url>')
        elif perintah[0] in ['.wikipedia','.wiki']:
            body[hasilCari[0]].click()
            try:
                hasil=wikipedia.page(perintah[1:])
                body[hasilCari[0]].click()
                kirim(hasil.summary)
            except wikipedia.exceptions.PageError:
                kirim(' Query %s Tidak tersedia'%(' '.join(perintah[1:])))
        elif perintah[0] in ['.spammas','.spamas']:
            body[hasilCari[0]].click()
            if len(perintah) == 1:
                kirim('Format Salah : \n.spamas <no1> <no2> <no3> #max 7 nomer')
            elif len(perintah) <= 8:
                if cekduplikat(perintah[1:]):
                    kirim('. nomer harus tidak sama & harus benar ')
                else:
                    for cont in perintah[1:]:
                        if spam.klikdokter(cont):
                            kirim('✅ Terkirim : %s'%(cont))
                        else:
                            kirim('*Tidak Terkirim : %s*'%(cont))
            else:
                kirim('*max 7*')
        elif perintah[0] in ['.spamx','.spamk']:
            body[hasilCari[0]].click()
            print(perintah[0])
            if len(perintah) == 1:
                kirim('Format Salah : \n.spam 85xxxxx <jum>\n*gk support banyak-banyak karna membutuh delay dan itu membuat system saya lamban jadi saya membatasi sampe 3*')
            elif len(perintah) == 2:
                if spam.klikdokter(perintah[1]):
                    kirim('✅ Terkirim : %s'%(perintah[1]))
                else:
                    kirim('*Tidak Terkirim* : %s'%(perintah[1]))
            else:
                if len(perintah) == 3:
                    try:
                        if int(perintah[2]) <= 8:
                            for c in range(int(perintah[2])):
                                if spam.klikdokter(perintah[1]):
                                    kirim('✅ Terkirim : %s'%(perintah[1]))
                                else:
                                    kirim('*Tidak Terkirim : %s'%(perintah[1]))
                        else:
                            kirim('max : 8')
                    except ValueError:
                        kirim('Format Salah : \n.spam 85xxxxx <jum>\n*gk support banyak-banyak so\'alnya butuh delay dan itu membuat system saya lamban jadi saya membatasi sampe 3*')
        elif perintah[0] in ['.intro','.info']:
            body[hasilCari[0]].click()
            waktu = time.asctime(time.localtime(time.time())).replace('Sun','Min').replace('Min','Sen').replace('Tue','Sel').replace('Wed','Rab').replace('Thu','Kam').replace('Fri','Jum').replace('Sat','Sab').split(' ')
            kirimTextMedia('''
<========================>
*Nama*   : BOT [BETA]
*Update* : Sel, 14 Jul 2020
*Time*   : %s
*Unread* : %s pesan
Ketik " *.help*" untuk bantuan
<========================>
'''%( '%s %s %s %s %s'%(waktu[0], waktu[2], waktu[1], waktu[4], waktu[3]), jumlahBelumTerbaca()),'D:/bot-admin/%s'%random.choice(['avatar.jpg','avatar2.jpg','avatar3.jpeg']))
        elif perintah[0] in ['.dump2txt','.dumpcontact']:
            body[hasilCari[0]].click()
            bs=BeautifulSoup(driver.page_source,'html.parser')
            hasil=bs.find_all('span',class_='_3-cMa _3Whw5')[0].text.split(', ')
            tulis=open('hasil.txt','w')
            for tag in hasil[:-1]:
                tulis.write(tag+'\n')
            tulis.close()
            kirimMedia('D:/bot-admin/hasil.txt')
        elif perintah[0] in ['.qrmaker','.qr']:
            body[hasilCari[0]].click()
            if len(perintah) == 1:
                kirim('Format Salah : \n.qrmaker <text>')
            else:
                pyqrcode.create(' '.join(hasilCari[1].text.split(' ')[1:])).png('bar.png', scale=6)
                kirimTextMedia('*Berhasil Di Buat*\n*TEXT :* %s'%(' '.join(hasilCari[1].text.split(' ')[1:])),'D:/bot-admin/bar.png')
        elif perintah[0] in ['.author','.admin']:
            body[hasilCari[0]].click()
            kirimTextMedia('Tambahkan saya sebagai kontak di WhatsApp. https://wa.me/qr/6ZQZQ45RSKYLG1','D:/bot-admin/admin.jpeg')
        elif perintah[0] in ['.tag','.all']:
            body[hasilCari[0]].click()
            bs=BeautifulSoup(driver.page_source,'html.parser')
            hasil=bs.find_all('span',class_='_3-cMa _3Whw5')[0].text.split(', ')
            print(str(hasil))
            for tag in hasil[:-1]:
                xerox.copy(tag)
                driver.find_element_by_class_name('_3uMse').send_keys('@%s'%(Keys.CONTROL+'v'))
                driver.find_element_by_class_name('matched-text').click()
                driver.find_element_by_class_name('_3uMse').send_keys(' ')
            driver.find_element_by_class_name('_1U1xa').click()
while True:
    try:
        cari()    
    except (selenium.common.exceptions.StaleElementReferenceException, selenium.common.exceptions.NoSuchElementException):
        pass