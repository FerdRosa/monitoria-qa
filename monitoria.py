import streamlit as st
import google.generativeai as genai

# --- CONFIGURAÇÃO ---
# Pega a chave dos segredos do Streamlit (nuvem)
API_KEY = st.secrets["GEMINI_KEY"] 

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

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

    # LISTA COMPLETA DE MOTIVOS
    lista_solicitacoes = [
        "2° VIA",
        "Falta de Agua::Falta de Água - Local",
        "Falta de Agua::Falta de Água - Massiva",
        "Falta de Agua::Pedir Caminhão Pipa",
        "Religação::A pedido",
        "Religação::Após troca de titularidade",
        "Religação::por débito",
        "Religação::Religação contestável",
        "Vazamento::Cavalete",
        "Vazamento::Ramal",
        "Vazamento::Rede",
        "Consumo Elevado::Cobrança devida de esgoto",
        "Consumo Elevado::Consumo do cliente",
        "Consumo Elevado::Vazamento interno",
        "Consumo Final::Asfalto",
        "Consumo Final::Cavalete",
        "Consumo Final::Ramal",
        "Consumo Final::Terra",
        "Acesso::à agencia virtual (Cadastro)",
        "Acesso::ao App (Reset de E-mail)",
        "Aferição de medidor",
        "Ligação Nova::Estudo de Viabilidade Técnica de água",
        "Ligação Nova::Estudo de Viabilidade Técnica de esgoto",
        "Ligação Nova::Extensão de Rede de água",
        "Ligação Nova::Extensão de Rede de esgoto",
        "Ligação Nova::Individualização de abastecimento de água",
        "Ligação Nova::Ligação Nova de Água",
        "Ligação Nova::Ligação Nova de Esgoto",
        "Ligação Nova::Retrabalho de ligação nova de água",
        "Ligação Nova::Verificação de existência de rede",
        "Tarifa Social::Recadastrar",
        "Tarifa Social::Requerer",
        "Troca de titularidade",
        "Viabilidade::DPA/DPE",
        "Viabilidade::Empreendimentos",
        "Viabilidade::Faturamento",
        "Viabilidade::Hidrantes",
        "Viabilidade::Ligação Definitiva",
        "Viabilidade::Ligação Provisória",
        "Viabilidade::Manutenção em geral (água e esgoto)",
        "Viabilidade::OCA/OCE",
        "Cobrança::Carta de anuência",
        "Cobrança::Cliente desconhece endereço",
        "Cobrança::Cliente possui débitos",
        "Cobrança::Cliente sem débitos",
        "Certidão Negativa de Débitos",
        "Contestação de Fatura::Alteração de categoria",
        "Contestação de Fatura::Caminhão pipa",
        "Contestação de Fatura::Cobrança de esgoto indevida",
        "Contestação de Fatura::Cobrança indevida de serviços",
        "Contestação de Fatura::Despejo industrial",
        "Contestação de Fatura::Divergência na quantidade de economia",
        "Contestação de Fatura::Divergência no HD",
        "Contestação de Fatura::Erro na leitura",
        "Contestação de Fatura::Leitura por média",
        "Contestação de Fatura::Matrícula inativa / Desativada",
        "Contestação de Fatura::Substituição de HD",
        "Contestação de Fatura::Vazamento interno",
        "Débito automático",
        "Estrututa tarifária",
        "Informar N° Da matricula",
        "Informar Pagamento",
        "Cancelamento de corte::Contestação em análise",
        "Cancelamento de corte::Quitação de débitos",
        "Ressarcimento",
        "Alterar Vencimento fatura",
        "Tarifa Esgoto:: Ligação como corte a pedido cobrando esgoto",
        "Tarifa Esgoto::Disponibilidade",
        "Quantidade M3 consumidos",
        "Pagamento em Duplicidade",
        "Negociação::Cliente ciente do débito",
        "Negociação::Cliente não é o titular",
        "Negociação::Não concorda com os débitos",
        "Negociação::Parcelamento",
        "Negociação::Previsão de pagamento",
        "Negociação::Problemas financeiros",
        "Negociação::Processo juducial",
        "Negociação::Promessa de pagamento",
        "Negociação::Quitação a vista",
        "Negociação::Reparcelamento",
        "Negociação::Titular ausente",
        "Negociação::Titular falecido",
        "Correção cadastral::Alterar Dados de contato (telefone/e-mail)",
        "Correção cadastral::Alterar Dados pessoais (Nome,RG, CPF ou CNPJ, DN e filiação)",
        "Correção cadastral::Alterar Numero casa, N°, quadra, lote ou bairro",
        "Correção cadastral::Alterar número do cep",
        "Correção cadastral::Categoria",
        "Correção cadastral::Número de HD",
        "Correção cadastral::O.S de verificação cadastral",
        "Correção cadastral::Quantidade de economia",
        "Quantidade Economias",
        "Deslocamento de cavalete::Acima de 1,5m",
        "Deslocamento de cavalete::Acima de 1m",
        "Deslocamento de cavalete::Até 1 m",
        "Deslocamento de cavalete::Até de 1,5m",
        "Deslocamento de cavalete::Padronização de cavalete",
        "Desobstrução Agua::Ramal",
        "Desobstrução Esgoto::Ramal",
        "Desobstrução Esgoto::Rede",
        "Diversos::Agendamento de visitas",
        "Diversos::Caixa Postal (Voz)",
        "Diversos::Canais digitais",
        "Diversos::Cliente desligou (voz)",
        "Diversos::Cliente não responde (Voz)",
        "Diversos::E-mail Spam",
        "Diversos::Fora da área de concessão",
        "Diversos::Ligação muda (voz)",
        "Diversos::Ligação por engano (voz)",
        "Diversos::Lojas",
        "Diversos::Projetos sociais",
        "Diversos::Queda de ligação (Voz)",
        "Diversos::Recebimento de cartas",
        "Diversos::Recebimento de ofícios",
        "Diversos::Sistema inoperante",
        "Diversos::Teste de sistema",
        "Diversos::Vaga de emprego",
        "Informações de faturas",
        "Repasse de leitura",
        "Furto de hidrômetro",
        "Substituição de hidrômetro",
        "Irregularidade - Auto Denúncia",
        "Solicitação Recomposição/Repavimentação",
        "Status de solicitação",
        "Fotos de Fachada",
        "Informações de Localização",
        "Simulação de parcelmento",
        "Verificação de pressão",
        "Qualidade da água",
        "Corte indevido",
        "Retirada de entulho",
        "Retrabalho de substituição de HD",
        "Retrabalho de Corte",
        "Retrabalho de Religação",
        "Retrabalho de Cavalete",
        "Retrabalho de Ramal",
        "Retrabalho de Rede",
        "Informação de Troca de Titularidade",
        "Retrabalho de Ligação nova",
        "Retrabalho de deslocamento de cavalete",
        "Verificação de consumo",
        "Tarifa 10",
        "Vizinhança Saneada",
        "Débitos e faturas",
        "Contestação de fatura: Consumo Elevado",
        "Irregularidade - Denúncia",
        "Substituição de Registro",
        "Outros"
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
        "Registrou o atendimento no comentário",
        "Tabulação completa",
        "Repassou as informações corretas e completas",
        "Abriu a OS correta",
        "Demonstrou empatia e cordialidade",
        "Notificou o cliente devidamente",
        "Encaminhou para pesquisa de satisfação",
        "Verificou o histórico da URA antes de iniciar",
        "Manteve o cliente informado durante o atendimento",
        "Houve clareza na comunicação",
        "Questionou o cliente para entender melhor a necessidade",
        "Atendeu cliente com tempo de 01ª interação até 20 min",
        "Atendeu o cliente dentro dos 5 segundos",
        "Anexou as documentações",
        "Evitou expor de forma negativa a empresa",
        "Utilizou a saudação final corretamente",
        "Solicitou que cliente preencha a pesquisa de satisfação",
        "Questionou com cliente como pode ajudar",
        "Sinalizou o cliente corretamente",
        "Manteve a voz calma",
        "Questionou se cliente ainda têm duvidas ou deseja algo mais",
        
        
        
    ]

    lista_melhoria = [
        "Sinalizar o cliente ao se ausentar (mais de 1 min)",
        "Sinalizar o motivo da ausencia, agradecendo a espera ao retornar para o atendimento",
        "Verificar o histórico da URA antes de iniciar",
        "Utilizar saudação final informando canais digitais",
        "Utilizar script padrão para pedir pesquisa de satisfação",
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
        "Verificar as informações no sistema antes de repassar ao cliente",
        "Ter cuidado com a ortografia",
        "Evitar o uso de termos técnicos",
        "Deve anexar as documentações em sistema",
        "Deve buscar a causa raiz da tratativa",
        "Evitar expor a empresa de forma negativa",
        "Não jogar a responsabilidade para outro setores/cliente",
        "Adaptar a resposta à necessidade específica do cliente",
        "Não minimizar a tratativa",
        "Manter a calma e o respeito com o cliente",
        "Atender o cliente no tempo correto",
        "Questionae ao cliente como pode ajudar",
        "Evite termos técnicos com o cliente",
        "Transferir o cliente para pesquisa ao final do atendimento"        
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
                4. **IMPORTANTE:** Se o campo "Obs Extras" estiver preenchido, você DEVE integrar essa informação no meio do texto do Resumo para dar contexto ao atendimento (não apenas cole a frase no final, reescreva ela formalmente dentro da narrativa). Caso você veja que o texto em obs_extra é um ponto positivo, coloque ele também nos pontos positivos, mas se for um ponto de melhoria, coloque ele também nos pontos de melhoria.
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






