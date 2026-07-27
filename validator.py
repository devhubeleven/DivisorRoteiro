"""Validação da integridade dos segmentos gerados."""

from __future__ import annotations

from collections import Counter
from typing import Any, Sequence


class Validator:
    """Confere tokens, ordem e continuidade dos índices."""

    @staticmethod
    def validar(tokens_originais: Sequence[str], segmentos: Sequence[dict[str, Any]]) -> list[str]:
        erros: list[str] = []
        tokens_saida = [token for segmento in segmentos for token in segmento["texto"].split()]

        if len(tokens_saida) != len(tokens_originais):
            erros.append(
                f"Quantidade divergente: original={len(tokens_originais)}, saída={len(tokens_saida)}."
            )

        faltantes = Counter(tokens_originais) - Counter(tokens_saida)
        repetidos = Counter(tokens_saida) - Counter(tokens_originais)
        if faltantes:
            erros.append(f"Tokens perdidos: {dict(faltantes)}.")
        if repetidos:
            erros.append(f"Tokens repetidos: {dict(repetidos)}.")
        if list(tokens_originais) != tokens_saida:
            erros.append("A sequência ou a posição dos tokens foi alterada.")

        fim_anterior = 0
        fim_tempo_anterior = 0
        for numero_esperado, segmento in enumerate(segmentos, start=1):
            if segmento["numero"] != numero_esperado:
                erros.append(f"Numeração inválida no segmento {numero_esperado}.")
            if not 0 <= segmento["inicio"] <= segmento["fim"] <= len(tokens_originais):
                erros.append(f"Índices inválidos no prompt {numero_esperado:03}.")
            if segmento["inicio"] != fim_anterior:
                erros.append(f"Descontinuidade antes do prompt {numero_esperado:03}.")
            if segmento["fim"] - segmento["inicio"] != segmento["palavras"]:
                erros.append(f"Contagem inválida no prompt {numero_esperado:03}.")
            texto_esperado = " ".join(tokens_originais[segmento["inicio"] : segmento["fim"]])
            if segmento["texto"] != texto_esperado:
                erros.append(f"Texto divergente dos índices no prompt {numero_esperado:03}.")
            if segmento["inicio_tempo"] != fim_tempo_anterior:
                erros.append(f"Descontinuidade de tempo no prompt {numero_esperado:03}.")
            if segmento["fim_tempo"] < segmento["inicio_tempo"]:
                erros.append(f"Intervalo de tempo inválido no prompt {numero_esperado:03}.")
            fim_anterior = segmento["fim"]
            fim_tempo_anterior = segmento["fim_tempo"]

        if fim_anterior != len(tokens_originais):
            erros.append("O índice final não coincide com o total de tokens.")
        if tokens_originais and tokens_saida:
            if tokens_originais[0] != tokens_saida[0]:
                erros.append("O primeiro token foi alterado.")
            if tokens_originais[-1] != tokens_saida[-1]:
                erros.append("O último token foi alterado.")
        return erros

    @classmethod
    def validar_ou_lancar(
        cls, tokens_originais: Sequence[str], segmentos: Sequence[dict[str, Any]]
    ) -> None:
        """Lança ValueError quando qualquer divergência é encontrada."""
        erros = cls.validar(tokens_originais, segmentos)
        if erros:
            raise ValueError("Falha na validação: " + " ".join(erros))
