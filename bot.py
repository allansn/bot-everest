
import os
import requests
from urllib.parse import quote

# Remove espaços e quebras de linha do token
TOKEN = "".join(os.environ["CLASH_API_TOKEN"].split())

CLAN_TAG = "#2JRP8G0U0"
API_URL = "https://cocproxy.royaleapi.dev/v1"

print("BOT EVEREST - Verificação")
print("Token carregado:", bool(TOKEN))
print("Tamanho do token:", len(TOKEN))
print("Contém espaços internos:", any(c.isspace() for c in TOKEN))
print("Formato JWT correto:", TOKEN.count(".") == 2)


def buscar_membros():
    url = f"{API_URL}/clans/{quote(CLAN_TAG, safe='')}\/members"
    url = url.replace("\\/", "/")

    resposta = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {TOKEN}"
        },
        timeout=30
    )

    if resposta.status_code != 200:
        print("Erro da API:", resposta.status_code)
        print("Detalhes:", resposta.text)
        raise SystemExit(1)

    membros = resposta.json().get("items", [])

    print(f"EVEREST™ - Total de membros: {len(membros)}")

    for membro in membros:
        print(
            membro.get("name"),
            membro.get("tag"),
            membro.get("role")
        )


if __name__ == "__main__":
    buscar_membros()
    
