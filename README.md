# 🧠 KernelLab 

**KernelLab** è uno strumento da riga di comando in Python progettato per fornire un'interfaccia minimalista, potente e modulare per l'analisi del kernel Linux, in particolare su distribuzioni come **Arch Linux**.  
Il progetto nasce come un laboratorio personale per esplorare, monitorare e comprendere il comportamento del kernel — il cuore del sistema operativo.

---

## 🔍 Panoramica

KernelLab è pensato per ambienti **minimalisti**, come installazioni Arch senza GUI o sistemi embedded, in cui i tool grafici non sono disponibili. Ti consente di:

- 🧾 Leggere e filtrare i log del kernel
- 🛠 Analizzare i moduli caricati (`lsmod`, `modinfo`)
- 🧠 Classificare e formattare i messaggi (`ERROR`, `WARNING`, `INFO`)
- ⚡ Avere un'interfaccia testuale leggibile e migliorata con [Rich](https://github.com/Textualize/rich)
- 📚 Estendere facilmente le funzionalità con nuovi comandi modulari

---

## 📂 Struttura del Progetto
\`\`\`
KernelLab/
├── main.py
├── core/
│ ├── log_parser.py
│ └── module_inspector.py
├── logs/
├── README.md
├── requirements.txt
└── .venv/             
\`\`\`
---

## ⚙️ Funzionalità

### ✅ Log del kernel
- Lettura dei log tramite `dmesg` o `journalctl -k`
- Fallback automatico: se non hai i permessi per `dmesg`, passa a `journalctl`
- Supporto per parsing e classificazione log
- Evidenziazione semantica (colore, livello)

### ✅ Parsing avanzato (`parse_log_lines`)
- Estrae: `timestamp`, `livello`, `messaggio`
- Classifica: `ERROR`, `WARNING`, `INFO`, personalizzabile
- Uscita strutturata come dizionario (utile per interfacce)

### 🚧 Moduli Kernel *(in sviluppo)*
- Elenco dei moduli caricati (`lsmod`)
- Informazioni dettagliate sui moduli (`modinfo`)
- Parsing dipendenze, dimensioni, utilizzi
- (Planned) Caricamento/rimozione dinamica (`modprobe`, `rmmod`)

### 🧪 Interfaccia testuale (TUI) *(in sviluppo)*
- Con librerie come `Textual`, `Rich Console`, o `urwid`
- Navigazione interattiva tra log, moduli, messaggi critici

---

## 🐍 Requisiti

- Linux (consigliato: Arch, Manjaro, Artix)
- Python 3.10+
- Accesso a `dmesg` **oppure** `journalctl`
- Pacchetti Python:

```bash
pip install -r requirements.txt
