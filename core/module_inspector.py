# core/module_inspector.py
import subprocess

def list_loaded_modules():
    """
    Restituisce un elenco dei moduli attualmente caricati usando 'lsmod'.
    Output: lista di dizionari con 'name', 'size', 'used_by'
    """
    try:
        result = subprocess.check_output(['lsmod'], text=True).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"[!] Errore nell'esecuzione di lsmod: {e}")
        return []

    modules = []
    for line in result[1:]:  
        parts = line.split()
        if len(parts) >= 3:
            modules.append({
                'name': parts[0],
                'size': parts[1],
                'used_by': parts[2]
            })

    return modules


def get_module_info(module_name):
    """
    Restituisce informazioni dettagliate su un modulo specifico usando 'modinfo'.
    Output: dizionario con chiavi come filename, license, description, depends...
    """
    try:
        output = subprocess.check_output(['modinfo', module_name], text=True).splitlines()
    except subprocess.CalledProcessError as e:
        print(f"[!] Impossibile ottenere informazioni per il modulo '{module_name}': {e}")
        return {}

    info = {}
    for line in output:
        if ':' in line:
            key, value = line.split(':', 1)
            info[key.strip()] = value.strip()
    return info


def print_module_summary(module):
    """
    Stampa in formato leggibile le info base di un modulo (da lsmod).
    """
    print(f"- {module['name']} | Size: {module['size']} | Used by: {module['used_by']}")


def print_module_info(info_dict):
    """
    Stampa info dettagliate su un modulo da 'modinfo'.
    """
    print("\n[+] Dettagli modulo:")
    for key, value in info_dict.items():
        print(f"{key:<15}: {value}")

