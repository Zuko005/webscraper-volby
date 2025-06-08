# Skript pro získávání výsledků voleb z volby.cz

Tento Python skript slouží k automatickému získávání (scrapování) dat o výsledcích voleb z webové stránky [volby.cz](https://www.volby.cz). Konkrétně stahuje data o obcích z daného kraje a následně podrobnosti o počtu voličů, obálek a hlasů pro jednotlivé strany v každé obci. Získaná data jsou uložena do CSV souboru.

## Co skript dělá?

1.  **Navštěvuje úvodní stránku:** Začíná na přehledové stránce pro daný kraj a volby (URL je zadána jako argument).
2.  **Sbírá ID a názvy obcí:** Z této stránky extrahuje číselné kódy (ID) a názvy všech obcí.
3.  **Detailní sběr dat pro každou obec:** Pro každou nalezenou obec navštíví její detailní stránku s výsledky.
4.  **Extrahování dat:** Z detailní stránky získává:
    * Počet voličů
    * Počet vydaných obálek
    * Počet platných hlasů
    * Názvy politických stran a počet hlasů pro každou stranu.
    * Automaticky si pamatuje všechny unikátní názvy stran, aby je mohl použít jako sloupce v CSV.
5.  **Uložení do CSV:** Všechna získaná data jsou strukturovaně uložená do jednoho CSV souboru, jehož název je zadán jako argument.

## Jak spustit skript
Skript se spouští přímo z příkazové řádky a vyžaduje dva argumenty: URL stránky pro skrapování a název výstupního CSV souboru.

Uložte skript: Uložte kód do souboru s příponou .py (např. volby_scraper.py). Ujistěte se, že máte ve stejném adresáři i soubor requirements.txt.

Spusťte skript z terminálu: Otevřete terminál nebo příkazový řádek, přejděte do adresáře, kam jste soubor uložili, a spusťte skript následovně:


python volby_scraper.py <URL_PRO_SCRAPOVANI> <NAZEV_VÝSTUPNÍHO_SOUBORU.csv>
Příklad spuštění:

python volby_scraper.py [https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103](https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103) vysledky_jihomoravsky_2017.csv
https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103 je URL stránky pro skrapování (v tomto případě Jihomoravský kraj, volby 2017).
vysledky_jihomoravsky_2017.csv je název souboru, do kterého budou data uložena. Skript automaticky zajistí, že název souboru bude končit na .csv.


### Požadavky a instalace

Než skript spustíte, ujistěte se, že máte nainstalovány všechny potřebné knihovny. Tyto knihovny jsou uvedeny v souboru `requirements.txt`.

Pro instalaci všech závislostí otevřete terminál nebo příkazový řádek ve stejném adresáři jako váš skript a `requirements.txt` a spusťte následující příkaz:

```bash
pip install -r requirements.txt
