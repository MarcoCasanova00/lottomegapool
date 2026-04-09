import itertools
import os
import sys

# Impostazioni Globali
MODALITA_SEVERA = True

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def spiega_errore(tipo, valore, dettagli):
    print(f"\n--- 🛑 BLOCCO MATEMATICO: {tipo} ---")
    print(f"Valore rilevato: {valore}")
    print(f"Spiegazione: {dettagli}")
    print("-" * 40)

def analizza_numeri(fissi, variabili, severa=True):
    numeri = [int(x) for x in fissi + variabili]
    pari = len([x for x in numeri if x % 2 == 0])
    dispari = 10 - pari
    
    # Calcolo Somma Prevista (Media dei 10 numeri proiettata su 5 estratti)
    media_dieci = sum(numeri) / 10
    somma_proiettata = media_dieci * 5
    
    errori = []
    avvisi = []

    # 1. Verifica Regola 3/2 (Pari/Dispari)
    if not (4 <= pari <= 6):
        msg = f"Hai scelto {pari} Pari e {dispari} Dispari. Statisticamente, le estrazioni con sbilanciamento > 4:1 sono rare. Il 68% delle vincite è 3:2 o 2:3."
        if severa: errori.append(("PARITÀ", f"{pari}P/{dispari}D", msg))
        else: avvisi.append(f"⚠️ Rapporto P/D sbilanciato ({pari}:{dispari}).")

    # 2. Verifica Intervallo Aureo (Somma 60-95)
    if somma_proiettata < 60:
        msg = "La tua selezione punta su numeri troppo bassi. La somma prevista è sotto il limite aureo di 60."
        if severa: errori.append(("SOMMA BASSA", int(somma_proiettata), msg))
        else: avvisi.append(f"⚠️ Somma proiettata bassa ({int(somma_proiettata)}).")
    elif somma_proiettata > 95:
        msg = "La tua selezione punta su numeri troppo alti. La somma prevista supera il limite aureo di 95."
        if severa: errori.append(("SOMMA ALTA", int(somma_proiettata), msg))
        else: avvisi.append(f"⚠️ Somma proiettata alta ({int(somma_proiettata)}).")

    return errori, avvisi

def genera_sistema(severa):
    clear_screen()
    titolo = "MODALITÀ SEVERA (STATISTICA RIGIDA)" if severa else "MODALITÀ FLESSIBILE (ADVISOR)"
    print(f"--- {titolo} ---")
    
    try:
        fissi = input("\nInserisci 2 numeri FISSI (es. 10 21): ").split()
        if len(fissi) != 2: raise ValueError("Servono 2 numeri fissi.")
        
        variabili = input("Inserisci 8 numeri VARIABILI: ").split()
        if len(variabili) != 8: raise ValueError("Servono 8 numeri variabili.")
        
        err, avv = analizza_numeri(fissi, variabili, severa)
        
        if err:
            for e in err: spiega_errore(e[0], e[1], e[2])
            print("\nGenerazione annullata. Correggi i numeri per ottimizzare le probabilità.")
            input("Premi Invio per tornare al menu...")
            return

        if avv:
            print("\n--- ⚠️ SUGGERIMENTI STATISTICI ---")
            for a in avv: print(a)
            cont = input("\nVuoi procedere comunque? (s/n): ")
            if cont.lower() != 's': return

        bonus = input("\nNumero Bonus (1-12): ")
        combinazioni = list(itertools.combinations(variabili, 3))
        
        nome_file = "sistema_export.txt"
        with open(nome_file, "w") as f:
            f.write(f"SISTEMA OTTIMIZZATO ({titolo})\n")
            f.write(f"Numeri: {sorted([int(x) for x in fissi+variabili])} | Bonus: {bonus}\n\n")
            for i, c in enumerate(combinazioni, 1):
                col = sorted(list(fissi) + list(c), key=int)
                f.write(f"Colonna {i:02d}: {' - '.join(map(str, col))} [B: {bonus}]\n")
        
        print(f"\n✅ Elaborazione completata! 56 colonne salvate in {nome_file}")
        input("Premi Invio...")

    except Exception as e:
        print(f"Errore: {e}")
        input("Premi Invio...")

def menu():
    while True:
        clear_screen()
        print("+" + "-"*40 + "+")
        print("|    LOTTO MATHEMATICAL ANALYZER v3.0    |")
        print("+" + "-"*40 + "+")
        print("| 1. Genera in MODALITÀ SEVERA           |")
        print("| 2. Genera in MODALITÀ FLESSIBILE       |")
        print("| 3. Documentazione & Best Practices     |")
        print("| 4. Esci                                |")
        print("+" + "-"*40 + "+")
        
        scelta = input("\nScelta > ")
        if scelta == '1': genera_sistema(severa=True)
        elif scelta == '2': genera_sistema(severa=False)
        elif scelta == '3':
            clear_screen()
            print("="*60)
            print(" DOCUMENTAZIONE TECNICA: PERCHÉ QUESTE REGOLE?")
            print("="*60)
            print("""
A. LA DISTRIBUZIONE NORMALE (GAUSS)
   In una lotteria 1-30, la somma dei 5 numeri estratti non è 
   casuale nel tempo. Si accumula attorno alla media (77.5). 
   Giocare una somma <60 o >95 significa scommettere su eventi 
   che accadono in meno del 15% dei casi.

B. LA LEGGE DELLA PARITÀ
   Le combinazioni 'tutti pari' o 'tutti dispari' sono outliers. 
   Mantenendo un equilibrio 5:5 nel tuo set da 10, forzi il 
   sistema a generare colonne che rispettano il trend 3:2 / 2:3.

C. EFFICIENZA COMBINATORIA
   Usando 56 colonne per 10 numeri, copriamo il 100% delle terzine 
   variabili. Se i 2 fissi sono corretti, hai 'imbrigliato' il 
   caso matematicamente.
            """)
            
            input("\nPremi Invio...")
        elif scelta == '4': break

if __name__ == "__main__":
    menu()
