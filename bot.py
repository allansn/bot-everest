
import os
import json
import requests
from pathlib import Path
from urllib.parse import quote
from datetime import datetime

TOKEN = "".join(os.environ["CLASH_API_TOKEN"].split())
CLAN_TAG = "#2JRP8G0U0"
API_URL = "https://cocproxy.royaleapi.dev/v1"

ARQUIVO = Path("membros.json")
ALERTAS = Path("alertas_whatsapp.txt")


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
    mensagens = []

    print("===== BOT EVEREST™ =====")
    print("Total de membros:", len(atuais))

    if anteriores is None:
        print("Histórico inicial criado.")
        salvar_historico(atuais)
        ALERTAS.write_text(
            "BOT EVEREST™\nPrimeira consulta realizada. "
            "Histórico inicial criado.",
            encoding="utf-8"
        )
        return

    novos = atuais.keys() - anteriores.keys()
    saidas = anteriores.keys() - atuais.keys()

    for tag in novos:
        nome = atuais[tag]["nome"]
        mensagens.append(
            f"🟢 NOVO MEMBRO NO EVEREST™\n"
            f"Jogador: {nome}\nTag: {tag}"
        )

    for tag in saidas:
        nome = anteriores[tag]["nome"]
        mensagens.append(
            f"🔴 MEMBRO SAIU DO EVEREST™\n"
            f"Jogador: {nome}\nTag: {tag}"
        )

    for tag in atuais.keys() & anteriores.keys():
        antigo = anteriores[tag]["cargo"]
        novo = atuais[tag]["cargo"]

        if antigo != novo:
            mensagens.append(
                f"⚔️ MUDANÇA DE CARGO - EVEREST™\n"
                f"Jogador: {atuais[tag]['nome']}\n"
                f"Cargo anterior: {antigo}\n"
                f"Novo cargo: {novo}"
            )

    if not mensagens:
        mensagens.append(
            "✅ EVEREST™\nNenhuma entrada, saída ou mudança de cargo."
        )

    relatorio = (
        "📢 RELATÓRIO DO EVEREST™\n"
        f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        f"Total de membros: {len(atuais)}\n\n"
        + "\n\n".join(mensagens)
    )

    print("\n" + relatorio)

    ALERTAS.write_text(relatorio, encoding="utf-8")
    salvar_historico(atuais)


if __name__ == "__main__":
    main()
