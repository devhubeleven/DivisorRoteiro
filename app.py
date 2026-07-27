"""Interface Streamlit do DivisorRoteiro."""

from __future__ import annotations

import html
import importlib
import json

import streamlit as st
import streamlit.components.v1 as components

import segmentador as modulo_segmentador


importlib.invalidate_caches()
modulo_segmentador = importlib.reload(modulo_segmentador)
Segmentador = modulo_segmentador.Segmentador


st.set_page_config(
    page_title="Divisor de Roteiros",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        :root {
            --brand: #2563EB;
            --brand-dark: #1D4ED8;
            --ink: #0F172A;
            --muted: #64748B;
            --line: #E2E8F0;
            --surface: #FFFFFF;
            --surface-soft: #F8FAFC;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 10% -10%, rgba(37, 99, 235, .08), transparent 30rem),
                #F8FAFC;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        .block-container {
            max-width: 1500px;
            padding: 3.25rem 3rem 5rem;
        }

        .hero {
            margin-bottom: 2rem;
        }

        .hero__eyebrow {
            display: inline-flex;
            align-items: center;
            gap: .5rem;
            margin-bottom: .9rem;
            color: var(--brand);
            font-size: .75rem;
            font-weight: 750;
            letter-spacing: .12em;
            text-transform: uppercase;
        }

        .hero__mark {
            width: .55rem;
            height: .55rem;
            border-radius: 999px;
            background: var(--brand);
            box-shadow: 0 0 0 5px rgba(37, 99, 235, .10);
        }

        .hero h1 {
            margin: 0;
            color: var(--ink);
            font-size: clamp(2.15rem, 4vw, 3.55rem);
            font-weight: 780;
            letter-spacing: -.045em;
            line-height: 1.05;
        }

        .hero__subtitle {
            max-width: 850px;
            margin: 1rem 0 .9rem;
            color: #475569;
            font-size: 1.08rem;
            line-height: 1.65;
        }

        .hero__benefits {
            color: var(--muted);
            font-size: .84rem;
            font-weight: 520;
            line-height: 1.7;
        }

        .section-heading {
            margin: 2.25rem 0 1rem;
        }

        .section-heading h2 {
            margin: 0;
            color: var(--ink);
            font-size: 1.25rem;
            font-weight: 720;
            letter-spacing: -.02em;
        }

        .section-heading p {
            margin: .35rem 0 0;
            color: var(--muted);
            font-size: .9rem;
        }

        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label {
            color: #334155;
            font-size: .88rem;
            font-weight: 650;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            border: 1px solid #CBD5E1;
            border-radius: 12px;
            background: var(--surface);
            color: var(--ink);
            box-shadow: 0 1px 2px rgba(15, 23, 42, .03);
            transition: border-color .18s ease, box-shadow .18s ease;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: var(--brand);
            box-shadow: 0 0 0 3px rgba(37, 99, 235, .12);
        }

        [data-testid="stTextArea"] textarea {
            min-height: 700px;
            padding: 1.15rem;
            font-size: .98rem;
            line-height: 1.7;
            resize: vertical;
        }

        [data-testid="stForm"] {
            padding: 1.5rem;
            border: 1px solid var(--line);
            border-radius: 18px;
            background: rgba(255, 255, 255, .92);
            box-shadow: 0 12px 30px rgba(15, 23, 42, .045);
        }

        [data-testid="stFormSubmitButton"] button {
            min-height: 3.15rem;
            border: 1px solid var(--brand);
            border-radius: 11px;
            background: var(--brand);
            color: #FFFFFF;
            font-size: .98rem;
            font-weight: 700;
            box-shadow: 0 7px 16px rgba(37, 99, 235, .20);
            transition: transform .18s ease, background .18s ease, box-shadow .18s ease;
        }

        [data-testid="stFormSubmitButton"] button:hover {
            border-color: var(--brand-dark);
            background: var(--brand-dark);
            color: #FFFFFF;
            box-shadow: 0 10px 24px rgba(37, 99, 235, .28);
            transform: translateY(-1px);
        }

        [data-testid="stFormSubmitButton"] button:active {
            transform: translateY(0);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(7, minmax(125px, 1fr));
            gap: .8rem;
            margin-bottom: .75rem;
        }

        .stat-card {
            min-width: 0;
            padding: 1.1rem 1rem;
            border: 1px solid var(--line);
            border-radius: 14px;
            background: var(--surface);
            box-shadow: 0 5px 14px rgba(15, 23, 42, .045);
        }

        .stat-card__label {
            overflow: hidden;
            margin-bottom: .45rem;
            color: var(--muted);
            font-size: .7rem;
            font-weight: 700;
            letter-spacing: .06em;
            text-overflow: ellipsis;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .stat-card__value {
            overflow: hidden;
            color: var(--ink);
            font-size: clamp(1.35rem, 2vw, 1.85rem);
            font-weight: 760;
            letter-spacing: -.035em;
            line-height: 1.1;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        [data-testid="stDownloadButton"] button {
            min-height: 2.85rem;
            border: 1px solid #CBD5E1;
            border-radius: 10px;
            background: var(--surface);
            color: #1E293B;
            font-weight: 650;
            box-shadow: 0 2px 7px rgba(15, 23, 42, .04);
            transition: border-color .18s ease, color .18s ease, transform .18s ease;
        }

        [data-testid="stDownloadButton"] button:hover {
            border-color: var(--brand);
            color: var(--brand);
            transform: translateY(-1px);
        }

        [data-testid="stExpander"] {
            overflow: hidden;
            margin-bottom: .75rem;
            border: 1px solid var(--line);
            border-radius: 13px;
            background: var(--surface);
            box-shadow: 0 3px 10px rgba(15, 23, 42, .035);
        }

        [data-testid="stExpander"] details summary {
            padding: .3rem .35rem;
        }

        [data-testid="stExpander"] details summary:hover {
            background: #F8FAFC;
        }

        .prompt-text {
            margin: .3rem 0 .75rem;
            padding: 1.15rem;
            border: 1px solid #E8EDF3;
            border-radius: 10px;
            background: var(--surface-soft);
            color: #1E293B;
            font-size: .96rem;
            line-height: 1.72;
            white-space: pre-wrap;
        }

        [data-testid="stAlert"] {
            border-radius: 12px;
        }

        @media (max-width: 1100px) {
            .block-container { padding: 2.5rem 2rem 4rem; }
            .stats-grid { grid-template-columns: repeat(4, minmax(130px, 1fr)); }
        }

        @media (max-width: 720px) {
            .block-container { padding: 1.75rem 1rem 3rem; }
            .hero { margin-bottom: 1.5rem; }
            .hero__benefits span { display: block; }
            [data-testid="stForm"] { padding: 1rem; border-radius: 14px; }
            [data-testid="stTextArea"] textarea { min-height: 560px; }
            .stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def formatar_tempo_interface(segundos: int) -> str:
    """Formata intervalos para exibição sem interferir no motor."""
    horas, resto = divmod(segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    if horas:
        return f"{horas}:{minutos:02d}:{segundos:02d}"
    return f"{minutos}:{segundos:02d}"


def botao_copiar(texto: str, rotulo: str, chave: str, largura_total: bool = False) -> None:
    """Renderiza um botão de cópia isolado com fallback para navegadores antigos."""
    texto_json = json.dumps(texto, ensure_ascii=False).replace("</", "<\\/")
    largura = "100%" if largura_total else "auto"
    componentes = f"""
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
        button {{
            width: {largura}; min-height: 40px; padding: 0 15px;
            border: 1px solid #CBD5E1; border-radius: 9px;
            background: #FFFFFF; color: #334155; cursor: pointer;
            font-size: 13px; font-weight: 650;
            transition: border-color .18s ease, color .18s ease, background .18s ease;
        }}
        button:hover {{ border-color: #2563EB; color: #2563EB; background: #F8FAFF; }}
        button.copied {{ border-color: #16A34A; color: #15803D; background: #F0FDF4; }}
    </style>
    <button id="copy-{chave}" type="button">{html.escape(rotulo)}</button>
    <textarea id="fallback-{chave}" aria-hidden="true" style="position:fixed;opacity:0;pointer-events:none"></textarea>
    <script>
        const button = document.getElementById('copy-{chave}');
        const content = {texto_json};
        button.addEventListener('click', async () => {{
            try {{
                await navigator.clipboard.writeText(content);
            }} catch (_) {{
                const fallback = document.getElementById('fallback-{chave}');
                fallback.value = content;
                fallback.focus();
                fallback.select();
                document.execCommand('copy');
            }}
            button.textContent = '✓ Copiado';
            button.classList.add('copied');
            window.setTimeout(() => {{
                button.textContent = {json.dumps(rotulo, ensure_ascii=False)};
                button.classList.remove('copied');
            }}, 1800);
        }});
    </script>
    """
    components.html(componentes, height=44, scrolling=False)


def cards_estatisticas(estatisticas: dict[str, object]) -> None:
    metricas = (
        ("Tempo", estatisticas["tempo"]),
        ("Palavras", estatisticas["palavras"]),
        ("Prompts", estatisticas["prompts"]),
        ("Média", f"{estatisticas['media']:.2f}"),
        ("Menor Prompt", estatisticas["menor_prompt"]),
        ("Maior Prompt", estatisticas["maior_prompt"]),
        ("Desvio Padrão", f"{estatisticas['desvio_padrao']:.2f}"),
    )
    cards = "".join(
        "<div class='stat-card'>"
        f"<div class='stat-card__label'>{html.escape(str(rotulo))}</div>"
        f"<div class='stat-card__value'>{html.escape(str(valor))}</div>"
        "</div>"
        for rotulo, valor in metricas
    )
    st.markdown(f"<div class='stats-grid'>{cards}</div>", unsafe_allow_html=True)


st.markdown(
    """
    <header class="hero">
        <div class="hero__eyebrow"><span class="hero__mark"></span>Segmentação profissional</div>
        <h1>Divisor de Roteiros</h1>
        <p class="hero__subtitle">
            Transforme qualquer roteiro em segmentos de aproximadamente 8 segundos
            preservando integralmente o texto original.
        </p>
        <div class="hero__benefits">
            <span>✓ Texto preservado integralmente</span> &nbsp;•&nbsp;
            <span>✓ Segmentação determinística</span> &nbsp;•&nbsp;
            <span>✓ Exportação em TXT, Markdown e CSV</span>
        </div>
    </header>
    """,
    unsafe_allow_html=True,
)

with st.form("formulario_roteiro", clear_on_submit=False):
    tempo = st.text_input(
        "Duração do voice-over",
        placeholder="Ex.: 12:30 ou 01:12:30",
        help="Informe a duração exata no formato MM:SS ou HH:MM:SS.",
    )
    roteiro = st.text_area(
        "Roteiro",
        height=700,
        placeholder="Cole aqui o roteiro completo...",
        help="O conteúdo e a ordem de todos os tokens serão preservados.",
    )
    enviar = st.form_submit_button("Dividir roteiro", type="primary", use_container_width=True)

if enviar:
    try:
        segmentador = Segmentador(roteiro, tempo)
        segmentos = segmentador.dividir()
        estatisticas = segmentador.estatisticas()
        st.session_state["resultado"] = (segmentador, segmentos, estatisticas)
    except (ValueError, RuntimeError) as erro:
        st.session_state.pop("resultado", None)
        st.error(str(erro), icon="⚠️")

if "resultado" in st.session_state:
    segmentador, segmentos, estatisticas = st.session_state["resultado"]
    conteudo_txt = segmentador.exportar_txt().decode("utf-8")

    st.markdown(
        "<div class='section-heading'><h2>Visão geral</h2>"
        "<p>Resumo da distribuição gerada para o roteiro.</p></div>",
        unsafe_allow_html=True,
    )
    cards_estatisticas(estatisticas)

    st.markdown(
        "<div class='section-heading'><h2>Exportar resultado</h2>"
        "<p>Baixe todos os segmentos no formato mais adequado ao seu fluxo.</p></div>",
        unsafe_allow_html=True,
    )
    downloads = st.columns(3, gap="medium")
    downloads[0].download_button(
        "📄  TXT",
        segmentador.exportar_txt(),
        "prompts.txt",
        "text/plain",
        use_container_width=True,
    )
    downloads[1].download_button(
        "📝  Markdown",
        segmentador.exportar_markdown(),
        "prompts.md",
        "text/markdown",
        use_container_width=True,
    )
    downloads[2].download_button(
        "📊  CSV",
        segmentador.exportar_csv(),
        "prompts.csv",
        "text/csv",
        use_container_width=True,
    )

    st.markdown(
        "<div class='section-heading'><h2>Prompts</h2>"
        f"<p>{len(segmentos)} segmentos prontos para uso.</p></div>",
        unsafe_allow_html=True,
    )
    botao_copiar(conteudo_txt, "📋  Copiar tudo", "todos", largura_total=True)

    for segmento in segmentos:
        inicio = formatar_tempo_interface(segmento["inicio_tempo"])
        fim = formatar_tempo_interface(segmento["fim_tempo"])
        titulo = (
            f"PROMPT {segmento['numero']:03d}  ·  "
            f"{segmento['palavras']} palavras  ·  {inicio} – {fim}"
        )
        with st.expander(titulo, expanded=segmento["numero"] <= 2):
            st.markdown(
                f"<div class='prompt-text'>{html.escape(segmento['texto'])}</div>",
                unsafe_allow_html=True,
            )
            botao_copiar(
                segmento["texto"],
                "📋  Copiar",
                f"prompt-{segmento['numero']}",
            )
