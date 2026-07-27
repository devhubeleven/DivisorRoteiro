"""Segmentação determinística de roteiros por índices de tokens."""

from __future__ import annotations

import math
import statistics
from bisect import bisect_left
from typing import Any

from exportador import Exportador
from validator import Validator


class Segmentador:
    """Divide um roteiro sem alterar, remover ou reordenar seus tokens."""

    DURACAO_PROMPT = 8
    JANELA_CORTE = 4
    PONTUACAO = (".", "?", "!", ":", ";", ",")
    CONECTORES = frozenset(
        {
            "a", "ao", "aos", "as", "com", "da", "das", "de", "do", "dos",
            "e", "em", "entre", "mas", "nem", "no", "nos", "na", "nas", "o",
            "os", "ou", "para", "pela", "pelas", "pelo", "pelos", "por", "porque",
            "que", "se", "sem", "sob", "um", "uma", "uns", "umas",
        }
    )
    TRANSICOES = frozenset(
        {
            "agora", "assim", "depois", "então", "finalmente", "logo", "portanto",
            "primeiro", "seguinte",
        }
    )
    CONTINUIDADE_ACAO = frozenset(
        {"antes", "até", "conforme", "durante", "enquanto", "quando", "simultaneamente"}
    )
    VOGAIS = frozenset("aeiouáàâãéêíóôõúü")

    def __init__(self, roteiro: str, tempo: str) -> None:
        self.roteiro = roteiro
        self.tempo = tempo.strip()
        self.tokens: list[str] = []
        self.total_segundos = 0
        self.total_palavras = 0
        self.total_prompts = 0
        self.media = 0.0
        self.segmentos: list[dict[str, Any]] = []

    @staticmethod
    def converter_tempo(tempo: str) -> int:
        """Converte MM:SS ou HH:MM:SS em segundos."""
        partes = tempo.strip().split(":")
        if len(partes) not in (2, 3) or any(not parte.isdigit() for parte in partes):
            raise ValueError("Tempo inválido. Use MM:SS ou HH:MM:SS.")

        valores = [int(parte) for parte in partes]
        if len(valores) == 2:
            minutos, segundos = valores
            horas = 0
        else:
            horas, minutos, segundos = valores

        if segundos >= 60 or (len(valores) == 3 and minutos >= 60):
            raise ValueError("Minutos e segundos devem estar entre 00 e 59.")

        total = horas * 3600 + minutos * 60 + segundos
        if total <= 0:
            raise ValueError("A duração deve ser maior que zero.")
        return total

    def _preparar(self) -> None:
        self.total_segundos = self.converter_tempo(self.tempo)
        self.tokens = self.roteiro.split()
        if not self.tokens:
            raise ValueError("O roteiro não pode estar vazio.")

        self.total_palavras = len(self.tokens)
        self.total_prompts = math.ceil(self.total_segundos / self.DURACAO_PROMPT)
        self.media = self.total_palavras / self.total_prompts

    @classmethod
    def _peso_token(cls, token: str) -> float:
        """Estima deterministicamente o tempo relativo de pronúncia de um token."""
        palavra = "".join(caractere for caractere in token.lower() if caractere.isalpha())
        grupos_vocais = 0
        em_vogal = False
        for caractere in palavra:
            vogal = caractere in cls.VOGAIS
            if vogal and not em_vogal:
                grupos_vocais += 1
            em_vogal = vogal
        peso = 0.55 + 0.34 * max(1, grupos_vocais) + 0.015 * min(len(palavra), 20)
        if token.endswith((".", "?", "!")):
            peso += 0.58
        elif token.endswith((":", ";")):
            peso += 0.36
        elif token.endswith(","):
            peso += 0.20
        return peso

    def _pesos_acumulados(self) -> list[float]:
        acumulados = [0.0]
        for token in self.tokens:
            acumulados.append(acumulados[-1] + self._peso_token(token))
        return acumulados

    def _candidatos(self, numero_corte: int, acumulados: list[float]) -> list[int]:
        if numero_corte == 0:
            return [0]
        if numero_corte == self.total_prompts:
            return [self.total_palavras]

        alvo_peso = acumulados[-1] * numero_corte / self.total_prompts
        ideal_audio = bisect_left(acumulados, alvo_peso)
        ideal_palavras = (
            2 * numero_corte * self.total_palavras + self.total_prompts
        ) // (2 * self.total_prompts)

        if self.total_palavras >= self.total_prompts:
            minimo_global = numero_corte
            maximo_global = self.total_palavras - (self.total_prompts - numero_corte)
        else:
            minimo_global = 0
            maximo_global = self.total_palavras

        candidatos: set[int] = set()
        for ideal in (ideal_audio, ideal_palavras):
            inicio = max(minimo_global, ideal - self.JANELA_CORTE)
            fim = min(maximo_global, ideal + self.JANELA_CORTE)
            candidatos.update(range(inicio, fim + 1))
        candidatos.add(min(max(ideal_palavras, minimo_global), maximo_global))
        return sorted(candidatos)

    @staticmethod
    def _normalizar_token(token: str) -> str:
        return token.strip(".,!?;:()[]{}\"'“”‘’—-").lower()

    def _custo_corte(self, corte: int) -> float:
        if corte <= 0 or corte >= self.total_palavras:
            return 0.0

        anterior = self.tokens[corte - 1]
        seguinte = self.tokens[corte]
        anterior_limpo = self._normalizar_token(anterior)
        seguinte_limpo = self._normalizar_token(seguinte)
        custo = 0.0

        recompensas = {".": -16.0, "?": -15.0, "!": -14.0, ":": -10.0, ";": -8.0, ",": -4.0}
        for sinal in self.PONTUACAO:
            if anterior.endswith(sinal):
                custo += recompensas[sinal]
                break
        else:
            custo += 7.0

        if anterior_limpo in self.CONECTORES:
            custo += 13.0
        if seguinte_limpo in self.CONECTORES:
            custo += 9.0
        if seguinte_limpo in self.CONTINUIDADE_ACAO:
            custo += 12.0
        if seguinte_limpo in self.TRANSICOES:
            custo -= 5.0
        if anterior.endswith(",") and seguinte_limpo in self.CONECTORES:
            custo += 7.0
        if anterior.endswith((".", "?", "!")) and seguinte[:1].isupper():
            custo -= 3.0
        return custo

    def _selecionar_limites(self) -> list[int]:
        """Otimiza simultaneamente todos os cortes por programação dinâmica."""
        acumulados = self._pesos_acumulados()
        peso_medio = acumulados[-1] / self.total_prompts
        candidatos_por_corte = [
            self._candidatos(numero, acumulados)
            for numero in range(self.total_prompts + 1)
        ]
        custos: dict[int, float] = {0: 0.0}
        caminhos: list[dict[int, int]] = []

        for numero in range(1, self.total_prompts + 1):
            novos_custos: dict[int, float] = {}
            predecessores: dict[int, int] = {}
            for fim in candidatos_por_corte[numero]:
                melhor: tuple[float, int] | None = None
                for inicio, custo_anterior in custos.items():
                    if fim < inicio or (self.total_palavras >= self.total_prompts and fim == inicio):
                        continue
                    palavras = fim - inicio
                    peso = acumulados[fim] - acumulados[inicio]
                    desvio_peso = (peso - peso_medio) / max(peso_medio, 1e-9)
                    desvio_palavras = (palavras - self.media) / max(self.media, 1.0)
                    custo = (
                        custo_anterior
                        + 22.0 * desvio_peso * desvio_peso
                        + 5.0 * desvio_palavras * desvio_palavras
                        + self._custo_corte(fim)
                    )
                    opcao = (custo, inicio)
                    if melhor is None or opcao < melhor:
                        melhor = opcao
                if melhor is not None:
                    novos_custos[fim] = melhor[0]
                    predecessores[fim] = melhor[1]
            if not novos_custos:
                raise RuntimeError("Não foi possível construir uma segmentação válida.")
            custos = novos_custos
            caminhos.append(predecessores)

        limite = self.total_palavras
        limites = [limite]
        for predecessores in reversed(caminhos):
            limite = predecessores[limite]
            limites.append(limite)
        limites.reverse()
        return limites

    def dividir(self) -> list[dict[str, Any]]:
        """Gera os prompts, valida sua integridade e retorna os segmentos."""
        self._preparar()
        self.segmentos = []
        limites = self._selecionar_limites()

        for indice in range(self.total_prompts):
            numero = indice + 1
            inicio = limites[indice]
            fim = limites[numero]

            inicio_tempo = indice * self.DURACAO_PROMPT
            fim_tempo = min(numero * self.DURACAO_PROMPT, self.total_segundos)
            self.segmentos.append(
                {
                    "numero": numero,
                    "inicio": inicio,
                    "fim": fim,
                    "inicio_tempo": inicio_tempo,
                    "fim_tempo": fim_tempo,
                    "palavras": fim - inicio,
                    "texto": " ".join(self.tokens[inicio:fim]),
                }
            )

        Validator.validar_ou_lancar(self.tokens, self.segmentos)
        return self.segmentos

    def estatisticas(self) -> dict[str, int | float | str]:
        """Retorna estatísticas da última divisão realizada."""
        if not self.segmentos:
            raise RuntimeError("Execute dividir() antes de solicitar estatísticas.")
        tamanhos = [segmento["palavras"] for segmento in self.segmentos]
        return {
            "tempo": self.tempo,
            "tempo_segundos": self.total_segundos,
            "palavras": self.total_palavras,
            "prompts": self.total_prompts,
            "media": self.media,
            "menor_prompt": min(tamanhos),
            "maior_prompt": max(tamanhos),
            "desvio_padrao": statistics.pstdev(tamanhos),
        }

    def exportar_txt(self) -> bytes:
        """Exporta os segmentos em TXT, em memória."""
        return Exportador.para_txt(self.segmentos).encode("utf-8")

    def exportar_markdown(self) -> bytes:
        """Exporta os segmentos em Markdown, em memória."""
        return Exportador.para_markdown(self.segmentos).encode("utf-8")

    def exportar_csv(self) -> bytes:
        """Exporta os segmentos em CSV, em memória."""
        return Exportador.para_csv(self.segmentos).encode("utf-8-sig")
