import os
import requests
from urllib.parse import quote

TOKEN = os.environ["CLASH_API_TOKEN"]
CLAN_TAG = "#2JRP8G0U0"
API_URL = "https://cocproxy.royaleapi.dev/v1"

def buscar_membros():
    url = f"{API_URL}/clans/{quote(CLAN_TAG, safe='')}/members"

    resposta = requests.get(
        url,
        headers={"auth": TOKEN},
        timeout=30
    )

    if resposta.status_code != 200:
        print("Erro da API:", resposta.status_code)
        print("Detalhes:", resposta.text)
        return

    membros = resposta.json().get("items", [])
    print(f"EVEREST™ - Total de membros: {len(membros)}")

    for membro in membros:
        print(membro.get("name"), membro.get("tag"), membro.get("role"))

if __name__ == "__main__":
    buscar_membros()
