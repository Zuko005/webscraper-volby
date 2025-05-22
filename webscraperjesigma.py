import requests
import bs4 as bs
import csv
cislo_obci = list()
nazev_obci = list()
pocet_volicu = list()
pocet_obalek = list()
pocet_valid_obalek = list()
nazev_strany = list()
pocet_hlasu_strany = list()
pocet_procent_strany = list()
def scrape(odkaz):
    page = requests.get(odkaz)
    soup = bs.BeautifulSoup(page.text, 'html.parser')
    hledam_jmeno_obce = soup.find_all("td",class_="overflow_name")
    hledam_cislo_obce = soup.find_all("td",class_="cislo")
    for cislo_obce in hledam_cislo_obce:
        cislo_obci.append(cislo_obce.text)
    for td_element in hledam_jmeno_obce:
        nazev_obci.append(td_element.text)
    link_pokud_ma_okrsek = "https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec=589276&xokrsek=1&xvyber=7103"
    link_pokud_nema_okrsek = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec={cislo_obci}&xvyber=7103"
    count = 0
    for cislo in cislo_obci:
        adresa = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec={cislo}&xvyber=7103"
        response = requests.get(adresa)
        if response.status_code != 200:
            print(f"Adresa nefunguje, chyba: {adresa}")
        else:
            soup1 = bs.BeautifulSoup(response.text, 'html.parser')
            count += 1
            hledam_volice = soup1.find_all("td",class_="cislo",headers="sa2") #hledá počet voličů z html
            for volice in hledam_volice:
                pocet_volicu.append(volice.text)
                print(volice.text)
            hledam_obalky = soup1.find_all("td",class_="cislo",headers="sa5") #hledá počet obálek z html
            for obalky in hledam_obalky:
                pocet_obalek.append(obalky.text)
                print(obalky.text)
            hledam_valid_obalky = soup1.find_all("td",class_="cislo",headers="sa6") #hledá validní obálky z html
            for valid_obalky in hledam_valid_obalky:
                pocet_valid_obalek.append(valid_obalky.text)
                print(valid_obalky.text)
            hledam_jmeno_strany_prvni_tabulka = soup1.find_all("td",class_="overflow_name",headers="t1sa1 t1sb2")
            for strany in hledam_jmeno_strany_prvni_tabulka:
                nazev_strany.append(strany.text)
            hledam_jmeno_strany_druha_tabulka = soup1.find_all("td",class_="overflow_name",headers="t2sa1 t2sb2")
            for jmeno_strany in hledam_jmeno_strany_druha_tabulka:
                nazev_strany.append(jmeno_strany.text)
            hledam_pocet_hlasu_strany_prvni_tabulka = soup1.find_all("td",class_="cislo",headers="t1sa2 t1sb3")
            for pocet_hlasu in hledam_pocet_hlasu_strany_prvni_tabulka:
                pocet_hlasu_strany.append(pocet_hlasu.text)
            hledam_pocet_hlasu_strany_druha_tabulka = soup1.find_all("td",class_="cislo",headers="t2sa2 t2sb3")
            for pocet_hlasu_druha_tabulka in hledam_pocet_hlasu_strany_druha_tabulka:
                pocet_hlasu_strany.append(pocet_hlasu_druha_tabulka.text)
            hledam_procenta_strany_prvni_tabulka = soup1.find_all("td",class_="cislo",headers="t1sa2 t1sb4")
            for procenta_strany in hledam_procenta_strany_prvni_tabulka:
                pocet_procent_strany.append(procenta_strany.text)
            hledam_procenta_strany_druha_tabulka = soup1.find_all("td",class_="cislo",headers="t2sa2 t2sb4")
            for procento_druha_tabulka in hledam_procenta_strany_druha_tabulka:
                pocet_procent_strany.append(procento_druha_tabulka.text)
            print("adresa je cool a funguje jsi cool",count)





#for index,cislo in enumerate(cislo_obci):
    #https: // www.volby.cz / pls / ps2017nss / ps311?xjazyk = CZ & xkraj = 12 & xobec = {cislo} & xvyber = 7103

#prevod do csv
#try:
    #with open(file, 'w', newline='', encoding='utf-8') as csvfile:
        #writer = csv.writer(csvfile)
