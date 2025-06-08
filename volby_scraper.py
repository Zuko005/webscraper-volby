import requests
import bs4 as bs
import csv
import sys

cislo_obci = list()
nazev_obci = list()
pocet_volicu = list()
pocet_obalek = list()
pocet_valid_obalek = list()

vsechny_hlasy_stran_za_obce = []

nazvy_stran = set()

def scrape(odkaz, nazev_vystupniho_souboru):
    page = requests.get(odkaz)
    soup = bs.BeautifulSoup(page.text, 'html.parser')

    hledam_jmeno_obce = soup.find_all("td",class_="overflow_name")
    hledam_cislo_obce = soup.find_all("td",class_="cislo")

    for cislo_obce_element in hledam_cislo_obce:
        cislo_obci.append(cislo_obce_element.text)
    for td_element in hledam_jmeno_obce:
        nazev_obci.append(td_element.text)

    count = 0
    for aktualni_cislo_obce in cislo_obci:
        adresa = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=12&xobec={aktualni_cislo_obce}&xvyber=7103"
        response = requests.get(adresa)

        if response.status_code != 200:
            print(f"Adresa nefunguje pro obec {aktualni_cislo_obce}, chyba: {adresa}")
            pocet_volicu.append("N/A")
            pocet_obalek.append("N/A")
            pocet_valid_obalek.append("N/A")
            vsechny_hlasy_stran_za_obce.append({})
            continue
        else:
            soup1 = bs.BeautifulSoup(response.text, 'html.parser')
            count += 1
            print(f"Processing obec ID: {aktualni_cislo_obce}, count: {count}")

            volice = soup1.find("td", class_="cislo", headers="sa2")
            pocet_volicu.append(volice.text.replace('\xa0', ' ') if volice else "N/A")

            obalky = soup1.find("td", class_="cislo", headers="sa5")
            pocet_obalek.append(obalky.text.replace('\xa0', ' ') if obalky else "N/A")

            valid_obalky = soup1.find("td", class_="cislo", headers="sa6")
            pocet_valid_obalek.append(valid_obalky.text.replace('\xa0', ' ') if valid_obalky else "N/A")

            aktualni_nazvy_stran_obec = []
            aktualni_hlasy_stran_obec = []

            hledam_jmeno_strany_prvni_tabulka = soup1.find_all("td",class_="overflow_name",headers="t1sa1 t1sb2")
            aktualni_nazvy_stran_obec.extend([s.text for s in hledam_jmeno_strany_prvni_tabulka])

            hledam_pocet_hlasu_strany_prvni_tabulka = soup1.find_all("td",class_="cislo",headers="t1sa2 t1sb3")
            aktualni_hlasy_stran_obec.extend([h.text.replace('\xa0', ' ') for h in hledam_pocet_hlasu_strany_prvni_tabulka])

            hledam_jmeno_strany_druha_tabulka = soup1.find_all("td",class_="overflow_name",headers="t2sa1 t2sb2")
            aktualni_nazvy_stran_obec.extend([s.text for s in hledam_jmeno_strany_druha_tabulka])

            hledam_pocet_hlasu_strany_druha_tabulka = soup1.find_all("td",class_="cislo",headers="t2sa2 t2sb3")
            aktualni_hlasy_stran_obec.extend([h.text.replace('\xa0', ' ') for h in hledam_pocet_hlasu_strany_druha_tabulka])

            party_votes_for_this_obec = {}
            for j, party_name in enumerate(aktualni_nazvy_stran_obec):
                if j < len(aktualni_hlasy_stran_obec):
                    hlasy = aktualni_hlasy_stran_obec[j]
                    party_votes_for_this_obec[party_name] = hlasy
                    nazvy_stran.add(party_name)
                else:
                    party_votes_for_this_obec[party_name] = "N/A"

            vsechny_hlasy_stran_za_obce.append(party_votes_for_this_obec)

            print(f"  Úspěšně zpracována obec: {aktualni_cislo_obce}")

    headers = ["Cislo Obce", "Nazev Obce", "Pocet Volicu", "Pocet Obalek", "Pocet Validnich Obalek"]
    dynamic_party_headers = sorted(list(nazvy_stran))
    headers.extend(dynamic_party_headers)

    try:
        with open(nazev_vystupniho_souboru, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers, restval="0")

            writer.writeheader()

            pocet_obci_k_zapisu = len(cislo_obci)
            for i in range(pocet_obci_k_zapisu):
                row_data = {
                    "Cislo Obce": cislo_obci[i] if i < len(cislo_obci) else "N/A",
                    "Nazev Obce": nazev_obci[i] if i < len(nazev_obci) else "N/A",
                    "Pocet Volicu": pocet_volicu[i] if i < len(pocet_volicu) else "N/A",
                    "Pocet Obalek": pocet_obalek[i] if i < len(pocet_obalek) else "N/A",
                    "Pocet Validnich Obalek": pocet_valid_obalek[i] if i < len(pocet_valid_obalek) else "N/A"
                }

                if i < len(vsechny_hlasy_stran_za_obce):
                    row_data.update(vsechny_hlasy_stran_za_obce[i])

                writer.writerow(row_data)

        print(f"\nData byla úspěšně zapsána do souboru '{nazev_vystupniho_souboru}'")

    except IndexError as e:
        print(f"\nChyba při zápisu do CSV: Nesoulad v délce seznamů. Zkontrolujte, zda se všechny seznamy plní pro každou obec. Chyba: {e}")
    except Exception as e:
        print(f"\nNastala neočekávaná chyba při zápisu do CSV: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Použití: python nazev_skriptu.py <url_ke_scrapovani> <nazev_vystupniho_souboru.csv>")
        print("Příklad: python volby_scraper.py https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 vysledky_voleb_2017.csv")
        sys.exit(1)

    scrape_url = sys.argv[1]
    output_filename = sys.argv[2]

    if not output_filename.endswith(".csv"):
        output_filename += ".csv"

    scrape(scrape_url, output_filename)
