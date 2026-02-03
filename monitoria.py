import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO ---
# Pega a chave dos segredos do Streamlit (nuvem)
API_KEY = st.secrets["GEMINI_KEY"] 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Configuração da Página
st.set_page_config(page_title="Monitoria de Qualidade", layout="wide", page_icon="✅")

st.markdown("""
<style>
    .big-font { font-size:20px !important; font-weight: bold; }
    div[data-testid="stSidebar"] { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

st.title("📝 Gerador de Resumos de Monitoria")
st.markdown("Preencha os dados abaixo para gerar o texto padrão da empresa.")

# --- BARRA LATERAL (INPUTS) ---
with st.sidebar:
    st.header("Dados do Ticket")
    
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome do Colaborador")
    with col2:
        ticket = st.text_input("Nº do Ticket")

    # Lista extraída do seu arquivo
    lista_solicitacoes = [
        "Falta de Água", "Caminhão Pipa", "Débitos", "2ª Via", 
        "Contestação de Fatura", "Consultar Status", "Ligação Nova",
        "Troca de Titularidade", "Atualização Cadastral", "Vazamento",
        "Desobstrução de Esgoto", "Religação", "Fatura Digital",
        "Pagamento em Duplicidade", "Tarifa Social", "Supressão",
        "Cancelamento de OS", "Informar Pagamento", "Outros"
    ]
    solicitacao = st.selectbox("Tipo de Solicitação", lista_solicitacoes)
    if solicitacao == "Outros":
        solicitacao = st.text_input("Especifique a solicitação:")

    st.markdown("---")
    st.subheader("Avaliação")

    # Listas extraídas do seu arquivo
    lista_positivos = [
        "Iniciou o atendimento corretamente",
        "Finalizou o atendimento corretamente",
        "Realizou a confirmação/atualização dos dados cadastrais",
        "Sondagem completa em sistema",
        "Registrou o atendimento no comentário (SCAE)",
        "Tabulação completa",
        "Repassou as informações corretas e completas",
        "Abriu a OS correta",
        "Demonstrou empatia e cordialidade",
        "Notificou o cliente devidamente",
        "Encaminhou para pesquisa de satisfação",
        "Verificou o histórico da URA antes de iniciar",
        "Manteve o cliente informado durante o atendimento",
        "Houve clareza na comunicação",
        "Questionou o cliente para entender melhor a necessidade"
    ]

    lista_melhoria = [
        "Sinalizar o cliente ao se ausentar (mais de 1 min)",
        "Verificar o histórico da URA antes de iniciar",
        "Utilizar saudação final informando canais digitais",
        "Utilizar a macro para pedir pesquisa de satisfação",
        "Atualizar dados divergentes no cadastro",
        "Registrar comentário em todo atendimento",
        "Evitar uso da tag 'Outros' na tabulação",
        "Verificar tabulação antes de encerrar o ticket",
        "Não informar abertura de OS se não foi feita",
        "Explicar de forma clara para não restar dúvidas",
        "Ter cuidado com o mute (risadas/ruídos)",
        "Não abandonar o atendimento",
        "Realizar sondagem completa da tratativa",
        "Ter mais empatia com o cliente",
        "Verificar as informações no sistema antes de repassar ao cliente"
    ]

    acoes_feitas = st.multiselect("✅ Pontos Positivos", options=lista_positivos)
    acoes_faltantes = st.multiselect("⚠️ Pontos de Melhoria", options=lista_melhoria)
    
    obs_extra = st.text_area("Observações Extras (Opcional)", height=80, 
                             placeholder="Ex: Cliente estava muito nervoso; Atendente demorou para responder...")

    # Sugestão de nota: Começa com 100 e tira pontos se tiver melhoria (apenas visual)
    nota_sugerida = 100 if not acoes_faltantes else 0 
    nota = st.number_input("Nota de Monitoria", min_value=0, max_value=100, value=nota_sugerida, step=5)

    btn_gerar = st.button("✨ Gerar Relatório", type="primary", use_container_width=True)

# --- LÓGICA DE GERAÇÃO ---
if btn_gerar:
    if not nome or not ticket:
        st.error("⚠️ Por favor, preencha o Nome e o Ticket.")
    else:
        with st.spinner('Analisando padrão e escrevendo resumo...'):
            try:
                # Prompt com FEW-SHOT LEARNING (Ensinando com seus exemplos)
                prompt = f"""
                Você é um auditor de qualidade experiente. Sua tarefa é escrever um resumo de monitoria seguindo o padrão e o tom de voz dos exemplos abaixo.

                --- EXEMPLOS DE APRENDIZADO (Use como base de estilo) ---
                Exemplo 1 (Padrão Perfeito):
                Resumo: Cliente deseja informações sobre débitos, o atendente realizou a confirmação cadastral, em seguida, após uma sondagem em sistema, o mesmo repassou as informações corretas e completas para o cliente, finalizando e encaminhando para pesquisa.

                Exemplo 2 (Com erro grave):
                Resumo: Cliente deseja solicitar o caminhão pipa, a atendente, após realizar a confirmação dos dados cadastrais, realizou a sondagem correta, porém realizou a abertura da OS incorreta e em seguida passou a informação errada para a cliente.

                Exemplo 3 (Com Obs Extra - Contexto Específico):
                DADOS -> Obs Extra: "Cliente estava gritando muito e o sistema estava lento"
                Resumo: Cliente entrou em contato reclamando de falta de água, o mesmo estava muito alterado e gritando durante a ligação. A atendente tentou realizar a confirmação cadastral, porém devido à lentidão sistêmica, houve demora no repasse de informações, mas ao final o procedimento foi realizado.
                ---------------------------------------------------------

                AGORA, GERE O RELATÓRIO PARA ESTE CASO:
                - Nome: {nome}
                - Ticket: {ticket}
                - Solicitação: {solicitacao}
                - Positivos: {', '.join(acoes_feitas)}
                - Melhorias: {', '.join(acoes_faltantes)}
                - Obs Extras (CRUCIAL): {obs_extra}
                - Nota: {nota}

                REGRAS DE ESCRITA:
                1. O "Resumo" deve ser um parágrafo único, formal e narrativo.
                2. Use termos técnicos da empresa: "sondagem em sistema", "SCAE", "tabulação", "OS".
                3. Se houver pontos de melhoria, mencione no resumo o que faltou ou foi feito errado.
                4. **IMPORTANTE:** Se o campo "Obs Extras" estiver preenchido, você DEVE integrar essa informação no meio do texto do Resumo para dar contexto ao atendimento (não apenas cole a frase no final, reescreva ela formalmente dentro da narrativa).
                5. A saída deve ser APENAS o texto formatado abaixo, pronto para copiar.

                FORMATO FINAL:
                Nome: {nome}
                Ticket: {ticket}
                Solicitação: {solicitacao}

                Resumo: 
                [Escreva o resumo aqui]

                Pontos positivos:
                {chr(10).join(acoes_feitas) if acoes_feitas else ""}

                Pontos de melhoria:
                {chr(10).join(acoes_faltantes) if acoes_faltantes else ""}

                Nota de monitoria: {nota}
                """

                response = model.generate_content(prompt)
                
                st.subheader("Resultado Pronto:")
                st.text_area("Copie o texto abaixo:", value=response.text, height=400)
                st.success("Gerado com sucesso!")

            except Exception as e:
                st.error(f"Erro: {e}")

else:
    # Tela inicial vazia (instrução)

    st.info("👈 Preencha os dados na barra lateral para começar.")



