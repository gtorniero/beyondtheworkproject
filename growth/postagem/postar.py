#!/usr/bin/env python3
"""Publicador automático das redes da Beyond the Work (Retrozap, Quiddo e SPORT DNA).

Lê a agenda aprovada no branch `social` (packs/<pack>/agenda.csv, STATUS.json,
<marca>/LEGENDAS.txt e manifest.json) e publica no Instagram e no Facebook pela
Graph API v23.0. Rode sempre com `python3 -I`.

  python3 -I growth/postagem/postar.py --dry-run
  python3 -I growth/postagem/postar.py --dry-run --quando 2026-11-16T23:59 --janela 1440 --checar-midia
  python3 -I growth/postagem/postar.py --executar
  python3 -I growth/postagem/postar.py --cobertura 2026-11-15:2026-12-06

O token da Meta é injetado pelo proxy de rede em graph.facebook.com. O token de
página é pedido em tempo de execução e fica só na memória: nunca é impresso,
gravado ou enviado a outro host que não seja da Meta.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import difflib
import fcntl
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

AQUI = Path(__file__).resolve().parent
REPO = AQUI.parents[1]
LOG = AQUI / "publicados.json"
TRAVA = AQUI / ".postar.lock"
SEM_FACEBOOK = Path(__file__).with_name("sem_facebook.json")
SEGURAR = AQUI / "segurar.json"
GRAPH = "https://graph.facebook.com/v23.0"
DONO_REPO = "gtorniero/beyondtheworkproject"
RAW = f"https://raw.githubusercontent.com/{DONO_REPO}/"
RAW_SOCIAL = RAW + "social/"
BRANCH_CONTEUDO = "social"
REF_CONTEUDO = "refs/remotes/origin/social"
BRT = ZoneInfo("America/Sao_Paulo")
ANTECIPAR_MIN = 15          # publica até 15 min antes do horário marcado
JANELA_PADRAO = 30          # e pega o que venceu nos últimos 30 min
JANELA_STORY_MANUAL_H = 3   # story não registrado nas 3 h antes do horário = já postado à mão
ESPERA_REEL_S = 900         # tempo máximo de processamento de vídeo
COTA_MINIMA = 5             # vagas livres na cota de 100 posts/24 h do Instagram

MARCAS = {
    "retrozap": {"nome": "Retrozap", "pasta": "retrozap", "page": "1481891254996380",
                 "ig": "17841471888314332", "usuario": "retrozap.app"},
    "quiddo": {"nome": "Quiddo", "pasta": "quiddo", "page": "1336804232858527",
               "ig": "17841425670576940", "usuario": "quiddo.app"},
    "sportdna": {"nome": "SPORT DNA", "pasta": "sportdna", "page": "1460739327115922",
                 "ig": "17841468452613351", "usuario": "sportdna.app"},
}
FORMATOS = {"story": "story", "stories": "story", "reel": "reel", "reels": "reel",
            "carrossel": "carrossel", "carousel": "carrossel"}
PLATAFORMAS = ("instagram", "facebook")


def chave_marca(nome: str) -> str | None:
    k = re.sub(r"[^a-z]", "", nome.lower())
    return k if k in MARCAS else None


# --------------------------------------------------------------------------- utilidades

def agora() -> dt.datetime:
    return dt.datetime.now(BRT)


def iso(t: dt.datetime | None) -> str:
    return t.astimezone(BRT).isoformat(timespec="seconds") if t else ""


def hm(t: dt.datetime) -> str:
    return t.astimezone(BRT).strftime("%d/%m %Hh%M")


def oculta_segredos(texto: str) -> str:
    """Tira qualquer token de mensagens de erro (URLs com access_token, cabeçalhos)."""
    texto = re.sub(r"(access_token=)[^&\s'\"]+", r"\1***", str(texto))
    texto = re.sub(r"(OAuth|Bearer)\s+[A-Za-z0-9._\-]+", r"\1 ***", texto)
    return re.sub(r"EA[A-Za-z0-9]{30,}", "***", texto)


def normaliza(texto: str) -> str:
    """Primeira linha sem emoji, pontuação, acento ou caixa, para comparar legendas."""
    linha = (texto or "").strip().split("\n")[0]
    linha = unicodedata.normalize("NFKD", linha)
    linha = "".join(c for c in linha if not unicodedata.combining(c))
    linha = re.sub(r"[^0-9a-zA-Z ]+", " ", linha).lower()
    return re.sub(r"\s+", " ", linha).strip()


def parece(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, normaliza(a), normaliza(b)).ratio()


def git(*args: str, check: bool = True) -> str:
    r = subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {r.stderr.strip()[:400]}")
    return r.stdout


# --------------------------------------------------------------------------- conteúdo do branch social

class Conteudo:
    """Leitura do branch social sempre na versão mais nova (git fetch a cada execução)."""

    def __init__(self, buscar: bool = True):
        self.avisos: list[str] = []
        if buscar:
            ok = False
            for tentativa in range(3):
                r = subprocess.run(["git", "-C", str(REPO), "fetch", "origin",
                                    f"+refs/heads/{BRANCH_CONTEUDO}:{REF_CONTEUDO}"],
                                   capture_output=True, text=True)
                if r.returncode == 0:
                    ok = True
                    break
                time.sleep(2 * 2 ** tentativa)
            if not ok:
                self.avisos.append("git fetch do branch social falhou; usando a cópia local (pode estar velha)")
        self.sha = git("rev-parse", REF_CONTEUDO).strip()
        self.arquivos = set(git("ls-tree", "-r", "--name-only", REF_CONTEUDO, "packs/").split())
        # id do conteúdo de cada arquivo (blob do git): mesmo id = mesmo arquivo, com qualquer nome
        self.blob: dict[str, str] = {}
        for l in git("ls-tree", "-r", REF_CONTEUDO, "packs/").splitlines():
            meta, _, cam = l.partition("\t")
            partes = meta.split()
            if len(partes) == 3 and partes[1] == "blob":
                self.blob[cam] = partes[2]
        self._cache: dict[str, str] = {}
        self._virtual_sequencias()

    def _virtual_sequencias(self) -> None:
        """packs/STORIES-SEQ (17/11): cada story vira 2 ou 3 quadros postados em sequência no mesmo horário.
        Viram linhas de agenda comuns com peça "<PECA>.<quadro>" (ex.: Q-S8.2). Quadro sem link (o 1 do
        Retrozap e da SPORT DNA) é o story do pack da semana, que já está na agenda normal."""
        base = "packs/STORIES-SEQ"
        fonte = f"{base}/agenda-sequencias.csv"
        if fonte not in self.arquivos:
            return
        try:
            st = json.loads(self.texto(f"{base}/STATUS.json") or "{}")
        except json.JSONDecodeError:
            st = {}
            self.avisos.append("STORIES-SEQ: STATUS.json ilegível; nenhum quadro de sequência sai")
        st_peca = {x.get("peca"): x for x in st.get("pecas", [])}
        linhas = list(csv.DictReader(io.StringIO(self.texto(fonte) or "")))
        com_q1 = {(l.get("marca"), l.get("peca")) for l in linhas if (l.get("quadro") or "").strip() == "1"
                  and (l.get("link") or "").strip()}
        out = io.StringIO()
        w = csv.writer(out)
        w.writerow(["data", "hora", "marca", "formato", "peca", "versao", "como", "arquivos", "links",
                    "adesivo", "titulo", "quadro", "anterior"])
        pecas = []
        for l in linhas:
            q = (l.get("quadro") or "").strip()
            link = (l.get("link") or "").strip()
            if not q.isdigit() or not link:
                continue
            peca, n = (l.get("peca") or "").strip(), int(q)
            if n == 1:
                anterior = ""
            elif n == 2:
                anterior = f"{peca}.1" if (l.get("marca"), peca) in com_q1 else peca
            else:
                anterior = f"{peca}.{n - 1}"
            nome = f"{peca}.{n}"
            w.writerow([l.get("data", ""), l.get("hora", ""), l.get("marca", ""), "story", nome, f"SEQ-{nome}-v1",
                        "sequência", l.get("arquivo", ""), link, "", l.get("titulo", ""), n, anterior])
            ref = st_peca.get(peca, {})
            pecas.append({"peca": nome, "versao": f"SEQ-{nome}-v1", "liberado": ref.get("liberado") is True,
                          "status_mesa": ref.get("status_mesa", "fora do STATUS.json da STORIES-SEQ")})
        self._cache[f"{base}/agenda.csv"] = out.getvalue()
        self._cache[f"{base}/STATUS.json"] = json.dumps({"pack": "STORIES-SEQ", "pecas": pecas})
        self.arquivos |= {f"{base}/agenda.csv", f"{base}/STATUS.json"}

    def texto(self, caminho: str) -> str | None:
        if caminho not in self.arquivos:
            return None
        if caminho not in self._cache:
            self._cache[caminho] = git("show", f"{REF_CONTEUDO}:{caminho}").lstrip("﻿")
        return self._cache[caminho]

    def bytes(self, caminho: str) -> bytes:
        return subprocess.run(["git", "-C", str(REPO), "show", f"{REF_CONTEUDO}:{caminho}"],
                              capture_output=True, check=True).stdout

    def packs(self) -> list[str]:
        ps = {p.split("/")[1] for p in self.arquivos if re.fullmatch(r"packs/[^/]+/agenda\.csv", p)}
        return sorted(ps)


def peca_da_versao(versao: str) -> str:
    v = re.sub(r"^(S\d+|X)-", "", versao.strip())
    return re.sub(r"-v\d+$", "", v)


def le_legendas(texto: str | None) -> dict[str, dict]:
    """LEGENDAS.txt -> {versao: {peca, cabecalho, legenda, arquivos, audio, notas}}."""
    blocos: dict[str, dict] = {}
    if not texto:
        return blocos
    for bloco in re.split(r"\n-{10,}\s*\n", texto.replace("\r\n", "\n")):
        linhas = bloco.strip("\n").split("\n")
        # "S03-Q-R8-v2 · …", "X-D-RX3-v2 · …" ou, desde 18/11, sem prefixo de pack: "QE-R1-v3 · …"
        idx = next((i for i, l in enumerate(linhas) if re.match(r"^(?:(?:S\d+|X)-)?[A-Z][A-Za-z0-9.]*-[A-Za-z0-9.-]*-v\d+\s+·", l)), None)
        if idx is None:
            continue
        cab = linhas[idx]
        versao = cab.split("·")[0].strip()
        corpo = "\n".join(linhas[idx + 1:])
        legenda = None
        m = re.search(r"(?m)^LEGENDA\s*\n(.*)", corpo, re.S)
        if m:
            leg = m.group(1)
            leg = re.split(r"\n\s*\nNotas:|\nNotas:", leg)[0]
            legenda = leg.strip()
        arq = re.search(r"(?m)^Arquivos:\s*(.*)$", corpo)
        audio = re.search(r"(?m)^Áudio:\s*(.*)$", corpo)
        notas = re.search(r"(?m)^Notas:\s*(.*)$", corpo)
        blocos[versao] = {"peca": peca_da_versao(versao), "cabecalho": cab, "legenda": legenda,
                          "arquivos": arq.group(1).strip() if arq else "",
                          "audio": audio.group(1).strip() if audio else "",
                          "notas": notas.group(1).strip() if notas else ""}
    return blocos


def le_data(celula: str) -> dt.date | None:
    m = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", celula or "")
    return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None


def le_hora(celula: str) -> dt.time | None:
    m = re.fullmatch(r"\s*(\d{1,2})\s*h\s*(\d{2})?\s*", (celula or "").lower())
    return dt.time(int(m.group(1)), int(m.group(2) or 0)) if m else None


def caminho_do_link(url: str) -> str | None:
    if url.startswith(RAW_SOCIAL):
        return url[len(RAW_SOCIAL):]
    return None


def numero_final(nome: str) -> int:
    m = re.search(r"-(\d+)\.[a-z0-9]+$", nome)
    return int(m.group(1)) if m else 0


def carrega_agenda(cont: Conteudo, fixar_sha: bool = True) -> list[dict]:
    """Todas as linhas de todas as agendas, já com aprovação, legenda, mídia e problemas."""
    itens: list[dict] = []
    for pack in cont.packs():
        base = f"packs/{pack}"
        agenda_txt = cont.texto(f"{base}/agenda.csv") or ""
        try:
            status = json.loads(cont.texto(f"{base}/STATUS.json") or "{}")
        except json.JSONDecodeError:
            status = {}
            cont.avisos.append(f"{pack}: STATUS.json ilegível; nada do pack será publicado")
        try:
            manifest = json.loads(cont.texto(f"{base}/manifest.json") or "{}")
        except json.JSONDecodeError:
            manifest = {}
            cont.avisos.append(f"{pack}: manifest.json ilegível")
        st_versao = {(p.get("peca"), p.get("versao")): p for p in status.get("pecas", [])}
        st_peca: dict[str, list[dict]] = {}
        for p in status.get("pecas", []):
            st_peca.setdefault(p.get("peca"), []).append(p)
        man_peca: dict[str, list[dict]] = {}
        for p in manifest.get("pieces", []):
            man_peca.setdefault(p.get("id"), []).append(p)
        legendas = {k: le_legendas(cont.texto(f"{base}/{m['pasta']}/LEGENDAS.txt")) for k, m in MARCAS.items()}

        for n, linha in enumerate(csv.DictReader(io.StringIO(agenda_txt)), start=2):
            linha = {k.strip(): (v or "").strip() for k, v in linha.items() if k}
            it = {"pack": pack, "linha": n, "peca": linha.get("peca", ""), "versao": linha.get("versao", ""),
                  "marca_txt": linha.get("marca", ""), "formato_txt": linha.get("formato", ""),
                  "data_txt": linha.get("data", ""), "hora_txt": linha.get("hora", ""),
                  "como": linha.get("como", ""), "titulo": linha.get("titulo", ""),
                  "adesivo": linha.get("adesivo", ""), "problemas": [], "avisos": [], "conteudo": [],
                  "reserva": False, "aprovado": False, "legenda": None, "legenda_fonte": "",
                  "midia": {}, "links": linha.get("links", "").split(),
                  "quadro": int(linha["quadro"]) if (linha.get("quadro") or "").isdigit() else 0,
                  "anterior": linha.get("anterior", "")}
            it["marca"] = chave_marca(it["marca_txt"])
            it["formato"] = FORMATOS.get(it["formato_txt"].lower())
            data, hora = le_data(it["data_txt"]), le_hora(it["hora_txt"])
            it["quando"] = dt.datetime.combine(data, hora, BRT) if data and hora else None
            it["data"] = data
            if not it["marca"]:
                it["problemas"].append(f"marca desconhecida: {it['marca_txt']!r}")
            if not it["formato"]:
                it["problemas"].append(f"formato desconhecido: {it['formato_txt']!r}")
            if data is None:
                it["problemas"].append(f"data ilegível: {it['data_txt']!r}")
            if "reserva" in (it["hora_txt"] + " " + it["como"]).lower():
                it["reserva"] = True
            elif hora is None:
                it["problemas"].append(f"hora ilegível: {it['hora_txt']!r}")

            # aprovação na Mesa (STATUS.json), na versão exata da agenda
            st = st_versao.get((it["peca"], it["versao"]))
            if st is None:
                outras = [p.get("versao") for p in st_peca.get(it["peca"], [])]
                it["problemas"].append("peça fora do STATUS.json" if not outras else
                                       f"versão {it['versao']} não está no STATUS.json (lá: {', '.join(str(x) for x in outras)})")
            else:
                it["status"] = st
                it["rotulo_ia"] = st.get("rotulo_ia") is True
                if "reserva" in (st.get("uso") or "").lower():
                    it["reserva"] = True
                # aceita "aprovado" puro ou com nota entre parênteses, ex.: "aprovado (música de banco, 15/11)"
                it["aprovado"] = st.get("liberado") is True and bool(
                    re.fullmatch(r"aprovado(\s*\(.*\)|\s*·.*)?", (st.get("status_mesa") or "").strip().lower(), re.S))
                # "aprovado · RESERVA: se a sequência ... for liberada, posta a sequência e NÃO este" (17/11)
                it["cede_para_sequencia"] = bool(re.search(r"sequ[êe]ncia", st.get("status_mesa") or "", re.I)
                                                 and re.search(r"reserva", st.get("status_mesa") or "", re.I))
                if not it["aprovado"]:
                    it["problemas"].append(f"não aprovado (liberado={st.get('liberado')}, "
                                           f"status_mesa={st.get('status_mesa')})")

            # legenda: LEGENDAS.txt da marca (versão exata); depois mesma peça; depois manifest
            if it["formato"] in ("reel", "carrossel") and it["marca"]:
                blocos = legendas[it["marca"]]
                b = blocos.get(it["versao"])
                if b and b["legenda"]:
                    it["legenda"], it["legenda_fonte"] = b["legenda"], f"{base}/{MARCAS[it['marca']]['pasta']}/LEGENDAS.txt ({it['versao']})"
                else:
                    alt = [x for v, x in blocos.items() if x["peca"] == it["peca"] and x["legenda"]]
                    if alt:
                        x = alt[-1]
                        it["legenda"] = x["legenda"]
                        it["legenda_fonte"] = f"LEGENDAS.txt ({x['cabecalho'].split('·')[0].strip()})"
                        it["avisos"].append(f"legenda tirada do bloco {x['cabecalho'].split('·')[0].strip()} "
                                            f"(a {it['versao']} não tem bloco próprio no LEGENDAS.txt)")
                    else:
                        man = [p for p in man_peca.get(it["peca"], []) if p.get("caption")]
                        man_ex = [p for p in man if p.get("version") == it["versao"]] or man
                        if man_ex:
                            it["legenda"] = man_ex[-1]["caption"].strip()
                            it["legenda_fonte"] = f"manifest.json ({man_ex[-1].get('version')})"
                            it["avisos"].append("legenda tirada do manifest.json (não achei no LEGENDAS.txt)")
                        else:
                            it["problemas"].append("sem legenda no LEGENDAS.txt nem no manifest.json")
                man = [p for p in man_peca.get(it["peca"], []) if p.get("caption")]
                if it["legenda"] and man and it["legenda_fonte"].startswith(("packs/", "LEGENDAS")):
                    if re.sub(r"\s+", " ", man[-1]["caption"]).strip() != re.sub(r"\s+", " ", it["legenda"]).strip():
                        it["avisos"].append("legenda do LEGENDAS.txt difere do manifest.json (vale o LEGENDAS.txt)")
                if it["legenda"]:
                    tira_aviso_ia(it)
                    tira_avisos_ficcao(it)
                # rede de segurança: LEGENDAS.txt diz voz de IA e o STATUS.json não marcou o rótulo
                info = " ".join(f"{x.get('audio', '')} {x.get('notas', '')}" for x in
                                [b] + [x for x in blocos.values() if x["peca"] == it["peca"]] if x)
                if not it.get("rotulo_ia") and re.search(r"voz (de|gerada por) IA|narração.{0,20}\bIA\b", info, re.I):
                    it["rotulo_ia"] = True
                    it["avisos"].append("rótulo de IA ligado pelo LEGENDAS.txt (voz de IA; faltava rotulo_ia no STATUS.json)")
                    verifica_legenda(it)

            # mídia
            arquivos_ok = True
            caminhos = []
            for url in it["links"]:
                cam = caminho_do_link(url)
                if not cam:
                    it["problemas"].append(f"link fora do branch social: {url}")
                    arquivos_ok = False
                elif cam not in cont.arquivos:
                    it["problemas"].append(f"arquivo não existe no branch social: {cam}")
                    arquivos_ok = False
                else:
                    caminhos.append(cam)
            if not it["links"]:
                it["problemas"].append("linha sem links de mídia")
            url_api = (lambda c: f"{RAW}{cont.sha}/{c}") if fixar_sha else (lambda c: RAW_SOCIAL + c)
            if arquivos_ok and it["formato"]:
                monta_midia(it, caminhos, url_api)
                md = it.get("midia") or {}
                principais = ([md.get("video")] if md.get("tipo") == "video" else
                              [md.get("imagem")] if md.get("tipo") == "imagem" else list(md.get("imagens") or []))
                it["blobs"] = [cont.blob[c] for c in principais if c and c in cont.blob]
            itens.append(it)
    return itens


def monta_midia(it: dict, caminhos: list[str], url_api) -> None:
    fmt = it["formato"]
    img = [c for c in caminhos if re.search(r"\.(png|jpe?g)$", c, re.I)]
    vid = [c for c in caminhos if c.lower().endswith((".mp4", ".mov"))]
    if fmt == "reel":
        principal = [c for c in vid if not c.lower().endswith("-so-voz.mp4")]
        capa = [c for c in img if re.search(r"-capa\.(png|jpe?g)$", c, re.I)]
        if len(principal) != 1:
            it["problemas"].append(f"reel precisa de 1 vídeo principal (achei {len(principal)})")
            return
        it["midia"] = {"tipo": "video", "video": principal[0], "capa": capa[0] if capa else None}
        if not capa:
            it["avisos"].append("reel sem capa (-capa.png); o Instagram usa o 1º quadro")
    elif fmt == "story":
        if len(img) + len(vid) != 1:
            it["problemas"].append(f"story precisa de 1 arquivo (achei {len(img) + len(vid)})")
            return
        it["midia"] = {"tipo": "imagem", "imagem": img[0]} if img else {"tipo": "video", "video": vid[0]}
    elif fmt == "carrossel":
        if vid:
            it["problemas"].append("carrossel com vídeo não é suportado por este script")
            return
        ordem = sorted(img, key=numero_final)
        if not 2 <= len(ordem) <= 10:
            it["problemas"].append(f"carrossel precisa de 2 a 10 imagens (achei {len(ordem)})")
            return
        nums = [numero_final(c) for c in ordem]
        if nums != list(range(1, len(ordem) + 1)):
            it["avisos"].append(f"numeração das páginas fora de ordem: {nums}")
        it["midia"] = {"tipo": "carrossel", "imagens": ordem}
    it["urls"] = {k: (url_api(v) if isinstance(v, str) else [url_api(x) for x in v])
                  for k, v in it["midia"].items() if k != "tipo" and v}


def rotulo_ia(it: dict, params: dict) -> dict:
    """Peça com "rotulo_ia": true no STATUS.json sai com o rótulo "Informações de IA" da Meta
    (is_ai_generated no container; não dá para pôr depois de publicado). Regra do Gui, 17/11."""
    if it.get("rotulo_ia"):
        return dict(params, is_ai_generated="true")
    return params


FICCAO = (r"simula[çc][ãa]o|simulad[oa]s? com|nomes? de exemplo|dados de exemplo|conversa de exemplo|grupo de exemplo|"
          r"fict[íi]ci[oa]s?|feit[oa] (?:com|por) (?:a )?IA|gerad[oa] (?:com|por) (?:a )?IA|ilustrativ[oa]")


def tira_avisos_ficcao(it: dict) -> None:
    """Regra do Gui (17/11): legenda NUNCA diz que é exemplo, simulação, fictício ou feito por IA.
    Tira parênteses com esses avisos e linhas que são só o aviso."""
    leg = it["legenda"]
    nova = re.sub(r"[ \t]*\([^()\n]*\b(?:" + FICCAO + r")[^()\n]*\)\.?", "", leg, flags=re.I)
    linhas = [l for l in nova.split("\n")
              if not re.fullmatch(r"\s*[^\w\n]{0,3}\s*(?:" + FICCAO + r")[^\n]{0,60}", l, re.I)]
    nova = re.sub(r"\n{3,}", "\n\n", "\n".join(l.rstrip() for l in linhas)).strip()
    if nova != leg:
        it["legenda"] = nova
        it["avisos"].append("aviso de exemplo/simulação tirado da legenda (regra do Gui, 17/11)")


def tira_aviso_ia(it: dict) -> None:
    """Regra do Gui (16/11): legenda não leva aviso de voz de IA. Se o LEGENDAS.txt trouxer, sai aqui."""
    nova = re.sub(r"\n?[^\n]*voz (de|gerada por) IA[^\n]*", "", it["legenda"]).strip()
    if nova != it["legenda"]:
        it["legenda"] = re.sub(r"\n{3,}", "\n\n", nova)
        it["avisos"].append("aviso de voz de IA tirado da legenda (regra do Gui, 16/11)")


def verifica_legenda(it: dict) -> None:
    """Regras de conteúdo. Problema aqui bloqueia a peça (libera só com --liberar PECA)."""
    leg = it["legenda"]
    if it["marca"] == "retrozap":
        if re.search(r"wrapped", leg + " " + it["titulo"], re.I):
            it["conteudo"].append("legenda do Retrozap usa \"Wrapped\" (proibido como descrição do produto)")
        # Preço do Retrozap: R$ 13,99 desde 14/11/2026; R$ 8,99 só na promoção de 01/12 a 31/12/2026.
        dia_post = max(it["data"], agora().date()) if it["data"] else agora().date()  # vale a data em que sai
        if "8,99" in leg and not (dt.date(2026, 12, 1) <= dia_post <= dt.date(2026, 12, 31)):
            it["conteudo"].append("legenda cita R$ 8,99, mas o preço do Retrozap é R$ 13,99 desde 14/11 "
                                  "(R$ 8,99 só na promoção de 01/12 a 31/12)")
    if len(leg) > 2200:
        it["problemas"].append(f"legenda com {len(leg)} caracteres (limite do Instagram: 2.200)")
    if len(re.findall(r"#\w", leg)) > 30:
        it["problemas"].append("legenda com mais de 30 hashtags")
    if len(re.findall(r"(?<!\w)@\w", leg)) > 20:
        it["problemas"].append("legenda com mais de 20 menções")


# --------------------------------------------------------------------------- peças seguradas (segurar.json)

def le_segurar(avisos: list[str]) -> dict[str, dict]:
    """segurar.json -> {PECA: regra}. Lido a cada execução; arquivo ilegível segura tudo o que der para ler."""
    if not SEGURAR.exists():
        return {}
    try:
        dados = json.loads(SEGURAR.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"segurar.json ilegível ({e}); corrija antes de publicar")
    regras = {}
    for r in dados.get("segurar", []):
        if r.get("peca"):
            regras[r["peca"].upper()] = r
    return regras


def numero_versao(versao: str) -> int:
    m = re.search(r"-v(\d+)$", versao or "")
    return int(m.group(1)) if m else 0


def segurada(it: dict, regras: dict[str, dict]) -> str | None:
    """Motivo se a peça está segurada nesta versão; None se pode sair."""
    r = regras.get(it["peca"].upper())
    if not r:
        return None
    v = it["versao"]
    if v in (r.get("versoes") or []):
        return r.get("motivo") or "segurada"
    minimo = r.get("liberar_a_partir_de_v")
    if minimo and numero_versao(v) < int(minimo):
        return r.get("motivo") or "segurada"
    return None


# --------------------------------------------------------------------------- Graph API

class ErroGraph(Exception):
    def __init__(self, msg: str, codigo=None, sub=None, incerto=False):
        super().__init__(oculta_segredos(msg))
        self.codigo, self.sub, self.incerto = codigo, sub, incerto


class PublicadoSemId(ErroGraph):
    """O Instagram publicou, mas não consegui descobrir o id da mídia."""


class Graph:
    TRANSITORIOS = {1, 2, 4, 17, 32, 341, 613, 80001, 80002, 80004}

    def __init__(self, log_http: bool = False):
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "btw-postagem/1.0"
        self.log_http = log_http
        self.chamadas_escrita = 0
        self._tokens: dict[str, str] = {}

    def _pedido(self, metodo, url, params=None, data=None, headers=None, timeout=90):
        return self.s.request(metodo, url, params=params, data=data, headers=headers, timeout=timeout)

    def chamar(self, metodo: str, caminho: str, params: dict | None = None, data: dict | None = None,
               idempotente: bool = True, tentativas: int = 4, url: str | None = None,
               headers: dict | None = None) -> dict:
        url = url or f"{GRAPH}/{caminho.lstrip('/')}"
        espera = 4
        for t in range(1, tentativas + 1):
            try:
                r = self._pedido(metodo, url, params=params, data=data, headers=headers)
            except requests.RequestException as e:
                if not idempotente:
                    raise ErroGraph(f"sem resposta em {metodo} {caminho}: {type(e).__name__}", incerto=True)
                if t == tentativas:
                    raise ErroGraph(f"sem resposta em {metodo} {caminho} após {t} tentativas: {type(e).__name__}: {e}")
                time.sleep(espera)
                espera *= 3
                continue
            try:
                corpo = r.json()
            except ValueError:
                corpo = {"_texto": r.text[:300]}
            if r.ok and not (isinstance(corpo, dict) and "error" in corpo):
                return corpo
            err = corpo.get("error", {}) if isinstance(corpo, dict) else {}
            codigo, sub = err.get("code"), err.get("error_subcode")
            transitorio = r.status_code >= 500 or err.get("is_transient") or codigo in self.TRANSITORIOS
            msg = (f"{metodo} {caminho} -> HTTP {r.status_code}: {err.get('message') or corpo.get('_texto', '')}"
                   f" (code {codigo}, subcode {sub}"
                   f"{', ' + err.get('error_user_msg') if err.get('error_user_msg') else ''})")
            if transitorio and t < tentativas:
                if not idempotente and r.status_code >= 500:
                    raise ErroGraph(msg, codigo, sub, incerto=True)
                time.sleep(espera)
                espera *= 3
                continue
            raise ErroGraph(msg, codigo, sub, incerto=(not idempotente and r.status_code >= 500))
        raise ErroGraph(f"{metodo} {caminho}: tentativas esgotadas")

    def get(self, caminho, **params):
        return self.chamar("GET", caminho, params=params)

    def enviar_arquivo(self, caminho: str, data: dict, files: dict) -> bool:
        """POST multipart (capa de vídeo). Sem nova tentativa: é opcional."""
        r = self.s.post(f"{GRAPH}/{caminho}", data=data, files=files, timeout=120)
        return r.ok

    def token_pagina(self, page: str) -> str:
        if page not in self._tokens:
            tok = self.get(page, fields="access_token").get("access_token")
            if not tok:
                raise ErroGraph(f"sem token da página {page} (pages_manage_posts?)")
            self._tokens[page] = tok
        return self._tokens[page]


# --------------------------------------------------------------------------- registro (publicados.json)

class Registro:
    def __init__(self, caminho: Path = LOG):
        self.caminho = caminho
        self.dados = {"descricao": "Registro do growth/postagem/postar.py: o que já saiu (ou já existia) em cada rede.",
                      "publicacoes": []}
        if caminho.exists():
            self.dados = json.loads(caminho.read_text(encoding="utf-8"))
        self.mudou = False

    @property
    def itens(self) -> list[dict]:
        return self.dados.setdefault("publicacoes", [])

    def achar(self, marca: str, peca: str, plataforma: str, status=("publicado", "ja_existia", "publicando")):
        return [e for e in self.itens if e.get("marca") == marca and e.get("peca") == peca
                and e.get("plataforma") == plataforma and e.get("status") in status]

    def ids_conhecidos(self) -> set[str]:
        ids = set()
        for e in self.itens:
            for k in ("media_id", "post_id", "video_id"):
                if e.get(k):
                    ids.add(str(e[k]))
        return ids

    def gravar(self, entrada: dict, substituir: dict | None = None) -> None:
        if substituir is not None and substituir in self.itens:
            self.itens[self.itens.index(substituir)] = entrada
        else:
            self.itens.append(entrada)
        self.mudou = True
        tmp = self.caminho.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        os.replace(tmp, self.caminho)

    def remover(self, entrada: dict) -> None:
        if entrada in self.itens:
            self.itens.remove(entrada)
            self.mudou = True
            tmp = self.caminho.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            os.replace(tmp, self.caminho)


def trava_duplicados(itens: list[dict], reg) -> None:
    """Nada sai duplicado (Gui, 18/11). Além do registro por peça e da checagem na conta:
    1) mesma mídia (mesmo arquivo, com qualquer nome ou versão) já publicada por outra peça da marca;
    2) duas peças diferentes com a mesma mídia na agenda: só a primeira pode sair;
    3) feed (reel/carrossel): uma por marca, formato e dia. Já publicada ganha; depois, pack especial
       (ex.: QUIDDO-EDUCACAO) ganha do pack da semana (Snn); o resto fica bloqueado."""
    pub = {(e.get("marca"), e.get("peca")) for e in reg.itens if e.get("status") in ("publicado", "ja_existia", "publicando")}
    dono: dict[tuple, str] = {}
    for e in reg.itens:
        if e.get("status") in ("publicado", "ja_existia", "publicando"):
            for b in e.get("blobs") or []:
                dono.setdefault((e.get("marca"), b), e.get("peca"))
    for i in itens:
        if (i["marca"], i["peca"]) in pub:
            for b in i.get("blobs") or []:
                dono.setdefault((i["marca"], b), i["peca"])

    def repete(i):
        bl = i.get("blobs") or []
        if not bl:
            return None
        outros = [dono.get((i["marca"], b)) for b in bl]
        outros = [o for o in outros if o and o != i["peca"]]
        # reel/story: o arquivo principal; carrossel: metade ou mais dos cards (o card final de CTA se repete de propósito)
        if i["formato"] == "carrossel" and len(outros) * 2 < len(bl):
            return None
        # quadro final de CTA das sequências de stories (quadro 3) também se repete de propósito
        if i.get("quadro", 0) >= 3:
            return None
        return outros[0] if outros else None

    ordem = sorted(itens, key=lambda i: (i.get("quando") or dt.datetime.max.replace(tzinfo=BRT), i["pack"], i.get("quadro", 0)))
    for i in ordem:
        if (i["marca"], i["peca"]) in pub or not i.get("aprovado") or i.get("reserva"):
            continue
        o = repete(i)
        if o:
            i["problemas"].append(f"duplicado: a mesma mídia já saiu (ou vai sair antes) como {o}")
            continue
        # só "reserva" a mídia o que ainda vai sair (data de hoje em diante); o que passou da data e não saiu não conta
        if not i["problemas"] and i.get("data") and i["data"] >= agora().date():
            for b in i.get("blobs") or []:
                dono.setdefault((i["marca"], b), i["peca"])

    especial = lambda i: not re.fullmatch(r"S\d+", i["pack"] or "")
    grupos: dict[tuple, list[dict]] = {}
    for i in itens:
        if i["formato"] in ("reel", "carrossel") and i.get("data") and not i.get("reserva") and i.get("aprovado"):
            grupos.setdefault((i["marca"], i["data"], i["formato"]), []).append(i)
    for chave, lista in grupos.items():
        vivos = [i for i in lista if (i["marca"], i["peca"]) in pub or not i["problemas"]]
        if len(vivos) < 2:
            continue
        vivos.sort(key=lambda i: (0 if (i["marca"], i["peca"]) in pub else 1, 0 if especial(i) else 1, i["pack"], i["peca"]))
        fica = vivos[0]
        for i in vivos[1:]:
            if (i["marca"], i["peca"]) not in pub:
                i["problemas"].append(f"duplicado no dia: já há {i['formato']} da marca em {chave[1]:%d/%m} ({fica['peca']})")


def entrada_base(it: dict, plataforma: str) -> dict:
    e = {"marca": it["marca"], "peca": it["peca"], "versao": it["versao"], "pack": it["pack"],
         "formato": it["formato"], "plataforma": plataforma, "agendado": iso(it["quando"])}
    if it.get("blobs"):
        e["blobs"] = it["blobs"]
    return e


# --------------------------------------------------------------------------- o que já está nas contas

class Perfis:
    """Últimas publicações de cada conta, para não repetir o que o DOT (ou alguém) postou à mão."""

    def __init__(self, g: Graph):
        self.g = g
        self.cache: dict[tuple, list[dict]] = {}
        self.erros: list[str] = []

    def _buscar(self, chave, fn):
        if chave not in self.cache:
            try:
                self.cache[chave] = fn()
            except ErroGraph as e:
                self.erros.append(f"{chave}: {e}")
                self.cache[chave] = None
        return self.cache[chave]

    def ig_media(self, marca):
        ig = MARCAS[marca]["ig"]
        return self._buscar(("ig_media", marca), lambda: self.g.get(
            f"{ig}/media", fields="id,caption,timestamp,media_product_type,media_type,permalink", limit=25).get("data", []))

    def ig_stories(self, marca):
        ig = MARCAS[marca]["ig"]
        return self._buscar(("ig_stories", marca), lambda: self.g.get(
            f"{ig}/stories", fields="id,timestamp,media_type,permalink", limit=50).get("data", []))

    def fb_posts(self, marca):
        page = MARCAS[marca]["page"]
        return self._buscar(("fb_posts", marca), lambda: self.g.get(
            f"{page}/published_posts", fields="id,message,created_time,permalink_url", limit=25,
            access_token=self.g.token_pagina(page)).get("data", []))

    def fb_reels(self, marca):
        page = MARCAS[marca]["page"]
        return self._buscar(("fb_reels", marca), lambda: self.g.get(
            f"{page}/video_reels", fields="id,description,created_time,permalink_url", limit=25,
            access_token=self.g.token_pagina(page)).get("data", []))

    def fb_videos(self, marca):
        page = MARCAS[marca]["page"]
        return self._buscar(("fb_videos", marca), lambda: self.g.get(
            f"{page}/videos", fields="id,description,created_time,permalink_url", limit=25,
            access_token=self.g.token_pagina(page)).get("data", []))

    def fb_stories(self, marca):
        page = MARCAS[marca]["page"]
        return self._buscar(("fb_stories", marca), lambda: self.g.get(
            f"{page}/stories", fields="post_id,status,creation_time,media_type,url", limit=50,
            access_token=self.g.token_pagina(page)).get("data", []))

    def esquecer(self, marca):
        for k in list(self.cache):
            if k[1] == marca:
                del self.cache[k]


def tempo_meta(s: str | int | None) -> dt.datetime | None:
    if s is None:
        return None
    if isinstance(s, (int, float)) or str(s).isdigit():
        return dt.datetime.fromtimestamp(int(s), dt.timezone.utc)
    s = str(s).replace("+0000", "+00:00")
    try:
        return dt.datetime.fromisoformat(s)
    except ValueError:
        return None


def duplicata_remota(it: dict, plataforma: str, perfis: Perfis, conhecidos: set[str]):
    """(achou, descrição, link, alertas). Feed: mesma 1ª linha de legenda. Story: story não registrado perto do horário."""
    marca, alertas = it["marca"], []
    if it["formato"] == "story":
        lista = perfis.ig_stories(marca) if plataforma == "instagram" else perfis.fb_stories(marca)
        if lista is None:
            return False, "", "", ["não consegui ler os stories da conta para checar duplicidade"]
        limite = it["quando"] - dt.timedelta(hours=JANELA_STORY_MANUAL_H)
        for s in lista:
            sid = str(s.get("id") or s.get("post_id") or "")
            t = tempo_meta(s.get("timestamp") or s.get("creation_time"))
            if sid in conhecidos or not t:
                continue
            if t >= limite:
                return True, f"já há story não registrado na conta, postado {hm(t)}", s.get("permalink") or s.get("url") or "", alertas
        return False, "", "", alertas
    alvo = it["legenda"] or ""
    if plataforma == "instagram":
        fontes = [perfis.ig_media(marca)]
    else:
        fontes = [perfis.fb_posts(marca), perfis.fb_reels(marca) if it["formato"] == "reel" else []]
        if it["formato"] == "reel":
            fontes.append(perfis.fb_videos(marca))
    for lista in fontes:
        if lista is None:
            alertas.append("não consegui ler as publicações da conta para checar duplicidade")
            continue
        for m in lista:
            texto = m.get("caption") or m.get("message") or m.get("description") or ""
            if not texto:
                continue
            link = m.get("permalink") or m.get("permalink_url") or ""
            if normaliza(texto) and normaliza(texto) == normaliza(alvo):
                return True, f"mesma 1ª linha de legenda já publicada ({(m.get('timestamp') or m.get('created_time') or '')[:16]})", link, alertas
            if parece(texto, alvo) >= 0.8:
                alertas.append(f"legenda parecida já no perfil: \"{texto.splitlines()[0][:60]}\" {link}")
    return False, "", "", alertas


# --------------------------------------------------------------------------- publicação

class Publicador:
    def __init__(self, g: Graph, reg: Registro, perfis: Perfis, fallback_video: bool = True):
        self.g, self.reg, self.perfis = g, reg, perfis
        self.fallback_video = fallback_video

    # ---- Instagram
    def ig_container(self, ig: str, params: dict) -> str:
        return self.g.chamar("POST", f"{ig}/media", data=params)["id"]

    def ig_esperar(self, cid: str, limite: int) -> None:
        fim, passo = time.time() + limite, 5
        while True:
            s = self.g.get(cid, fields="status_code,status")
            cod = s.get("status_code")
            if cod in ("FINISHED", "PUBLISHED"):
                return
            if cod in ("ERROR", "EXPIRED"):
                raise ErroGraph(f"container {cid}: {cod} {s.get('status', '')}")
            if time.time() > fim:
                raise ErroGraph(f"container {cid} ainda em {cod} após {limite}s")
            time.sleep(passo)
            passo = min(passo + 5, 20)

    def ig_publicar(self, marca: str, cid: str, inicio: dt.datetime) -> str:
        ig = MARCAS[marca]["ig"]
        for t in range(4):
            try:
                return self.g.chamar("POST", f"{ig}/media_publish", data={"creation_id": cid},
                                     idempotente=False, tentativas=1)["id"]
            except ErroGraph as e:
                st = {}
                try:
                    st = self.g.get(cid, fields="status_code")
                except ErroGraph:
                    pass
                if st.get("status_code") == "PUBLISHED":
                    mid = self.ig_achar_publicado(marca, inicio)
                    if mid:
                        return mid
                    raise PublicadoSemId(f"container {cid} foi publicado mas não achei o id da mídia; confira o perfil")
                if e.incerto or e.codigo in (9007, 4, 2) or e.sub == 2207027:
                    time.sleep(10 * (t + 1))
                    continue
                raise
        raise ErroGraph(f"media_publish do container {cid} falhou 4 vezes")

    def ig_achar_publicado(self, marca: str, inicio: dt.datetime) -> str | None:
        self.perfis.esquecer(marca)
        conhecidos = self.reg.ids_conhecidos()
        for lista in (self.perfis.ig_media(marca) or [], self.perfis.ig_stories(marca) or []):
            for m in lista:
                t = tempo_meta(m.get("timestamp"))
                if t and t >= inicio - dt.timedelta(minutes=2) and m["id"] not in conhecidos:
                    return m["id"]
        return None

    def instagram(self, it: dict) -> dict:
        marca, ig, u = it["marca"], MARCAS[it["marca"]]["ig"], it["urls"]
        inicio = agora()
        if it["formato"] == "story":
            p = {"media_type": "STORIES"}
            p.update({"image_url": u["imagem"]} if "imagem" in u else {"video_url": u["video"]})
            cid = self.ig_container(ig, rotulo_ia(it, p))
            self.ig_esperar(cid, ESPERA_REEL_S if "video" in u else 180)
        elif it["formato"] == "reel":
            p = {"media_type": "REELS", "video_url": u["video"], "caption": it["legenda"], "share_to_feed": "true"}
            if u.get("capa"):
                p["cover_url"] = u["capa"]
            cid = self.ig_container(ig, rotulo_ia(it, p))
            self.ig_esperar(cid, ESPERA_REEL_S)
        else:
            filhos = []
            for img in u["imagens"]:
                filhos.append(self.ig_container(ig, {"is_carousel_item": "true", "image_url": img}))
            for f in filhos:
                self.ig_esperar(f, 180)
            cid = self.ig_container(ig, rotulo_ia(it, {"media_type": "CAROUSEL", "children": ",".join(filhos),
                                         "caption": it["legenda"]}))
            self.ig_esperar(cid, 180)
        pend = dict(entrada_base(it, "instagram"), status="publicando", container_id=cid, inicio=iso(inicio))
        self.reg.gravar(pend)
        try:
            mid = self.ig_publicar(marca, cid, inicio)
        except PublicadoSemId as e:
            fim = dict(entrada_base(it, "instagram"), status="publicado", media_id="", permalink="",
                       container_id=cid, publicado_em=iso(agora()), obs=str(e))
            self.reg.gravar(fim, substituir=pend)
            return fim
        except ErroGraph:
            self.reg.remover(pend)
            raise
        link = ""
        try:
            link = self.g.get(mid, fields="permalink").get("permalink", "")
        except ErroGraph:
            pass
        fim = dict(entrada_base(it, "instagram"), status="publicado", media_id=mid, permalink=link,
                   container_id=cid, publicado_em=iso(agora()))
        self.reg.gravar(fim, substituir=pend)
        return fim

    # ---- Facebook
    def fb_foto_oculta(self, page: str, tok: str, url: str) -> str:
        return self.g.chamar("POST", f"{page}/photos", data={"url": url, "published": "false",
                                                              "access_token": tok})["id"]

    def fb_upload_por_url(self, upload_url: str, tok: str, arquivo_url: str) -> None:
        if not re.match(r"^https://[a-z0-9.-]+\.facebook\.com/", upload_url or ""):
            raise ErroGraph("upload_url fora de facebook.com; não envio o token")  # token de página só para a Meta
        r = self.g.chamar("POST", "", url=upload_url, headers={"Authorization": f"OAuth {tok}", "file_url": arquivo_url},
                          tentativas=3)
        if not r.get("success", True):
            raise ErroGraph(f"upload do vídeo recusado: {r}")

    def fb_esperar_video(self, vid: str, tok: str, limite: int = ESPERA_REEL_S) -> dict:
        """Espera o Facebook terminar de baixar o vídeo (uploading_phase = complete)."""
        fim = time.time() + limite
        while True:
            st = self.g.get(vid, fields="status", access_token=tok).get("status", {})
            fases = [st.get("video_status")] + [(st.get(f) or {}).get("status") for f in
                                                ("uploading_phase", "processing_phase", "publishing_phase")]
            if "error" in fases:
                raise ErroGraph(f"vídeo {vid} com erro no Facebook: {json.dumps(st)[:300]}")
            if (st.get("uploading_phase") or {}).get("status") == "complete" or st.get("video_status") in ("ready", "upload_complete"):
                return st
            if time.time() > fim:
                raise ErroGraph(f"vídeo {vid} não terminou de subir em {limite}s: {json.dumps(st)[:200]}")
            time.sleep(8)

    def fb_achar_recente(self, marca: str, inicio: dt.datetime, texto: str | None, fontes) -> dict | None:
        self.perfis.esquecer(marca)
        for fonte in fontes:
            for m in fonte(marca) or []:
                t = tempo_meta(m.get("created_time") or m.get("creation_time"))
                corpo = m.get("message") or m.get("description") or ""
                if t and t >= inicio - dt.timedelta(minutes=2) and (texto is None or normaliza(corpo) == normaliza(texto)):
                    return m
        return None

    def facebook(self, it: dict) -> dict:
        marca, page, u = it["marca"], MARCAS[it["marca"]]["page"], it["urls"]
        tok = self.g.token_pagina(page)
        inicio = agora()
        extra: dict = {}
        if it["formato"] == "story":
            if "imagem" in u:
                foto = self.fb_foto_oculta(page, tok, u["imagem"])
                try:
                    r = self.g.chamar("POST", f"{page}/photo_stories", data={"photo_id": foto, "access_token": tok},
                                      idempotente=False, tentativas=1)
                except ErroGraph as e:
                    if e.incerto and self.fb_achar_recente(marca, inicio, None, [self.perfis.fb_stories]):
                        r = {"post_id": "?"}
                    else:
                        raise
                post_id = r.get("post_id") or r.get("id")
                extra = {"post_id": post_id, "foto_id": foto}
            else:
                ini = self.g.chamar("POST", f"{page}/video_stories", data={"upload_phase": "start", "access_token": tok})
                vid = ini["video_id"]
                self.fb_upload_por_url(ini["upload_url"], tok, u["video"])
                r = self.g.chamar("POST", f"{page}/video_stories", data={"upload_phase": "finish", "video_id": vid,
                                                                       "access_token": tok}, idempotente=False, tentativas=1)
                extra = {"post_id": r.get("post_id"), "video_id": vid}
        elif it["formato"] == "carrossel":
            fotos = [self.fb_foto_oculta(page, tok, url) for url in u["imagens"]]
            dados = {"message": it["legenda"], "access_token": tok,
                     "attached_media": json.dumps([{"media_fbid": f} for f in fotos])}
            try:
                r = self.g.chamar("POST", f"{page}/feed", data=dados, idempotente=False, tentativas=1)
            except ErroGraph as e:
                achado = e.incerto and self.fb_achar_recente(marca, inicio, it["legenda"], [self.perfis.fb_posts])
                if not achado:
                    raise
                r = {"id": achado["id"]}
            extra = {"post_id": r.get("id")}
        else:
            extra = self.fb_reel(it, page, tok, inicio)
        link = ""
        alvo = extra.get("post_id") or extra.get("video_id")
        if alvo and alvo != "?":
            try:
                link = self.g.get(alvo, fields="permalink_url", access_token=tok).get("permalink_url", "")
            except ErroGraph:
                pass
        ent = dict(entrada_base(it, "facebook"), status="publicado", permalink=link, publicado_em=iso(agora()), **extra)
        self.reg.gravar(ent)
        return ent

    def fb_reel(self, it: dict, page: str, tok: str, inicio: dt.datetime) -> dict:
        u = it["urls"]
        ini = self.g.chamar("POST", f"{page}/video_reels", data={"upload_phase": "start", "access_token": tok})
        vid = ini["video_id"]
        upload_url = ini.get("upload_url") or f"https://rupload.facebook.com/video-upload/v23.0/{vid}"
        try:
            self.fb_upload_por_url(upload_url, tok, u["video"])
        except ErroGraph as e:
            if not self.fallback_video:
                raise
            # rupload.facebook.com fora da rede liberada: sobe como vídeo da página (o Facebook o mostra como reel).
            return self.fb_video_pagina(it, page, tok, inicio, motivo=str(e))
        self.fb_esperar_video(vid, tok)
        try:
            self.g.chamar("POST", f"{page}/video_reels",
                          data={"upload_phase": "finish", "video_id": vid, "video_state": "PUBLISHED",
                                "description": it["legenda"], "access_token": tok},
                          idempotente=False, tentativas=1)
        except ErroGraph as e:
            if not (e.incerto and self.fb_achar_recente(it["marca"], inicio, it["legenda"], [self.perfis.fb_reels])):
                raise
        extra = {"video_id": vid, "tipo_fb": "reel"}
        if u.get("capa"):
            extra["capa_fb"] = self.fb_capa(vid, tok, it)
        return extra

    def fb_video_pagina(self, it: dict, page: str, tok: str, inicio: dt.datetime, motivo: str) -> dict:
        u = it["urls"]
        try:
            r = self.g.chamar("POST", f"{page}/videos",
                              data={"file_url": u["video"], "description": it["legenda"], "published": "true",
                                    "access_token": tok}, idempotente=False, tentativas=1)
        except ErroGraph as e:
            achado = e.incerto and self.fb_achar_recente(it["marca"], inicio, it["legenda"], [self.perfis.fb_videos])
            if not achado:
                raise
            r = {"id": achado["id"]}
        extra = {"video_id": r.get("id"), "tipo_fb": "video_pagina",
                 "obs": "reel subiu como vídeo da página: upload do Reels (rupload.facebook.com) bloqueado: "
                        + oculta_segredos(motivo)[:160]}
        if u.get("capa"):
            extra["capa_fb"] = self.fb_capa(r.get("id"), tok, it)
        return extra

    def fb_capa(self, vid: str, tok: str, it: dict) -> str:
        """Capa do vídeo no Facebook (melhor esforço; falha não derruba a publicação)."""
        try:
            conteudo = requests.get(it["urls"]["capa"], timeout=60)
            conteudo.raise_for_status()
            nome = it["midia"]["capa"].rsplit("/", 1)[-1]
            ok = self.g.enviar_arquivo(f"{vid}/thumbnails", {"is_preferred": "true", "access_token": tok},
                                       {"source": (nome, conteudo.content, "image/png")})
            return "ok" if ok else "falhou"
        except Exception as e:  # noqa: BLE001 - capa é opcional
            return f"falhou: {oculta_segredos(type(e).__name__)}"


# --------------------------------------------------------------------------- checagem de mídia

def checar_midia(it: dict, cont: Conteudo, sessao: requests.Session, cache: dict) -> list[str]:
    """Links: HTTP 200 e tipo certo. Arquivos: specs de Reels/Stories/feed via ffprobe e PIL."""
    achados: list[str] = []
    m = it.get("midia") or {}
    caminhos = [c for k, c in m.items() if k in ("video", "capa", "imagem") and c] + m.get("imagens", [])
    for cam in caminhos:
        for url in (RAW_SOCIAL + cam, f"{RAW}{cont.sha}/{cam}"):
            if url in cache:
                r = cache[url]
            else:
                try:
                    h = sessao.head(url, timeout=30, allow_redirects=True)
                    r = (h.status_code, h.headers.get("content-type", ""), int(h.headers.get("content-length") or 0))
                except requests.RequestException as e:
                    r = (0, type(e).__name__, 0)
                cache[url] = r
            cod, tipo, tam = r
            esperado = ("video/mp4", "application/octet-stream") if cam.endswith(".mp4") else ("image/png", "image/jpeg")
            if cod != 200 or not tipo.startswith(esperado):
                achados.append(f"ERRO link {url}: HTTP {cod}, {tipo}")
    for cam in caminhos:
        chave = ("spec", cam, it["formato"])
        if chave not in cache:
            cache[chave] = spec_arquivo(cam, it["formato"], cont)
        achados += cache[chave]
    if it["formato"] == "carrossel" and m.get("imagens"):
        tamanhos = {_cache_dim.get(c) for c in m["imagens"]}
        if len(tamanhos) > 1:
            achados.append(f"ERRO carrossel com páginas de tamanhos diferentes: {sorted(map(str, tamanhos))}")
    return achados


def spec_arquivo(cam: str, formato: str, cont: Conteudo) -> list[str]:
    nome = cam.rsplit("/", 1)[-1]
    achados: list[str] = []
    dados = cont.bytes(cam)
    if cam.lower().endswith((".png", ".jpg", ".jpeg")):
        from PIL import Image  # import local: só a checagem precisa
        with Image.open(io.BytesIO(dados)) as im:
            w, h = im.size
        _cache_dim[cam] = (w, h)
        if len(dados) > 8 * 1024 * 1024:
            achados.append(f"ERRO {nome}: {len(dados) / 1e6:.1f} MB (limite do Instagram: 8 MB)")
        if formato == "story" and abs(w / h - 9 / 16) > 0.01:
            achados.append(f"AVISO {nome}: {w}×{h} não é 9:16")
        if formato == "carrossel" and not (0.8 - 0.005 <= w / h <= 1.91):
            achados.append(f"ERRO {nome}: {w}×{h} fora de 4:5 a 1,91:1")
        if formato == "reel" and cam.lower().endswith(("-capa.png", "-capa.jpg")) and abs(w / h - 9 / 16) > 0.01:
            achados.append(f"AVISO capa {nome}: {w}×{h} não é 9:16")
        return achados
    if not shutil.which("ffprobe"):
        return [f"AVISO {nome}: ffprobe não instalado, specs do vídeo não conferidas"]
    with tempfile.TemporaryDirectory() as d:
        arq = Path(d) / "video.mp4"
        arq.write_bytes(dados)
        r = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(arq)],
                           capture_output=True, text=True)
    if r.returncode != 0:
        return [f"ERRO {nome}: ffprobe não leu o arquivo"]
    info = json.loads(r.stdout)
    v = next((s for s in info["streams"] if s.get("codec_type") == "video"), None)
    a = next((s for s in info["streams"] if s.get("codec_type") == "audio"), None)
    dur = float(info["format"].get("duration") or 0)
    if not v:
        return [f"ERRO {nome}: sem faixa de vídeo"]
    w, h = int(v["width"]), int(v["height"])
    num, den = (v.get("avg_frame_rate") or v.get("r_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den or 1) if float(den or 1) else 0
    br = int(info["format"].get("bit_rate") or 0)
    resumo = (f"{nome}: {w}×{h}, {dur:.1f}s, {v.get('codec_name')} {v.get('pix_fmt')}, {fps:.0f} fps, "
              f"{br / 1e6:.1f} Mbps, áudio {a.get('codec_name') + ' ' + str(a.get('sample_rate')) + ' Hz' if a else 'nenhum'}, "
              f"{len(dados) / 1e6:.1f} MB")
    achados.append("INFO " + resumo)
    if v.get("codec_name") not in ("h264", "hevc"):
        achados.append(f"ERRO {nome}: codec {v.get('codec_name')} (use H.264 ou HEVC)")
    if v.get("pix_fmt") not in ("yuv420p", "yuvj420p"):
        achados.append(f"AVISO {nome}: pix_fmt {v.get('pix_fmt')} (recomendado yuv420p)")
    if a and a.get("codec_name") != "aac":
        achados.append(f"ERRO {nome}: áudio {a.get('codec_name')} (use AAC)")
    if abs(w / h - 9 / 16) > 0.01:
        achados.append(f"AVISO {nome}: {w}×{h} não é 9:16")
    if w > 1920 or h > 1920 * 16 / 9 + 1:
        achados.append(f"AVISO {nome}: resolução acima do recomendado (1080×1920)")
    if not 23 <= fps <= 60:
        achados.append(f"ERRO {nome}: {fps:.1f} fps (Reels/Stories: 23 a 60)")
    if br > 25e6:
        achados.append(f"ERRO {nome}: bitrate {br / 1e6:.1f} Mbps (máx. 25)")
    if formato == "reel":
        if not 3 <= dur <= 900:
            achados.append(f"ERRO {nome}: {dur:.1f}s (Reels no Instagram: 3 s a 15 min)")
        if dur > 90:
            achados.append(f"AVISO {nome}: {dur:.1f}s (Reels no Facebook: até 90 s)")
    if formato == "story" and not 3 <= dur <= 60:
        achados.append(f"ERRO {nome}: {dur:.1f}s (story em vídeo: 3 a 60 s)")
    return achados


_cache_dim: dict[str, tuple[int, int]] = {}


def volume_maximo(cont: Conteudo, cam: str, cache: dict) -> float | None:
    """Pico de áudio do vídeo em dB (None se não der para medir). -91 dB = faixa muda."""
    if cam in cache:
        return cache[cam]
    if not shutil.which("ffmpeg"):
        cache[cam] = None
        return None
    with tempfile.TemporaryDirectory() as d:
        arq = Path(d) / "video.mp4"
        arq.write_bytes(cont.bytes(cam))
        r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(arq), "-vn", "-af", "volumedetect",
                            "-f", "null", "-"], capture_output=True, text=True)
    m = re.search(r"max_volume:\s*(-?[\d.]+|-inf) dB", r.stderr)
    if not m:
        cache[cam] = -999.0 if "does not contain any stream" in r.stderr or "Output file is empty" in r.stderr else None
        if cache[cam] is None and "Stream #0" in r.stderr and "Audio" not in r.stderr:
            cache[cam] = -999.0
    else:
        cache[cam] = -999.0 if m.group(1) == "-inf" else float(m.group(1))
    return cache[cam]


def validar_containers(it: dict, g: Graph) -> list[str]:
    """Cria containers do Instagram SEM publicar (não ficam públicos e expiram em 24 h)."""
    ig, u, res = MARCAS[it["marca"]]["ig"], it["urls"], []
    pub = Publicador(g, None, None)  # só usa ig_container/ig_esperar: nada é publicado
    try:
        if it["formato"] == "story":
            p = {"media_type": "STORIES"}
            p.update({"image_url": u["imagem"]} if "imagem" in u else {"video_url": u["video"]})
            cid = pub.ig_container(ig, rotulo_ia(it, p))
            pub.ig_esperar(cid, ESPERA_REEL_S)
        elif it["formato"] == "reel":
            p = {"media_type": "REELS", "video_url": u["video"], "caption": it["legenda"], "share_to_feed": "true"}
            if u.get("capa"):
                p["cover_url"] = u["capa"]
            cid = pub.ig_container(ig, rotulo_ia(it, p))
            pub.ig_esperar(cid, ESPERA_REEL_S)
        else:
            filhos = [pub.ig_container(ig, {"is_carousel_item": "true", "image_url": x}) for x in u["imagens"]]
            for f in filhos:
                pub.ig_esperar(f, 180)
            cid = pub.ig_container(ig, rotulo_ia(it, {"media_type": "CAROUSEL", "children": ",".join(filhos), "caption": it["legenda"]}))
            pub.ig_esperar(cid, 180)
        res.append(f"container IG {cid}: FINISHED (pronto, NÃO publicado)")
    except ErroGraph as e:
        res.append(f"ERRO container IG: {e}")
    return res


# --------------------------------------------------------------------------- git do registro

def git_atualizar(avisos: list[str]) -> None:
    r = subprocess.run(["git", "-C", str(REPO), "pull", "--rebase", "--autostash", "-q"], capture_output=True, text=True)
    if r.returncode != 0:
        avisos.append(f"git pull --rebase falhou (sigo com o registro local): {r.stderr.strip()[:200]}")


def git_salvar_registro(reg: Registro, avisos: list[str]) -> str:
    if not reg.mudou:
        return "registro sem mudança; nada a commitar"
    ramo = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    if ramo in ("main", "master", BRANCH_CONTEUDO, "HEAD"):
        avisos.append(f"branch atual é {ramo}: não faço commit nem push do registro aqui")
        return "sem push"
    rel = str(LOG.relative_to(REPO))
    git_atualizar(avisos)
    git("add", rel)
    if not git("diff", "--cached", "--name-only", "--", rel).strip():
        return "registro já estava no git"
    git("commit", "-q", "-m", f"Postagem: registro de publicações ({agora():%d/%m %Hh%M})", "--", rel)
    for t in range(4):
        r = subprocess.run(["git", "-C", str(REPO), "push", "-q", "origin", f"HEAD:{ramo}"], capture_output=True, text=True)
        if r.returncode == 0:
            return f"registro commitado e enviado para {ramo}"
        time.sleep(2 * 2 ** t)
        subprocess.run(["git", "-C", str(REPO), "pull", "--rebase", "--autostash", "-q", "origin", ramo],
                       capture_output=True, text=True)
    avisos.append("push do registro falhou 4 vezes: rode git push à mão")
    return "push falhou"


# --------------------------------------------------------------------------- relatórios

def rotulo(it: dict) -> str:
    q = hm(it["quando"]) if it.get("quando") else it["data_txt"]
    return f"{q} · {MARCAS[it['marca']]['nome'] if it['marca'] else it['marca_txt']} · {it['formato']} · {it['peca']} ({it['versao']})"


def imprime_item_dry(it: dict, plats: list[str], destinos: dict) -> None:
    print(f"\n▶ {rotulo(it)}  [{it['pack']}, linha {it['linha']}]")
    print(f"  título: {it['titulo']}")
    if it.get("rotulo_ia"):
        print("  rótulo de IA da Meta: ligado (is_ai_generated)")
    for p in plats:
        alvo = MARCAS[it["marca"]]["usuario"] if p == "instagram" else f"página {MARCAS[it['marca']]['page']}"
        print(f"  {p}: {destinos[p]}  → {alvo}")
    u = it.get("urls", {})
    for k in ("imagem", "video", "capa"):
        if u.get(k):
            print(f"  {k}: {u[k]}")
    for i, x in enumerate(u.get("imagens", []), 1):
        print(f"  página {i}: {x}")
    if it["legenda"]:
        print(f"  legenda ({it['legenda_fonte']}):")
        print("    | " + it["legenda"].replace("\n", "\n    | "))
    elif it["formato"] == "story":
        print("  legenda: (story não tem legenda)")


def descreve_destinos(it: dict) -> dict:
    if it["formato"] == "story":
        fb = "story de foto (/photos oculta → /photo_stories)" if "imagem" in it.get("urls", {}) else "story de vídeo (/video_stories)"
        return {"instagram": "STORIES (" + ("imagem" if "imagem" in it.get("urls", {}) else "vídeo") + ")", "facebook": fb}
    if it["formato"] == "reel":
        return {"instagram": "REELS (share_to_feed, capa)", "facebook": "reel (/video_reels; se o upload for bloqueado, vídeo da página)"}
    n = len(it.get("urls", {}).get("imagens", []))
    return {"instagram": f"CAROUSEL ({n} imagens)", "facebook": f"post com {n} fotos (/photos ocultas → /feed)"}


def cobertura(itens: list[dict], de: dt.date, ate: dt.date, cont: Conteudo | None = None,
              regras: dict | None = None) -> str:
    validos = [i for i in itens if i["marca"] and i["data"] and not i["reserva"] and i["aprovado"]
               and not i["problemas"] and i.get("quando")]
    vol: dict = {}

    def mudo(i: dict) -> bool:
        if not cont or i["formato"] != "reel" or not i.get("midia", {}).get("video"):
            return False
        pico = volume_maximo(cont, i["midia"]["video"], vol)
        return pico is not None and pico < -60
    out = [f"# Cobertura de {de:%d/%m} a {ate:%d/%m} (só peças aprovadas, sem reservas)\n",
           "| Dia | " + " | ".join(MARCAS[m]["nome"] for m in MARCAS) + " |",
           "|---|" + "---|" * len(MARCAS)]
    buracos, horarios = [], set()
    d = de
    nomes_dia = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
    while d <= ate:
        cel = []
        for m in MARCAS:
            doDia = sorted([i for i in validos if i["data"] == d and i["marca"] == m], key=lambda i: i["quando"])
            for i in doDia:
                horarios.add(i["quando"].strftime("%Hh%M").replace("h00", "h"))
            partes = [f"{i['formato'][0].upper()} {i['peca']} {i['quando']:%Hh%M}".replace("h00", "h")
                      + (" ⏸" if regras and segurada(i, regras) else "")
                      + (" ⚠" if i["conteudo"] else "") + (" 🔇" if mudo(i) else "") for i in doDia]
            if not any(i["formato"] == "story" for i in doDia):
                partes.append("**sem story**")
                buracos.append((d, m))
            cel.append("<br>".join(partes) if partes else "—")
        out.append(f"| {d:%d/%m} {nomes_dia[d.weekday()]} | " + " | ".join(cel) + " |")
        d += dt.timedelta(days=1)
    out.append("\nS = story, R = reel, C = carrossel. ⏸ = segurada (segurar.json). ⚠ = alerta de conteúdo (bloqueada até --liberar). 🔇 = reel sem som (precisa do ok do Gui: --permitir-mudo).\n")
    out.append(f"Dias-marca sem story: {len(buracos)}")
    por_dia: dict[dt.date, list[str]] = {}
    for d, m in buracos:
        por_dia.setdefault(d, []).append(MARCAS[m]["nome"])
    for d, ms in por_dia.items():
        out.append(f"- {d:%d/%m}: {', '.join(ms)}")
    res = [i for i in itens if i["reserva"] and i["aprovado"]]
    if res:
        out.append("\nReservas aprovadas (sem data, podem cobrir buraco com ok do Gui):")
        for i in res:
            out.append(f"- {MARCAS[i['marca']]['nome']} · {i['formato']} · {i['peca']} ({i['versao']}) · {i['titulo']}")
    out.append(f"\nHorários usados nas agendas: {', '.join(sorted(horarios))} (Brasília)")
    return "\n".join(out)


# --------------------------------------------------------------------------- principal

def main() -> int:
    ap = argparse.ArgumentParser(description="Publica no Instagram e no Facebook a agenda aprovada do branch social.")
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument("--dry-run", action="store_true", help="mostra o que seria publicado, sem nenhum POST")
    modo.add_argument("--executar", action="store_true", help="publica de verdade")
    modo.add_argument("--cobertura", metavar="DE:ATE", help="tabela de cobertura (ex.: 2026-11-15:2026-12-06)")
    ap.add_argument("--quando", help="AAAA-MM-DDTHH:MM em Brasília (padrão: agora)")
    ap.add_argument("--janela", type=int, default=JANELA_PADRAO,
                    help=f"minutos para trás a partir de --quando (padrão {JANELA_PADRAO}); "
                         f"também pega até {ANTECIPAR_MIN} min à frente")
    ap.add_argument("--marca", action="append", help="só esta marca (retrozap, quiddo, sportdna); pode repetir")
    ap.add_argument("--peca", action="append", help="só esta peça (ex.: R-RX1); pode repetir")
    ap.add_argument("--plataformas", default="instagram", help="instagram (padrão; o Gui decidiu em 17/11 não postar no Facebook)")
    ap.add_argument("--liberar", action="append", default=[],
                    help="peça cujo alerta de conteúdo o Gui já liberou (ex.: R-R6); pode repetir")
    ap.add_argument("--incluir-reserva", action="append", default=[], metavar="PECA",
                    help="publica agora uma reserva aprovada (ex.: D-S8), só com ok do Gui; pode repetir")
    ap.add_argument("--checar-midia", action="store_true", help="confere links (HTTP 200, tipo) e specs (ffprobe/PIL)")
    ap.add_argument("--validar-containers", action="store_true",
                    help="no --dry-run, cria containers do Instagram sem publicar (expiram em 24 h)")
    ap.add_argument("--sem-fetch", action="store_true", help="não busca o branch social (usa a cópia local)")
    ap.add_argument("--sem-git", action="store_true", help="no --executar, não faz pull/commit/push do registro")
    ap.add_argument("--sem-fixar", action="store_true", help="usa links do branch (padrão: links fixados no commit lido)")
    ap.add_argument("--sem-fallback-video", action="store_true",
                    help="no Facebook, não sobe reel como vídeo da página quando o upload do Reels falhar")
    ap.add_argument("--permitir-mudo", action="store_true",
                    help="publica reels sem som (o guia do pack manda perguntar ao Gui antes)")
    ap.add_argument("--relatorio", help="grava o relatório em JSON neste caminho")
    a = ap.parse_args()

    plats = [p.strip() for p in a.plataformas.split(",") if p.strip()]
    try:
        sem_fb = json.loads(SEM_FACEBOOK.read_text(encoding="utf-8")).get("pular", {}) if SEM_FACEBOOK.exists() else {}
    except (ValueError, OSError):
        sem_fb = {"story": list(MARCAS), "carrossel": list(MARCAS), "reel": list(MARCAS)}  # ilegível: não arrisca
    if any(p not in PLATAFORMAS for p in plats):
        ap.error("--plataformas aceita instagram e facebook")
    marcas_f = {chave_marca(m) for m in (a.marca or [])}
    if None in marcas_f:
        ap.error("--marca aceita retrozap, quiddo ou sportdna")
    liberar = {p.upper() for p in a.liberar}

    if a.executar:  # só uma publicação por vez; dry-run e cobertura não escrevem nada
        trava = open(TRAVA, "w")
        try:
            fcntl.flock(trava, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            print("Outra execução do postar.py --executar está rodando. Saindo.", file=sys.stderr)
            return 3

    avisos: list[str] = []
    if a.executar and not a.sem_git:
        git_atualizar(avisos)
    cont = Conteudo(buscar=not a.sem_fetch)
    avisos += cont.avisos
    itens = carrega_agenda(cont, fixar_sha=not a.sem_fixar)
    aprovados_seq = {(i["marca"], i["peca"]) for i in itens if i.get("quadro") == 1 and i.get("aprovado")}
    for i in itens:
        if i.get("cede_para_sequencia") and (i["marca"], f"{i['peca']}.1") in aprovados_seq:
            i["problemas"].append("substituído pela sequência aprovada do mesmo dia (STORIES-SEQ)")
    trava_duplicados(itens, Registro())  # lê o publicados.json (só leitura)

    if a.cobertura:
        de, _, ate = a.cobertura.partition(":")
        print(cobertura(itens, dt.date.fromisoformat(de), dt.date.fromisoformat(ate or de), cont, le_segurar(avisos)))
        return 0

    quando = dt.datetime.fromisoformat(a.quando).replace(tzinfo=BRT) if a.quando else agora()
    inicio_j = quando - dt.timedelta(minutes=a.janela)
    fim_j = quando + dt.timedelta(minutes=ANTECIPAR_MIN)
    if a.executar:
        fim_j = min(fim_j, agora() + dt.timedelta(minutes=ANTECIPAR_MIN))  # nunca publica o futuro
    reservas_ok = {p.upper() for p in a.incluir_reserva}
    for i in itens:
        if i["reserva"] and i["peca"].upper() in reservas_ok:
            i["reserva"], i["quando"] = False, quando if a.quando else agora()
            i["avisos"].append("reserva publicada fora da agenda com --incluir-reserva (ok do Gui)")
            reservas_ok.discard(i["peca"].upper())
    if reservas_ok:
        ap.error(f"reserva não encontrada: {', '.join(sorted(reservas_ok))}")
    sel = [i for i in itens if i.get("quando") and inicio_j <= i["quando"] <= fim_j]
    sel += [i for i in itens if i["reserva"] and i["data"] and inicio_j.date() <= i["data"] <= fim_j.date()]
    if marcas_f:
        sel = [i for i in sel if i["marca"] in marcas_f]
    if a.peca:
        sel = [i for i in sel if i["peca"].upper() in {p.upper() for p in a.peca}]
    sel.sort(key=lambda i: (i.get("quando") or dt.datetime.combine(i["data"], dt.time(23, 59), BRT),
                            list(MARCAS).index(i["marca"]) if i["marca"] else 9, i["formato"] or "",
                            i.get("quadro", 0)))

    modo_txt = "EXECUÇÃO" if a.executar else "DRY-RUN (nenhum POST de publicação)"
    print(f"== postar.py · {modo_txt} · branch social @ {cont.sha[:10]}")
    print(f"== janela: {hm(inicio_j)} → {hm(fim_j)} (Brasília) · plataformas: {', '.join(plats)} · {len(sel)} linha(s)")
    if a.executar and fim_j < quando:
        print("== (o --executar nunca publica o que está marcado para mais de 15 min no futuro)")

    g = Graph()
    reg = Registro()
    perfis = Perfis(g)
    pub = Publicador(g, reg, perfis, fallback_video=not a.sem_fallback_video)
    rel = {"modo": "executar" if a.executar else "dry-run", "sha_social": cont.sha, "janela": [iso(inicio_j), iso(fim_j)],
           "publicado": [], "seria_publicado": [], "pulado": [], "segurado": [], "bloqueado": [], "erros": [], "adesivos": [], "avisos": avisos}
    segurar = le_segurar(avisos)
    cache_midia: dict = {}
    cache_volume: dict = {}
    sessao_midia = requests.Session()

    # pendências de execuções interrompidas (status "publicando")
    if a.executar:
        for e in [x for x in reg.itens if x.get("status") == "publicando"]:
            try:
                st = g.get(e["container_id"], fields="status_code").get("status_code")
            except ErroGraph:
                st = None
            if st == "PUBLISHED":
                ini = tempo_meta(e.get("inicio")) or agora() - dt.timedelta(hours=24)
                mid = pub.ig_achar_publicado(e["marca"], ini)
                novo = dict(e, status="publicado", media_id=mid or "", publicado_em=e.get("inicio"),
                            obs="recuperado de execução interrompida")
                reg.gravar(novo, substituir=e)
            else:
                reg.remover(e)

    # quota do Instagram
    cota: dict[str, int] = {}
    if "instagram" in plats:
        for m in {i["marca"] for i in sel if i["marca"]}:
            try:
                d = g.get(f"{MARCAS[m]['ig']}/content_publishing_limit", fields="quota_usage,config")["data"][0]
                cota[m] = int(d["config"]["quota_total"]) - int(d["quota_usage"])
            except (ErroGraph, KeyError, IndexError, ValueError):
                cota[m] = 100

    planejado: set = set()  # (marca, peça, plataforma) que sai nesta rodada (no dry-run, libera o quadro seguinte)
    for it in sel:
        nome = rotulo(it)
        if it["reserva"]:
            rel["pulado"].append({"peca": nome, "motivo": "reserva: não agendar (só com ok do Gui)"})
            continue
        motivo_seg = segurada(it, segurar)
        if motivo_seg:
            rel["segurado"].append({"peca": nome, "motivo": f"segurado: aguardando versão aprovada ({motivo_seg})"})
            print(f"\n⏸ {nome}\n  segurado: aguardando versão aprovada ({motivo_seg})")
            continue
        if it["formato"] == "reel" and it.get("midia", {}).get("video") and not it["problemas"]:
            pico = volume_maximo(cont, it["midia"]["video"], cache_volume)
            if pico is None:
                it["avisos"].append("não consegui medir o áudio do reel (ffmpeg)")
            elif pico < -60 and not a.permitir_mudo:
                it["conteudo"].append("reel sem som (sem música nem narração). O guia do pack manda perguntar ao Gui "
                                      "antes de publicar sem música; a API não põe áudio em alta. "
                                      "Com o ok dele: --permitir-mudo")
            elif pico < -60:
                it["avisos"].append("reel sem som publicado com --permitir-mudo")
        bloqueios = list(it["problemas"])
        if it["peca"].upper() not in liberar:
            bloqueios += it["conteudo"]
        elif it["conteudo"]:
            it["avisos"].append("alerta de conteúdo liberado via --liberar: " + "; ".join(it["conteudo"]))
        if bloqueios:
            rel["bloqueado"].append({"peca": nome, "motivos": bloqueios})
            print(f"\n✖ {nome}\n  BLOQUEADO: " + "\n  BLOQUEADO: ".join(bloqueios))
            continue
        if it["formato"] == "story" and it["adesivo"]:
            rel["adesivos"].append({"peca": nome, "adesivo": it["adesivo"]})
        elif it["adesivo"] and not it["adesivo"].lower().startswith("áudio: usar o do vídeo"):
            it["avisos"].append("nota da agenda: " + it["adesivo"])  # "usar o áudio do vídeo" já é o que a API faz

        destinos = descreve_destinos(it)
        a_fazer = []
        for p in plats:
            if it.get("anterior"):
                ant = [e for e in reg.achar(it["marca"], it["anterior"], p) if e.get("status") in ("publicado", "ja_existia")]
                if not ant and not (not a.executar and (it["marca"], it["anterior"], p) in planejado):
                    rel["pulado"].append({"peca": nome, "plataforma": p,
                                          "motivo": f"sequência: o quadro anterior ({it['anterior']}) ainda não saiu"})
                    continue
            if p == "facebook" and it["marca"] in sem_fb.get(it["formato"], []):
                rel["pulado"].append({"peca": nome, "plataforma": p,
                                      "motivo": "Facebook desligado (sem_facebook.json): "
                                                "o Gui decidiu em 17/11 não postar no Facebook"})
                continue
            ja = reg.achar(it["marca"], it["peca"], p)
            if ja:
                e = ja[-1]
                rel["pulado"].append({"peca": nome, "plataforma": p,
                                      "motivo": f"já no registro ({e.get('status')} {e.get('versao')} "
                                                f"{e.get('publicado_em') or e.get('agendado')})",
                                      "link": e.get("permalink", "")})
                continue
            try:
                achou, desc, link, alertas = duplicata_remota(it, p, perfis, reg.ids_conhecidos())
            except ErroGraph as e:
                achou, desc, link, alertas = False, "", "", [f"checagem de duplicidade falhou: {e}"]
            it["avisos"] += [f"{p}: {x}" for x in alertas]
            if achou:
                rel["pulado"].append({"peca": nome, "plataforma": p, "motivo": desc, "link": link})
                if a.executar:
                    reg.gravar(dict(entrada_base(it, p), status="ja_existia", permalink=link,
                                    obs=desc, registrado_em=iso(agora())))
                continue
            if p == "instagram" and cota.get(it["marca"], 100) < COTA_MINIMA:
                rel["pulado"].append({"peca": nome, "plataforma": p, "motivo": "cota de publicação do Instagram quase no fim"})
                continue
            a_fazer.append(p)

        planejado.update((it["marca"], it["peca"], p) for p in a_fazer)
        if not a.executar:
            if a_fazer:
                imprime_item_dry(it, a_fazer, destinos)
                rel["seria_publicado"].append({"peca": nome, "plataformas": a_fazer, "legenda": it["legenda"],
                                               "urls": it.get("urls"), "destinos": {p: destinos[p] for p in a_fazer}})
                if a.checar_midia:
                    achados = checar_midia(it, cont, sessao_midia, cache_midia)
                    for x in achados:
                        print("  mídia: " + x)
                    rel["seria_publicado"][-1]["midia"] = achados
                if a.validar_containers and "instagram" in a_fazer:
                    for x in validar_containers(it, g):
                        print("  " + x)
                        rel["seria_publicado"][-1].setdefault("containers", []).append(x)
            for x in it["avisos"]:
                print(f"  aviso: {x}")
                rel["avisos"].append(f"{it['peca']}: {x}")
            continue

        for p in a_fazer:
            print(f"\n→ publicando {nome} no {p}…", flush=True)
            try:
                ent = pub.instagram(it) if p == "instagram" else pub.facebook(it)
                if p == "instagram":
                    cota[it["marca"]] = cota.get(it["marca"], 100) - 1
                rel["publicado"].append({"peca": nome, "plataforma": p, "link": ent.get("permalink", ""),
                                         "id": ent.get("media_id") or ent.get("post_id") or ent.get("video_id"),
                                         "obs": ent.get("obs", "")})
                print(f"  ok: {ent.get('permalink') or ent.get('media_id') or ent.get('post_id') or ent.get('video_id')}")
            except (ErroGraph, requests.RequestException, KeyError) as e:
                msg = oculta_segredos(str(e))
                rel["erros"].append({"peca": nome, "plataforma": p, "erro": msg})
                print(f"  ERRO: {msg}")
        for x in it["avisos"]:
            rel["avisos"].append(f"{it['peca']}: {x}")

    if perfis.erros:
        rel["avisos"] += [f"leitura do perfil: {x}" for x in perfis.erros]
    if a.executar and not a.sem_git:
        try:
            rel["git"] = git_salvar_registro(reg, rel["avisos"])
        except RuntimeError as e:
            rel["avisos"].append(f"git do registro falhou: {oculta_segredos(str(e))}")

    print("\n================ RELATÓRIO ================")
    if a.executar:
        print(f"Publicado: {len(rel['publicado'])}")
        for x in rel["publicado"]:
            print(f"  ✔ {x['peca']} · {x['plataforma']} · {x['link'] or x['id']}" + (f" · {x['obs']}" if x["obs"] else ""))
    else:
        print(f"Seria publicado: {len(rel['seria_publicado'])} peça(s)")
        for x in rel["seria_publicado"]:
            print(f"  • {x['peca']} → {', '.join(x['plataformas'])}")
    print(f"Pulado: {len(rel['pulado'])}")
    for x in rel["pulado"]:
        print(f"  – {x['peca']}" + (f" · {x['plataforma']}" if x.get("plataforma") else "") + f": {x['motivo']}"
              + (f" {x['link']}" if x.get("link") else ""))
    print(f"Segurado: {len(rel['segurado'])}")
    for x in rel["segurado"]:
        print(f"  ⏸ {x['peca']}: {x['motivo']}")
    print(f"Bloqueado: {len(rel['bloqueado'])}")
    for x in rel["bloqueado"]:
        print(f"  ✖ {x['peca']}: {'; '.join(x['motivos'])}")
    if rel["erros"]:
        print(f"Erros: {len(rel['erros'])}")
        for x in rel["erros"]:
            print(f"  ! {x['peca']} · {x['plataforma']}: {x['erro']}")
    if rel["adesivos"]:
        print("Adesivos que a API não aplica (a arte sai sem eles):")
        for x in rel["adesivos"]:
            print(f"  ◦ {x['peca']}: {x['adesivo']}")
    if rel["avisos"]:
        print("Avisos:")
        for x in rel["avisos"]:
            print(f"  · {x}")
    if "git" in rel:
        print(f"Git: {rel['git']}")
    if a.relatorio:
        Path(a.relatorio).write_text(json.dumps(rel, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return 1 if rel["erros"] else 0


if __name__ == "__main__":
    sys.exit(main())
