from csv import reader
from csv import writer

def carica_da_file(file_path):
    """Carica le foto dal file, creando un nuovo anno ogni volta che compare per la prima volta"""
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            lettore = reader(csvfile, delimiter=',')
            next(lettore, None) #Uso il comando next() per saltare la prima riga di intestazione, se il file fosse vuoto: restituisce None.

            album = {}
            for riga in lettore:
                annoFoto = int(riga[4])
                datiFoto = {
                    "codice": riga[0],
                    "titolo": riga[1],              #dizionario dati rimanenti
                    "autore": riga[2],
                    "mese": int(riga[3])
                }

                if annoFoto not in album:
                    album[annoFoto] = []

                album[annoFoto].append(datiFoto)

        #Per visualizzare le foto in ordine temporale
        for foto in album.values():
            foto.sort(key=lambda datiFoto: datiFoto["mese"])
            """Uso .sort() per riordinare la lista, essendo foto una lista all'interno di un'altra lista album, la seconda (quella esterna) si aggiornerá 
            automaticamente senza dover fare due passaggi. """
            #key serve a indicare quale elemento viene usato come discriminante

        return album

    except FileNotFoundError:
        return None

def aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path):
    """Aggiunge una foto all'album, creando l'anno al volo se non è ancora presente"""
    try:
        anno = int(anno)
        mese = int(mese)
    except (ValueError, TypeError):
        print("Errore: mese e anno devono essere numeri interi.")
        return None

    if not 1 <= mese <= 12:
        print("Errore: il mese deve essere compreso tra 1 e 12.")
        return None

    for lista_foto in album.values():
        for foto in lista_foto:
            if foto["codice"] == codice:
                print(f"Errore: il codice '{codice}' é giá presente nell'album.")
                return None

    nuova_foto = {
        "codice": codice,
        "titolo": titolo,
        "autore": autore,
        "mese": mese
    }

    try:
        with open(file_path, 'r+', encoding='utf-8', newline='') as csvfile: #Metto r+ per richiedere l'esistenza del file
            csvfile.seek(0,2) #Comando necessario dato l'utilizzo del seek(); 0: nessuna modifica rispetto al punto di riferimento; 2: il punto di riferimento
            scrittore = writer(csvfile, delimiter=',')
            scrittore.writerow([codice, titolo, autore, mese, anno]) #indico i nomi delle varie colonne del file csv
    except FileNotFoundError:
        return None

    if anno not in album:
        album[anno] = []

    album[anno].append(nuova_foto)
    album[anno].sort(key=lambda datiFoto: datiFoto["mese"]) #stesso discorso fatto in precedenza

    return nuova_foto

def cerca_foto(album, codice):
    """Cerca una foto nell'album dato il codice."""
    for anno, lista_foto in album.items():
        for foto in lista_foto:
            if codice == foto["codice"]:
                return (
                    f"{foto['codice']},{foto['titolo']},"
                    f"{foto['autore']},{foto['mese']},{anno}"
                )

    return None

def elenco_foto_anno_per_titolo(album, anno):
    """Ordina i titoli delle foto di un dato anno in ordine alfabetico"""
    if anno not in album:
        return None

    titoli = []

    for foto in album[anno]:
        titoli.append(foto["titolo"])

    titoli.sort()
    return titoli


def main():
    album = []
    file_path = "album_fotografico.csv"

    while True:
        print("\n--- MENU ALBUM FOTOGRAFICO ---")
        print("1. Carica album da file")
        print("2. Aggiungi una nuova foto")
        print("3. Cerca una foto per codice")
        print("4. Elenco foto di un anno (ordinato per titolo)")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                album = carica_da_file(file_path)
                if album is None:
                    break
                else:
                    for anno, lista_foto in album.items():
                        print(f"\nAnno {anno}:")

                        for foto in lista_foto:
                            print(
                                f"{foto['codice']} - {foto['titolo']} - "
                                f"{foto['autore']} - mese {foto['mese']}"
                            )
                    break

        elif scelta == "2":
            if album is None:
                print("Prima carica l'album da file.")
                continue

            codice = input("Codice della foto: ").strip()
            titolo = input("Titolo: ").strip()
            autore = input("Autore: ").strip()

            try:
                mese = int(input("Mese (1-12): ").strip())
                anno = int(input("Anno: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per mese e anno.")
                continue

            foto = aggiungi_foto(album, codice, titolo, autore, mese, anno, file_path)
            if foto is not None:
                print(f"\nFoto '{foto['titolo']}' aggiunta con successo!")

        elif scelta == "3":
            if album is None:
                print("L'album è vuoto.")
                continue

            codice = input("Inserisci il codice della foto da cercare: ").strip()
            risultato = cerca_foto(album, codice)
            if risultato:
                print(f"\nFoto trovata: {risultato}")
            else:
                print("Foto non trovata.")

        elif scelta == "4":
            if album is None:
                print("L'album è vuoto.")
                continue

            try:
                anno = int(input("Inserisci l'anno da consultare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_foto_anno_per_titolo(album, anno)
            if titoli is not None:
                print(f'\nFoto del {anno}:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))
            else:
                print(f"\nNessuna foto trovata per l'anno {anno}.")

        elif scelta == "5":
            print("\nUscita dal programma...")
            break
        else:
            print("\nOpzione non valida. Riprova.")


if __name__ == "__main__":
    main()
