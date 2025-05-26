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
scrape("https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103")
output_filename = "vysledky_obci.csv"

#hlavičky pro každý sloupec
headers = ["Cislo Obce", "Nazev Obce", "Pocet Volicu", "Pocet Obalek", "Pocet Validnich Obalek"]

try:
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        cisla_ob = len(cislo_obci)
        for i in range(cisla_ob):
            row = [
                cislo_obci[i] if i < len(cislo_obci) else "N/A",
                nazev_obci[i] if i < len(nazev_obci) else "N/A",
                pocet_volicu[i] if i < len(pocet_volicu) else "N/A",
                pocet_obalek[i] if i < len(pocet_obalek) else "N/A",
                pocet_valid_obalek[i] if i < len(pocet_valid_obalek) else "N/A"
            ]
            writer.writerow(row)
    print(f"\nData byla úspěšně zapsána do souboru '{output_filename}'")

except IndexError as e:
    print(f"\nChyba při zápisu do CSV: Nesoulad v délce seznamů. Zkontrolujte, zda se všechny seznamy plní pro každou obec. Chyba: {e}")
except Exception as e:
    print(f"\nNastala neočekávaná chyba při zápisu do CSV: {e}")

