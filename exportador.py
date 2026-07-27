"""Exportação dos prompts em formatos portáveis."""

from __future__ import annotations

import csv
import io
from typing import Any, Sequence

from formatter import Formatter


class Exportador:
    """Gera TXT, Markdown e CSV sem acessar o sistema de arquivos."""

    @staticmethod
    def _exigir_segmentos(segmentos: Sequence[dict[str, Any]]) -> None:
        if not segmentos:
            raise ValueError("Não há segmentos para exportar.")

    @classmethod
    def para_txt(cls, segmentos: Sequence[dict[str, Any]]) -> str:
        cls._exigir_segmentos(segmentos)
        return Formatter.formatar_todos(segmentos) + "\n"

    @classmethod
    def para_markdown(cls, segmentos: Sequence[dict[str, Any]]) -> str:
        cls._exigir_segmentos(segmentos)
        blocos = []
        for segmento in segmentos:
            inicio = Formatter.formatar_tempo(segmento["inicio_tempo"])
            fim = Formatter.formatar_tempo(segmento["fim_tempo"])
            blocos.append(
                f"## PROMPT {segmento['numero']:03d}\n\n"
                f"**{inicio} - {fim} · {segmento['palavras']} palavras**\n\n"
                f"{segmento['texto']}"
            )
        return "\n\n---\n\n".join(blocos) + "\n"

    @classmethod
    def para_csv(cls, segmentos: Sequence[dict[str, Any]]) -> str:
        cls._exigir_segmentos(segmentos)
        saida = io.StringIO(newline="")
        writer = csv.writer(saida)
        writer.writerow(["prompt", "inicio", "fim", "palavras", "texto"])
        for segmento in segmentos:
            writer.writerow(
                [
                    segmento["numero"],
                    Formatter.formatar_tempo(segmento["inicio_tempo"]),
                    Formatter.formatar_tempo(segmento["fim_tempo"]),
                    segmento["palavras"],
                    segmento["texto"],
                ]
            )
        return saida.getvalue()
