import json
import requests
import re

def get_domains(pastebin_url):
    """
    Recupera il contenuto del Pastebin con i link completi e li pulisce.
    :param pastebin_url: URL del Pastebin da cui recuperare i link.
    :return: Lista dei link senza 'www.' e senza '/' finale.
    """
    try:
        response = requests.get(pastebin_url)
        response.raise_for_status()
        # Pulisce i link: rimuove spazi, '\r', '/' finale e 'www.'
        domains = [clean_url(line) for line in response.text.strip().split('\n')]
        return domains
    except requests.RequestException as e:
        print(f"Errore durante il recupero dei link: {e}")
        return []

def clean_url(url):
    """
    Pulisce un URL rimuovendo il 'www.' e lo slash finale.
    :param url: URL da pulire.
    :return: URL pulito.
    """
    url = url.strip().replace('\r', '').rstrip('/')  # Rimuove spazi e '/' finale
    url = re.sub(r'^https?://www\.', 'https://', url)  # Rimuove 'www.' se presente
    return url

def update_json_file():
    """
    Aggiorna il file JSON con i link completi (senza 'www.' e senza slash finale).
    """
    # Carica il file JSON
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Errore: Il file config.json non è stato trovato.")
        return
    except json.JSONDecodeError:
        print("Errore: Il file config.json non è un JSON valido.")
        return

    # URL dei Pastebin
    streamingcommunity_url = 'https://pastebin.com/raw/KgQ4jTy6'
    general_pastebin_url = 'https://pastebin.com/raw/E8WAhekV'

    # Recupera i link dai Pastebin
    streamingcommunity_links = get_domains(streamingcommunity_url)
    general_links = get_domains(general_pastebin_url)

    if not streamingcommunity_links or not general_links:
        print("Lista dei link vuota. Controlla i link di Pastebin.")
        return

    # Mappatura siti da aggiornare con i link completi
    site_mapping = {
        'StreamingCommunity': streamingcommunity_links[0],
        'Filmpertutti': general_links[1],
        'Tantifilm': general_links[2],
        'LordChannel': general_links[3],
        'StreamingWatch': general_links[4],
        'CB01': general_links[5],
        'DDLStream': general_links[6],
        'Guardaserie': general_links[7],
        'GuardaHD': general_links[8],
        'AnimeWorld': general_links[9],
        'SkyStreaming': general_links[10],
       # 'DaddyLiveHD': general_links[11],  # Commentato come nell'originale
    }

    # Aggiorna il file JSON
    for site_key, full_url in site_mapping.items():
        if site_key in data['Siti']:
            data['Siti'][site_key]['url'] = full_url  # Usa 'url' invece di 'domain'
            print(f"Aggiornato {site_key}: {full_url}")  # Debug

    # Salva il JSON aggiornato
    try:
        with open('config.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        print("File config.json aggiornato con successo!")
    except Exception as e:
        print(f"Errore durante il salvataggio del file JSON: {e}")

if __name__ == '__main__':
    update_json_file()
