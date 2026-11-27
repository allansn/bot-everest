
import os
import json
import requests
from pathlib import Path
from urllib.parse import quote

TOKEN = "".join(os.environ["CLASH_API_TOKEN"].split())
CLAN_TAG = "#2JRP8G0U0"
API_URL = "https://cocproxy.royaleapi.dev/v1"
ARQUIVO = Path("membros.json")


def buscar_membros():
    url = f"{API_URL}/clans/{quote(CLAN_TAG, safe='')}/members"

    resposta = requests.get(
        url,
        headers={"Authorization": f"Bearer {TOKEN}"},
        timeout=30
    )

    resposta.raise_for_status()

    membros = resposta.json().get("items", [])

    return {
        membro["tag"]: {
            "nome": membro.get("name"),
            "cargo": membro.get("role")
        }
        for membro in membros
    }


def carregar_historico():
    if ARQUIVO.exists():
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    return None


def salvar_historico(membros):
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(membros, arquivo, ensure_ascii=False, indent=2)


def main():
    atuais = buscar_membros()
    anteriores = carregar_historico()

    print("===== BOT EVEREST™ =====")
    print("Total de membros:", len(atuais))

    if anteriores is None:
        print("Primeira consulta: histórico inicial criado.")
        salvar_historico(atuais)
        return

    novos = atuais.keys() - anteriores.keys()
    saidas = anteriores.keys() - atuais.keys()

    for tag in novos:
        print("NOVO MEMBRO:", atuais[tag]["nome"], tag)

    for tag in saidas:
        print("SAIU DO CLÃ:", anteriores[tag]["nome"], tag)

    for tag in atuais.keys() & anteriores.keys():
        cargo_antigo = anteriores[tag]["cargo"]
        cargo_novo = atuais[tag]["cargo"]

        if cargo_antigo != cargo_novo:
            print(
                "MUDANÇA DE CARGO:",
                atuais[tag]["nome"],
                cargo_antigo,
                "->",
                cargo_novo
            )

    if not novos and not saidas:
        print("Nenhuma entrada ou saída detectada.")

    salvar_historico(atuais)


if __name__ == "__main__":
    main()
    
