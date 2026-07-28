"""Testes de propriedades do segmentador."""

import math
import unittest

from segmentador import Segmentador
from validator import Validator


class SegmentadorTestes(unittest.TestCase):
    def test_preserva_tokens_em_ampla_faixa(self) -> None:
        sinais = (".", "?", "!", ":", ";", ",", "")
        for palavras in range(1, 151):
            texto = " ".join(
                f"token{indice}{sinais[indice % len(sinais)]}" for indice in range(palavras)
            )
            for segundos in range(1, 161, 7):
                segmentador = Segmentador(texto, f"00:{segundos:02d}" if segundos < 60 else f"{segundos // 60:02d}:{segundos % 60:02d}")
                segmentos = segmentador.dividir()
                self.assertEqual(math.ceil(segundos / 8), len(segmentos))
                self.assertEqual([], Validator.validar(texto.split(), segmentos))
                self.assertEqual(texto.split(), [token for item in segmentos for token in item["texto"].split()])

    def test_balanceamento_tem_limite(self) -> None:
        texto = " ".join(f"p{indice}." for indice in range(503))
        segmentador = Segmentador(texto, "06:40")
        segmentos = segmentador.dividir()
        tamanhos = [segmento["palavras"] for segmento in segmentos]
        self.assertLessEqual(max(tamanhos) - min(tamanhos), 1)
        self.assertEqual({10, 11}, set(tamanhos))

    def test_janela_impede_quebras_naturais_extremas(self) -> None:
        texto = " ".join(
            f"p{indice}." if indice in (2, 17) else f"p{indice}"
            for indice in range(20)
        )
        tamanhos = [
            item["palavras"] for item in Segmentador(texto, "00:24").dividir()
        ]
        media = 20 / 3
        self.assertGreaterEqual(min(tamanhos), math.floor(media * 0.6))
        self.assertLessEqual(max(tamanhos), math.ceil(media * 1.4))

    def test_extremos_so_ocorrem_quando_inevitaveis(self) -> None:
        segmentos = Segmentador("uma duas tres", "00:40").dividir()
        self.assertEqual(
            [0, 0, 1, 1, 1], sorted(item["palavras"] for item in segmentos)
        )

    def test_poucas_palavras_nao_duplica_tokens(self) -> None:
        segmentador = Segmentador("uma. duas?", "01:20")
        segmentos = segmentador.dividir()
        self.assertEqual(10, len(segmentos))
        self.assertEqual(["uma.", "duas?"], [token for item in segmentos for token in item["texto"].split()])

    def test_pontuacao_respeita_prioridade(self) -> None:
        texto = "a b c d e f g, h. i j k l m n o p q"
        segmentos = Segmentador(texto, "00:16").dividir()
        self.assertTrue(segmentos[0]["texto"].endswith("."))

    def test_pontuacao_natural_pode_superar_balanceamento_perfeito(self) -> None:
        texto = "a b c, d e f. g h i j k l m n o p"
        segmentos = Segmentador(texto, "00:16").dividir()
        self.assertEqual([6, 10], [item["palavras"] for item in segmentos])
        self.assertTrue(segmentos[0]["texto"].endswith("."))

    def test_timing_estimado_compensa_palavras_longas(self) -> None:
        texto = "extraordinariamente incompreensivelmente rapidamente sol luz mar céu paz fim"
        segmentos = Segmentador(texto, "00:16").dividir()
        self.assertLessEqual(segmentos[0]["palavras"], segmentos[1]["palavras"])

    def test_evitar_corte_antes_de_continuidade_de_acao(self) -> None:
        texto = "A câmera avança, enquanto a personagem abre lentamente a porta. Depois surge outra cena completa."
        segmentos = Segmentador(texto, "00:16").dividir()
        self.assertFalse(segmentos[1]["texto"].startswith("enquanto"))

    def test_tempos_invalidos(self) -> None:
        for tempo in ("", "00:00", "1:60", "00:70", "abc", "1:2:3:4"):
            with self.subTest(tempo=tempo), self.assertRaises(ValueError):
                Segmentador("texto", tempo).dividir()


if __name__ == "__main__":
    unittest.main()
