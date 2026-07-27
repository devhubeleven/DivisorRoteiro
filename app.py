"""Interface Streamlit do DivisorRoteiro."""

from __future__ import annotations

import html
import importlib
import json

import streamlit as st

import segmentador as modulo_segmentador


importlib.invalidate_caches()
modulo_segmentador = importlib.reload(modulo_segmentador)
Segmentador = modulo_segmentador.Segmentador

st.set_page_config(
    page_title="Divisor de Roteiros",
    page_icon="●",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "modo_escuro" not in st.session_state:
    st.session_state["modo_escuro"] = False

modo_escuro = bool(st.session_state["modo_escuro"])

st.markdown(
    """
    <style>
        :root {
            --brand: #0867F2;
            --brand-strong: #0057E7;
            --brand-soft: #EAF2FF;
            --page: #F8FAFD;
            --surface: #FFFFFF;
            --surface-soft: #FBFCFE;
            --ink: #101828;
            --text: #344054;
            --muted: #667085;
            --line: #E4EAF2;
            --line-strong: #D5DDE8;
            --shadow: 0 6px 24px rgba(15, 39, 76, .055);
        }

        html { scroll-behavior: smooth; }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 5% 0%, rgba(38, 132, 255, .07), transparent 34rem),
                var(--page);
            color: var(--ink);
        }

        [data-testid="stHeader"] { background: transparent; }
        [data-testid="stToolbar"] { right: 1rem; }

        .block-container {
            width: min(1400px, calc(100% - 48px));
            max-width: 1400px;
            padding: 2.35rem 0 5rem;
        }

        .hero { padding: .15rem 0 1.75rem; }

        .hero__eyebrow {
            display: flex;
            align-items: center;
            gap: .72rem;
            margin-bottom: 1rem;
            color: var(--brand);
            font-size: 1rem;
            font-weight: 850;
            letter-spacing: .145em;
            line-height: 1.2;
            text-transform: uppercase;
        }

        .hero__dot {
            width: .68rem;
            height: .68rem;
            flex: 0 0 auto;
            border-radius: 999px;
            background: var(--brand);
            box-shadow: 0 0 0 5px rgba(8, 103, 242, .11);
        }

        .hero h1 {
            margin: 0;
            color: var(--ink);
            font-size: clamp(3.25rem, 5.2vw, 5rem);
            font-weight: 900;
            letter-spacing: -.062em;
            line-height: .98;
        }

        .hero__subtitle {
            max-width: 980px;
            margin: 1.15rem 0 .95rem;
            color: var(--muted);
            font-size: 1rem;
            line-height: 1.6;
        }

        .hero__benefits {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: .5rem .85rem;
            color: var(--muted);
            font-size: .78rem;
            font-weight: 560;
        }

        .hero__benefits i {
            color: #A8B3C2;
            font-style: normal;
        }

        .theme-label {
            padding-top: .28rem;
            color: var(--text);
            font-size: .76rem;
            font-weight: 700;
            white-space: nowrap;
        }

        .theme-icon {
            padding-top: .16rem;
            color: var(--muted);
            font-size: .95rem;
            text-align: center;
        }

        [data-testid="stVerticalBlockBorderWrapper"] {
            border: 1px solid var(--line) !important;
            border-radius: 13px !important;
            background: var(--surface);
            box-shadow: var(--shadow);
        }

        [data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 1.1rem 1.2rem;
        }

        [data-testid="stToggle"] { margin: 0; }
        [data-testid="stToggle"] label { gap: 0; }
        [data-testid="stToggle"] p { display: none; }

        .field-label-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            min-height: 1.65rem;
            margin-bottom: .15rem;
        }

        .field-label {
            color: var(--ink);
            font-size: .82rem;
            font-weight: 760;
        }

        .word-count {
            color: var(--muted);
            font-size: .72rem;
            font-weight: 600;
        }

        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            border: 1px solid var(--line-strong);
            border-radius: 8px;
            background: var(--surface);
            color: var(--ink);
            box-shadow: inset 0 1px 2px rgba(16, 24, 40, .025);
            transition: border-color .16s ease, box-shadow .16s ease;
        }

        [data-testid="stTextInput"] input { min-height: 3rem; }

        [data-testid="stTextArea"] textarea {
            min-height: 330px;
            padding: 1rem;
            font-size: .94rem;
            line-height: 1.7;
            resize: vertical;
        }

        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus {
            border-color: var(--brand);
            box-shadow: 0 0 0 3px rgba(8, 103, 242, .11);
        }

        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder { color: #98A2B3; }

        [data-testid="stButton"] button[kind="primary"] {
            min-height: 3.65rem;
            border: 1px solid #075EDB;
            border-radius: 8px;
            background: linear-gradient(180deg, #1477FF 0%, #0062EC 100%);
            color: #FFFFFF;
            font-size: .96rem;
            font-weight: 760;
            box-shadow: 0 6px 14px rgba(0, 98, 236, .21);
            transition: transform .17s ease, box-shadow .17s ease, filter .17s ease;
        }

        [data-testid="stButton"] button[kind="primary"]:hover {
            border-color: #0054CF;
            color: #FFFFFF;
            filter: brightness(1.035);
            box-shadow: 0 9px 20px rgba(0, 98, 236, .28);
            transform: translateY(-1px);
        }

        [data-testid="stButton"] button[kind="primary"]:active { transform: translateY(0); }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(7, minmax(0, 1fr));
            gap: .72rem;
            margin: 1rem 0;
        }

        .stat-card {
            display: flex;
            align-items: center;
            min-width: 0;
            min-height: 92px;
            padding: .9rem;
            border: 1px solid var(--line);
            border-radius: 11px;
            background: var(--surface);
            box-shadow: var(--shadow);
        }

        .stat-card__icon {
            display: grid;
            width: 2.25rem;
            height: 2.25rem;
            flex: 0 0 2.25rem;
            place-items: center;
            margin-right: .7rem;
            border-radius: 999px;
            font-size: 1rem;
        }

        .stat-card__content { min-width: 0; }

        .stat-card__label {
            overflow: hidden;
            margin-bottom: .3rem;
            color: var(--muted);
            font-size: .61rem;
            font-weight: 650;
            line-height: 1.2;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .stat-card__value {
            overflow: hidden;
            color: var(--ink);
            font-size: 1.28rem;
            font-weight: 820;
            letter-spacing: -.035em;
            line-height: 1.05;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .section-title-row {
            display: flex;
            align-items: center;
            gap: .65rem;
            min-height: 2.2rem;
        }

        .section-title-row h2 {
            margin: 0;
            color: var(--ink);
            font-size: 1rem;
            font-weight: 800;
            letter-spacing: -.02em;
        }

        .count-badge {
            padding: .22rem .52rem;
            border-radius: 999px;
            background: #F0F3F7;
            color: var(--muted);
            font-size: .67rem;
            font-weight: 680;
        }

        [data-testid="stDownloadButton"] button {
            min-height: 2.55rem;
            border: 1px solid #72A9FF;
            border-radius: 7px;
            background: var(--surface);
            color: var(--brand);
            font-size: .73rem;
            font-weight: 680;
            box-shadow: none;
            transition: background .16s ease, transform .16s ease, box-shadow .16s ease;
        }

        [data-testid="stDownloadButton"] button:hover {
            border-color: var(--brand);
            background: var(--brand-soft);
            color: var(--brand);
            box-shadow: 0 4px 10px rgba(8, 103, 242, .10);
            transform: translateY(-1px);
        }

        .prompt-list-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 1.2rem 0 .65rem;
        }

        .prompt-list-heading h2 {
            margin: 0;
            color: var(--ink);
            font-size: 1.05rem;
            font-weight: 820;
        }

        [data-testid="stExpander"] {
            overflow: hidden;
            margin-bottom: .62rem;
            border: 1px solid var(--line);
            border-radius: 9px;
            background: var(--surface);
            box-shadow: 0 3px 12px rgba(15, 39, 76, .04);
            transition: border-color .16s ease, box-shadow .16s ease, transform .16s ease;
        }

        [data-testid="stExpander"]:hover {
            border-color: #C7D8EF;
            box-shadow: 0 7px 18px rgba(15, 39, 76, .075);
            transform: translateY(-1px);
        }

        [data-testid="stExpander"] details summary {
            min-height: 3.25rem;
            padding: .25rem .45rem;
        }

        [data-testid="stExpander"] details summary p {
            color: var(--ink);
            font-size: .78rem;
            font-weight: 760;
        }

        .prompt-time {
            margin: -.1rem 0 .65rem;
            color: var(--brand);
            font-size: .7rem;
            font-weight: 720;
        }

        .prompt-body {
            padding: .8rem .9rem;
            border: 1px solid var(--line);
            border-radius: 8px;
            background: var(--surface-soft);
            color: var(--text);
            font-size: .86rem;
            line-height: 1.65;
            white-space: pre-wrap;
        }

        [data-testid="stAlert"] { border-radius: 9px; }

        @media (max-width: 1120px) {
            .block-container { width: min(100% - 32px, 1400px); }
            .stats-grid { grid-template-columns: repeat(4, minmax(0, 1fr)); }
            .hero h1 { font-size: clamp(3rem, 6vw, 4.35rem); }
        }

        @media (max-width: 760px) {
            .block-container { width: calc(100% - 24px); padding-top: 1.25rem; }
            .hero { padding-bottom: 1rem; }
            .hero__eyebrow { font-size: .78rem; letter-spacing: .11em; }
            .hero h1 { font-size: clamp(2.6rem, 12vw, 3.6rem); }
            .hero__benefits { display: grid; gap: .25rem; }
            .hero__benefits i { display: none; }
            .stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
            [data-testid="stTextArea"] textarea { min-height: 420px; }
            [data-testid="stVerticalBlockBorderWrapper"] > div { padding: .9rem; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if modo_escuro:
    st.markdown(
        """
        <style>
            :root {
                --brand: #60A5FA;
                --brand-strong: #3B82F6;
                --brand-soft: #13294A;
                --page: #07101E;
                --surface: #101B2D;
                --surface-soft: #0B1423;
                --ink: #F8FAFC;
                --text: #D4DEEB;
                --muted: #93A4BA;
                --line: #26354A;
                --line-strong: #34445B;
                --shadow: 0 7px 24px rgba(0, 0, 0, .18);
                color-scheme: dark;
            }
            [data-testid="stAppViewContainer"] {
                background: radial-gradient(circle at 5% 0%, rgba(59, 130, 246, .14), transparent 34rem), var(--page);
            }
            [data-testid="stTextInput"] input,
            [data-testid="stTextArea"] textarea { background: #0B1423; color: var(--ink); }
            .count-badge { background: #1A2940; }
            [data-testid="stExpander"]:hover { border-color: #3D536E; }
            [data-testid="stDownloadButton"] button { background: var(--surface); }
        </style>
        """,
        unsafe_allow_html=True,
    )


def formatar_tempo_interface(segundos: int) -> str:
    horas, resto = divmod(segundos, 3600)
    minutos, segundos = divmod(resto, 60)
    if horas:
        return f"{horas}:{minutos:02d}:{segundos:02d}"
    return f"{minutos}:{segundos:02d}"


def botao_copiar(
    texto: str,
    rotulo: str,
    chave: str,
    largura_total: bool = False,
) -> None:
    texto_json = json.dumps(texto, ensure_ascii=False).replace("</", "<\\/")
    rotulo_json = json.dumps(rotulo, ensure_ascii=False)
    largura = "100%" if largura_total else "auto"
    fundo = "#101B2D" if modo_escuro else "#FFFFFF"
    hover = "#13294A" if modo_escuro else "#F2F7FF"
    borda = "#4773AD" if modo_escuro else "#72A9FF"
    componentes = f"""
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; background: transparent; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
        button {{
            width: {largura}; min-height: 40px; padding: 0 14px;
            border: 1px solid {borda}; border-radius: 7px;
            background: {fundo}; color: #2680FF; cursor: pointer;
            font-size: 12px; font-weight: 680;
            transition: background .16s ease, transform .16s ease, box-shadow .16s ease;
        }}
        button:hover {{ background: {hover}; box-shadow: 0 4px 10px rgba(8,103,242,.12); transform: translateY(-1px); }}
        button.copied {{ border-color: #22C55E; color: #16A34A; background: #F0FDF4; }}
    </style>
    <button id="copy-{chave}" type="button">{html.escape(rotulo)}</button>
    <textarea id="fallback-{chave}" style="position:fixed;opacity:0;pointer-events:none"></textarea>
    <script>
        const button = document.getElementById('copy-{chave}');
        const content = {texto_json};
        button.addEventListener('click', async () => {{
            try {{ await navigator.clipboard.writeText(content); }}
            catch (_) {{
                const fallback = document.getElementById('fallback-{chave}');
                fallback.value = content; fallback.focus(); fallback.select(); document.execCommand('copy');
            }}
            button.textContent = '✓ Copiado'; button.classList.add('copied');
            window.setTimeout(() => {{ button.textContent = {rotulo_json}; button.classList.remove('copied'); }}, 1600);
        }});
    </script>
    """
    st.iframe(
        componentes,
        width="stretch" if largura_total else "content",
        height=42,
        tab_index=-1,
    )


def cards_estatisticas(estatisticas: dict[str, object]) -> None:
    metricas = (
        ("◷", "Tempo", estatisticas["tempo"], "#EAF3FF", "#2E83FF"),
        ("▣", "Palavras", estatisticas["palavras"], "#EAFBF4", "#35B982"),
        ("▤", "Prompts", estatisticas["prompts"], "#F2EDFF", "#8B5CF6"),
        ("⌁", "Média", f"{estatisticas['media']:.2f}", "#FFF8E8", "#EFAE32"),
        ("↓", "Menor prompt", estatisticas["menor_prompt"], "#FFF0F3", "#F0647E"),
        ("↑", "Maior prompt", estatisticas["maior_prompt"], "#EAFBF3", "#29B475"),
        ("Σ", "Desvio padrão", f"{estatisticas['desvio_padrao']:.2f}", "#F2EDFF", "#805AD5"),
    )
    cards = "".join(
        "<div class='stat-card'>"
        f"<div class='stat-card__icon' style='background:{fundo};color:{cor}'>{icone}</div>"
        "<div class='stat-card__content'>"
        f"<div class='stat-card__label'>{html.escape(str(rotulo))}</div>"
        f"<div class='stat-card__value'>{html.escape(str(valor))}</div>"
        "</div></div>"
        for icone, rotulo, valor, fundo, cor in metricas
    )
    st.markdown(f"<div class='stats-grid'>{cards}</div>", unsafe_allow_html=True)


cabecalho, controle_tema = st.columns([8.5, 1.5], gap="large", vertical_alignment="top")
with cabecalho:
    st.markdown(
        """
        <header class="hero">
            <div class="hero__eyebrow"><span class="hero__dot"></span>SEGMENTAÇÃO PROFISSIONAL</div>
            <h1>Divisor de Roteiros</h1>
            <p class="hero__subtitle">Transforme qualquer roteiro em segmentos de 8 segundos preservando integralmente o texto original.</p>
            <div class="hero__benefits">
                <span>✓ Texto preservado integralmente</span><i>•</i>
                <span>✓ Segmentação determinística</span><i>•</i>
                <span>✓ Exportação em TXT, Markdown e CSV</span>
            </div>
        </header>
        """,
        unsafe_allow_html=True,
    )

with controle_tema:
    with st.container(border=True):
        legenda, sol, alternador, lua = st.columns([1.45, .45, 1.1, .45], gap="small")
        legenda.markdown("<div class='theme-label'>Tema</div>", unsafe_allow_html=True)
        sol.markdown("<div class='theme-icon'>☀</div>", unsafe_allow_html=True)
        alternador.toggle("Tema escuro", key="modo_escuro", label_visibility="collapsed")
        lua.markdown("<div class='theme-icon'>☾</div>", unsafe_allow_html=True)

with st.container(border=True):
    coluna_tempo, coluna_roteiro = st.columns([1.15, 4.85], gap="medium", vertical_alignment="top")
    with coluna_tempo:
        st.markdown("<div class='field-label-row'><span class='field-label'>Tempo do voice-over</span></div>", unsafe_allow_html=True)
        tempo = st.text_input(
            "Tempo do voice-over",
            placeholder="Ex.: 11:36",
            label_visibility="collapsed",
        )
    with coluna_roteiro:
        roteiro_atual = st.session_state.get("roteiro", "")
        total_digitado = len(roteiro_atual.split())
        st.markdown(
            "<div class='field-label-row'><span class='field-label'>Roteiro</span>"
            f"<span class='word-count'>{total_digitado} palavras</span></div>",
            unsafe_allow_html=True,
        )
        roteiro = st.text_area(
            "Roteiro",
            height=330,
            placeholder="Cole seu roteiro aqui...",
            key="roteiro",
            label_visibility="collapsed",
        )
    dividir = st.button("Dividir roteiro", type="primary", width="stretch")

if dividir:
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
    cards_estatisticas(estatisticas)

    downloads_coluna, prompts_coluna = st.columns([1, 1.18], gap="medium")
    with downloads_coluna:
        with st.container(border=True):
            st.markdown("<div class='section-title-row'><h2>Downloads</h2></div>", unsafe_allow_html=True)
            botoes = st.columns(3, gap="small")
            botoes[0].download_button("▧  Baixar TXT", segmentador.exportar_txt(), "prompts.txt", "text/plain", width="stretch")
            botoes[1].download_button("▧  Baixar Markdown", segmentador.exportar_markdown(), "prompts.md", "text/markdown", width="stretch")
            botoes[2].download_button("▦  Baixar CSV", segmentador.exportar_csv(), "prompts.csv", "text/csv", width="stretch")

    with prompts_coluna:
        with st.container(border=True):
            titulo_prompts, copiar_todos = st.columns([3, 1], gap="small", vertical_alignment="center")
            titulo_prompts.markdown(
                "<div class='section-title-row'><h2>Prompts</h2>"
                f"<span class='count-badge'>{len(segmentos)} prompts</span></div>",
                unsafe_allow_html=True,
            )
            with copiar_todos:
                botao_copiar(conteudo_txt, "▣  Copiar tudo", "todos", largura_total=True)

    st.markdown(
        "<div class='prompt-list-heading'><h2>Lista de prompts</h2>"
        f"<span class='count-badge'>{len(segmentos)} segmentos</span></div>",
        unsafe_allow_html=True,
    )

    for segmento in segmentos:
        inicio = formatar_tempo_interface(segmento["inicio_tempo"])
        fim = formatar_tempo_interface(segmento["fim_tempo"])
        titulo = f"PROMPT {segmento['numero']:03d}   ·   {segmento['palavras']} palavras"
        with st.expander(titulo, expanded=segmento["numero"] == 1):
            conteudo, copiar = st.columns([8.5, 1.5], gap="medium", vertical_alignment="top")
            with conteudo:
                st.markdown(f"<div class='prompt-time'>{inicio} – {fim}</div>", unsafe_allow_html=True)
                st.markdown(
                    f"<div class='prompt-body'>{html.escape(segmento['texto'])}</div>",
                    unsafe_allow_html=True,
                )
            with copiar:
                botao_copiar(segmento["texto"], "▣  Copiar", f"prompt-{segmento['numero']}", largura_total=True)
