# Kreiranje Poročil Štetja

Aplikacija za avtomatsko generiranje PDF poročil iz .dat datotek štetja bankovcev.

## Opis

Program prebere XML podatke iz .dat datotek, ki vsebujejo informacije o preštetih bankovcih, in ustvari pregledno PDF poročilo. Poročilo vsebuje:
- Podatke o podjetju
- Datum štetja
- Razčlenjen prikaz števila in vrednosti bankovcev po apoenih
- Skupno vrednost preštetih bankovcev
- Vse zneske formatirane v slovenskem formatu (npr. 1.234,56 EUR)

## Funkcionalnosti

- Samodejno zaznavanje .dat datotek v mapi
- Možnost izbire med več datotekami
- Avtomatsko kreiranje PDF poročila
- Premik obdelanih datotek v mapo "Obdelano"
- Samodejno odpiranje generiranega PDF-ja

## Namestitev

1. Prenesite najnovejšo verzijo .exe datoteke iz [releases](link_do_releases)
2. Kopirajte .exe datoteko v mapo, kjer se nahajajo .dat datoteke za obdelavo
3. Zaženite program z dvoklikom na .exe datoteko

## Uporaba

1. Zaženite program
2. Če je v mapi več .dat datotek:
   - Program bo prikazal seznam vseh najdenih datotek
   - Izberite želeno datoteko z vnosom številke
   - Ali pritisnite Enter za obdelavo najnovejše datoteke
3. Program bo:
   - Ustvaril PDF poročilo
   - Premaknil izvorno datoteko v mapo "Obdelano"
   - Samodejno odprl generirano poročilo

## Zahteve

- Windows operacijski sistem
- Adobe Reader ali drug PDF pregledovalnik
- Dostop do pisanja v mapo, kjer se program izvaja

## Razvoj

Za razvoj potrebujete:
- Python 3.x
- Knjižnice:
  - reportlab
  - glob
  - os
  - shutil
  - datetime

## Licenca

Ta projekt je licenciran pod MIT licenco - glej [LICENSE](LICENSE) datoteko za podrobnosti.

## Avtor

Erik Klavora, 2025

## Verzija

Trenutna verzija: 1.0.0
