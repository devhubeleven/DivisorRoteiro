"""Formatação de tempos e prompts."""

from __future__ import annotations

from typing import Any, Sequence


class Formatter:
    """Centraliza a apresentação textual dos resultados."""

    @staticmethod
    def formatar_tempo(segundos: int) -> str:
        horas, resto = divmod(segundos, 3600)
        minutos, segundos = divmod(resto, 60)
        if horas:
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        return f"{minutos:02d}:{segundos:02d}"

    @classmethod
    def formatar_segmento(cls, segmento: dict[str, Any]) -> str:
        inicio = cls.formatar_tempo(segmento["inicio_tempo"])
        fim = cls.formatar_tempo(segmento["fim_tempo"])
        return (
            f"PROMPT {segmento['numero']:03d} | {inicio} - {fim} | "
            f"{segmento['palavras']} palavras\n{segmento['texto']}"
        )

    @classmethod
    def formatar_todos(cls, segmentos: Sequence[dict[str, Any]]) -> str:
        return "\n\n".join(cls.formatar_segmento(segmento) for segmento in segmentos)
