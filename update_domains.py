import json
import requests

def get_domains(pastebin_url):
    """
    Recupera il contenuto del Pastebin con i domini.
    :param pastebin_url: URL del Pastebin da cui recuperare i domini.
    :return: Lista degli URL (senza slash finale).
    """
    try:
        response = requests.get(pastebin_url)
        response.raise_for_status()
        domains = response.text.strip().split('\n')
        domains = [domain.strip().replace('\r', '').rstrip('/') for domain in domains]  # Rimuove \r e lo slash finale
        return domains
    except requests.RequestException as e:
        print(f"Errore durante il recupero dei domini: {e}")
        return []

def update_json_file():
    """
    Aggiorna il file JSON con gli URL completi recuperati da Pastebin.
    """
    # Carica il file JSON che vuoi aggiornare
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Errore: Il file config.json non è stato trovato.")
        return
    except json.JSONDecodeError:
        print("Errore: Il file config.json non è un JSON valido.")
        return

    # Ottieni gli URL per StreamingCommunity da un Pastebin specifico
    streamingcommunity_url = 'https://pastebin.com/raw/KgQ4jTy6'
    streamingcommunity_domains = get_domains(streamingcommunity_url)

    # Ottieni gli URL per gli altri siti dal Pastebin generale
    general_pastebin_url = 'https://pastebin.com/raw/E8WAhekV'
    general_domains = get_domains(general_pastebin_url)

    if not general_domains or not streamingcommunity_domains:
        print("Lista degli URL vuota. Controlla i link di Pastebin.")
        return

    # Mappatura dei siti da aggiornare
    site_mapping = {
        'StreamingCommunity': streamingcommunity_domains[0],  # Dominio specifico per StreamingCommunity
        'Filmpertutti': general_domains[1],                  # Secondo dominio
        'Tantifilm': general_domains[2],                     # Terzo dominio
        'LordChannel': general_domains[3],                   # Quarto dominio
        'StreamingWatch': general_domains[4],                # Quinto dominio
        'CB01': general_domains[5],                          # Sesto dominio
        'DDLStream': general_domains[6],                     # Settimo dominio
        'Guardaserie': general_domains[7],                   # Ottavo dominio
        'GuardaHD': general_domains[8],                      # Nono dominio
        'AnimeWorld': general_domains[9],                    # Decimo dominio
        'SkyStreaming': general_domains[10],                 # Undicesimo dominio
        'DaddyLiveHD': general_domains[11],                  # Dodicesimo dominio
    }

    # Aggiorna il file JSON con gli URL completi
    for site_key, full_url in site_mapping.items():
        if site_key in data['Siti']:
            data['Siti'][site_key]['url'] = full_url  # Usa "url" invece di "domain"
            print(f"Aggiornato {site_key}: {full_url}")  # Messaggio di debug

    # Scrivi il file JSON aggiornato
    try:
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("File config.json aggiornato con successo!")
    except Exception as e:
        print(f"Errore durante il salvataggio del file JSON: {e}")

if __name__ == '__main__':
    update_json_file()
