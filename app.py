"""Interface Streamlit do DivisorRoteiro."""

import importlib

import streamlit as st

import segmentador as modulo_segmentador


importlib.invalidate_caches()
modulo_segmentador = importlib.reload(modulo_segmentador)
Segmentador = modulo_segmentador.Segmentador


st.set_page_config(page_title="DivisorRoteiro", page_icon="🎬", layout="wide")
st.title("🎬 DivisorRoteiro")
st.caption("Divisão determinística em prompts de aproximadamente 8 segundos.")

tempo = st.text_input("Tempo do voice-over", placeholder="MM:SS ou HH:MM:SS")
roteiro = st.text_area("Roteiro", height=320, placeholder="Cole aqui o roteiro completo...")

if st.button("Gerar Prompts", type="primary", use_container_width=True):
    try:
        segmentador = Segmentador(roteiro, tempo)
        segmentos = segmentador.dividir()
        estatisticas = segmentador.estatisticas()
        st.session_state["resultado"] = (segmentador, segmentos, estatisticas)
    except (ValueError, RuntimeError) as erro:
        st.session_state.pop("resultado", None)
        st.error(str(erro))

if "resultado" in st.session_state:
    segmentador, segmentos, estatisticas = st.session_state["resultado"]
    st.subheader("Estatísticas")
    colunas = st.columns(4)
    metricas = [
        ("Tempo", estatisticas["tempo"]),
        ("Palavras", estatisticas["palavras"]),
        ("Prompts", estatisticas["prompts"]),
        ("Média", f"{estatisticas['media']:.2f}"),
        ("Menor prompt", estatisticas["menor_prompt"]),
        ("Maior prompt", estatisticas["maior_prompt"]),
        ("Desvio padrão", f"{estatisticas['desvio_padrao']:.2f}"),
    ]
    for indice, (rotulo, valor) in enumerate(metricas):
        colunas[indice % 4].metric(rotulo, valor)

    st.subheader("Downloads")
    downloads = st.columns(3)
    downloads[0].download_button(
        "Baixar TXT", segmentador.exportar_txt(), "prompts.txt", "text/plain"
    )
    downloads[1].download_button(
        "Baixar Markdown",
        segmentador.exportar_markdown(),
        "prompts.md",
        "text/markdown",
    )
    downloads[2].download_button(
        "Baixar CSV", segmentador.exportar_csv(), "prompts.csv", "text/csv"
    )

    st.subheader("Prompts")
    for segmento in segmentos:
        with st.expander(
            f"PROMPT {segmento['numero']:03d} · {segmento['palavras']} palavras",
            expanded=segmento["numero"] <= 3,
        ):
            st.caption(
                f"{segmento['inicio_tempo']}s–{segmento['fim_tempo']}s · "
                f"tokens {segmento['inicio']}–{segmento['fim']}"
            )
            st.write(segmento["texto"])
