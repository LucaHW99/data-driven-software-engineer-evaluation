

import os
import pandas as pd
from PDF2 import PdfLeggi, PdfErrore
from pathlib import Path

class EstattorePDF:
    def __init__(self, cartella_pdf):
        self.cartella_pdf = cartella_pdf
        self.dati = []

    def estrai_dati(self):
        for file_pdf in Path(self.cartella_pdf).glob("*.pdf"):
            self.estrai_dati_da_file(file_pdf)

    def estrai_dati_da_file(self, file_pdf):
        try:
            lettore = PdfLeggi(file_pdf)
            testo = self.estrai_testo(lettore)
            self.aggiungi_dati(file_pdf.name, testo)
        except (PdfErrore, Exception) as e:
            print(f"Errore con il file {file_pdf}: {e}")

    def estrai_testo(self, lettore):
        """Estrae il testo da un lettore PDF."""
        testo = "\n".join(pagina.extract_text() for pagina in lettore.pages if pagina.extract_text())
        return testo.strip()

    def aggiungi_dati(self, nome_file, testo):
        if testo:
            self.dati.append({"nome_file": nome_file, "contenuto": testo})

    def salva_csv(self, file_output):
        df = pd.DataFrame(self.dati)
        df.to_csv(file_output, index=False)

def main():
    cartella_pdf = './pdfs'
    file_output = './output/dati_estratti.csv'

    os.makedirs(os.path.dirname(file_output), exist_ok=True)

    estrattore = EstattorePDF(cartella_pdf)
    estrattore.estrai_dati()
    estrattore.salva_csv(file_output)
    print(f"Dati estratti e salvati in {file_output}")

if __name__ == "__main__":
    main()