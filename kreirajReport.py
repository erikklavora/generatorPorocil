import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os
import shutil
import glob
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))

def format_amount(amount):
    """Formatira znesek v slovenski format z ločilom tisočic in decimalk"""
    amount_str = f"{float(amount):,.2f}"
    # Najprej zamenjamo vse pike z vejicami
    amount_str = amount_str.replace(",", "X").replace(".", ",").replace("X", ".")
    return amount_str

def create_report(xml_file):
    # Preberi XML
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Pridobi datum iz imena datoteke
    filename_parts = os.path.basename(xml_file).split('_')
    date_str = filename_parts[3]  # 020525
    time_str = filename_parts[4]  # 094143
    
    # Pretvori datum in čas iz imena datoteke
    file_datetime = datetime.strptime(f"20{date_str} {time_str}", "%Y%m%d %H%M%S")
    slo_date = file_datetime.strftime("%d.%m.%Y")
    
    # Ustvari PDF
    pdf_filename = f"Porocilo_stetja_{file_datetime.strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    
    # Nastavi začetno pozicijo
    y_position = 800
    
    # Dodaj glavo z imenom podjetja
    c.setFont("Arial", 10)
    c.drawString(50, y_position, "Trine d.o.o., Neblo 11, 5212 Dobrovo")
    
    y_position -= 40
    
    # Dodaj naslov
    c.setFont("Arial-Bold", 16)
    c.drawString(50, y_position, f"Poročilo štetja {slo_date}")
    
    # Dodaj črto pod naslovom
    y_position -= 15
    c.line(50, y_position, 545, y_position)
    
    y_position -= 40
    
    # Dodaj uvodno besedilo
    c.setFont("Arial", 12)
    c.drawString(50, y_position, "V danem štetju je bilo preštetih:")
    
    y_position -= 30
    
    # Izpiši podatke za vsak apoen
    total_amount = 0
    
    # Najprej sortiraj apoene po vrednosti (padajoče)
    counters = []
    for counter in root.findall(".//Counter[@Currency='EUR']"):
        if counter.get('Output') == 'Stacked':
            counters.append(counter)
    
    counters.sort(key=lambda x: int(x.get('Value')), reverse=True)
    
    # Izpiši glavo tabele
    c.setFont("Arial", 11)
    c.drawString(50, y_position, "Apoen")
    c.drawString(200, y_position, "Število kosov")
    c.drawRightString(500, y_position, "Znesek")
    
    y_position -= 20
    # Nariši črto pod glavo tabele
    c.line(50, y_position, 545, y_position)
    y_position -= 15
    
    for counter in counters:
        value = counter.get('Value')
        currency = counter.get('Currency')
        number = counter.get('Number')
        amount = int(counter.get('Amount'))
        
        formatted_amount = format_amount(amount)
        
        c.drawString(50, y_position, f"Apoen {value} {currency}")
        # Ločeno izpišemo število (desno poravnano) in besedo "kos"
        c.drawRightString(250, y_position, str(number))
        c.drawString(260, y_position, "kos")
        c.drawRightString(500, y_position, f"{formatted_amount} EUR")
        y_position -= 25
    
    # Poišči skupni znesek
    total = root.find(".//Total[@Type='Stacked'][@Amount]")
    total_amount = int(total.get('Amount'))
    formatted_total = format_amount(total_amount)
    
    # Nariši črto nad skupnim zneskom
    y_position += 10
    c.line(50, y_position, 545, y_position)
    y_position -= 25
    
    c.setFont("Arial-Bold", 12)
    c.drawString(50, y_position, "Skupaj:")
    c.drawRightString(500, y_position, f"{formatted_total} EUR")
    
    # Dodaj nogo (pred c.save())
    c.setFont("Arial", 8)
    c.drawString(50, 30, "App za kreiranje poročil v.1.0.0, kreiral Erik Klavora 2025")
    
    # Shrani PDF
    c.save()
    
    # Premakni XML v mapo Obdelano
    if not os.path.exists("Obdelano"):
        os.makedirs("Obdelano")
    
    shutil.move(xml_file, os.path.join("Obdelano", os.path.basename(xml_file)))
    
    # Odpri ustvarjen PDF
    os.system(f'start {pdf_filename}')

def process_dat_files():
    # Poišči vse .dat datoteke
    dat_files = glob.glob("*.dat")
    if not dat_files:
        print("Ni najdenih .dat datotek v trenutni mapi.")
        return

    # Razvrsti datoteke po času nastanka (najnovejša prva)
    dat_files.sort(key=os.path.getctime, reverse=True)
    
    if len(dat_files) > 1:
        print("\nNajdenih več .dat datotek:")
        for i, file in enumerate(dat_files, 1):
            file_time = datetime.fromtimestamp(os.path.getctime(file))
            print(f"{i}. {file} (ustvarjena: {file_time.strftime('%d.%m.%Y %H:%M:%S')})")
        
        while True:
            try:
                choice = input("\nIzberite številko datoteke za obdelavo (ali pritisnite Enter za najnovejšo): ")
                if choice == "":
                    selected_file = dat_files[0]  # Vzemi najnovejšo
                    break
                choice = int(choice)
                if 1 <= choice <= len(dat_files):
                    selected_file = dat_files[choice-1]
                    break
                else:
                    print("Neveljavna izbira. Prosim izberite številko iz seznama.")
            except ValueError:
                print("Prosim vnesite veljavno številko.")
    else:
        selected_file = dat_files[0]
    
    print(f"\nObdelujem datoteko: {selected_file}")
    create_report(selected_file)

if __name__ == "__main__":
    process_dat_files()