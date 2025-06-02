import streamlit as st
import datetime
from unidecode import unidecode # Para remover acentos

# --- Dicionários e Constantes ---
MAPA_CENTRO_CUSTO = {
    "Comercial": "1010",
    "Supervisão de Vendas": "1020",
    "CIV": "1030",
    "E-Commerce": "1040",
    "Marketing": "1050",
    "Logística": "1060",
    "Desenvolvimento de Produtos": "1070",
    "Customização": "1080",
    "Promotores de Vendas": "1090",
    "Transporte Aéreo": "1091",
    "Gestão Industrial": "2010",
    "PCP": "2020",
    "Qualidade": "2030",
    "Eng. Proc. Produtos": "2040",
    "Manutenção Predial": "2050",
    "Manutenção": "2060",
    "Expedição": "2070",
    "Almoxarifado": "2080",
    "Diretoria": "4010",
    "Administrativo": "4020",
    "Importação": "4030",
    "Exportação": "4035",
    "Financeiro": "4040",
    "RH": "4050",
    "TI": "4060",
    "Compras": "4070",
    "Seg. do Trabalho": "4080",
    "Portaria": "4090",
    "Limpeza": "4100",
    "Cadastro": "4110",
    "OOE": "4120",
    "Facilities": "4121",
    "Acoplagem": "6010",
    "Baralho": "6020",
    "Blister": "6030",
    "Brasilflex": "6040",
    "Corte e Solda": "6050",
    "Corte Vinco": "6060",
    "Embalagens Kraft": "6070",
    "Envase": "6080",
    "Flexografia": "6090",
    "Guilhotina": "6100",
    "Impressão": "6110",
    "Injetora": "6120",
    "Marcenaria": "6140",
    "Montagem": "6150",
    "Montagem II": "6160",
    "Pintura": "6170",
    "Termoformadora": "6180",
    "Vinil": "6190",
}

URL_CLOUD = "https://antares-s3.seniorcloud.com.br/?utm_medium=email&_hsenc=p2ANqtz-9VYNrv3-RJ4vxW-PlKV0Yt-sGD_3pfWGutm2VbCMZ0XjlDWMcQ3evC1qPxH2s6AE0l7zz8443jyxq3JrK1c7vxnaw4pXQzL33e0DZYAUq145Xbguc&_hsmi=335519716&utm_content=335519716&utm_source=hs_email"
URL_GLPI = "https://glpi.masfatech.com.br/glpi/marketplace/formcreator/front/formlist.php"

# --- Funções Auxiliares ---
def normalizar_texto(texto):
    return unidecode(texto).lower()

def processar_nome_completo(nome_completo):
    partes_nome = nome_completo.strip().split()
    artigos = ["de", "da", "do", "dos", "e"]
    nomes_validos = [p for p in partes_nome if p.lower() not in artigos]
    if not nomes_validos: return "", "", ""
    primeiro_nome_original = nomes_validos[0]
    primeiro_nome_norm = normalizar_texto(primeiro_nome_original)
    ultimo_sobrenome_norm = normalizar_texto(nomes_validos[-1]) if len(nomes_validos) > 1 else primeiro_nome_norm
    return primeiro_nome_norm, ultimo_sobrenome_norm, primeiro_nome_original.capitalize()

# --- Funções de Geração de Credenciais ---
def gerar_credenciais_cloud(primeiro_nome_norm, ultimo_sobrenome_norm, setor_norm):
    usuario_cloud = f"gala.{primeiro_nome_norm[0]}{ultimo_sobrenome_norm}"
    ano_atual_curto = str(datetime.datetime.now().year)[-2:]
    nome_str = primeiro_nome_norm if primeiro_nome_norm else "xxxx"
    pass_nome_part = nome_str[0].upper() + (nome_str[1:4].lower() if len(nome_str) > 1 else "xxx")
    pass_nome_part = (pass_nome_part + "xxxx")[:4]
    setor_str = setor_norm if setor_norm else "xxx"
    pass_setor_part = setor_str[0].upper() + (setor_str[1:3].lower() if len(setor_str) > 1 else "xx")
    pass_setor_part = (pass_setor_part + "xxx")[:3]
    senha_cloud = f"{pass_nome_part}@{pass_setor_part}#{ano_atual_curto}!"
    return usuario_cloud, senha_cloud

def gerar_credenciais_senior(primeiro_nome_norm, ultimo_sobrenome_norm):
    usuario_senior = f"{primeiro_nome_norm}.{ultimo_sobrenome_norm}"
    senha_senior = f"Gala@{datetime.datetime.now().year}"
    return usuario_senior, senha_senior

def gerar_credenciais_glpi(primeiro_nome_norm, ultimo_sobrenome_norm, primeiro_nome_cap_para_senha):
    usuario_glpi = f"{primeiro_nome_norm}.{ultimo_sobrenome_norm}"
    senha_glpi = f"{primeiro_nome_cap_para_senha}@123"
    return usuario_glpi, senha_glpi

# --- Interface Streamlit ---
st.set_page_config(page_title="Gerador de Credenciais", layout="wide")
st.title("⚙️ Gerador de Credenciais de Colaboradores")
st.markdown("Selecione a ação desejada e preencha os dados do colaborador.")

modo_operacao = st.radio(
    "Selecione a Ação Desejada:",
    ("Criar Novas Credenciais Completas", "Redefinir Apenas Senha da Cloud"),
    key="modo_operacao_key",
    horizontal=True # Para melhor visualização do radio
)

# Define opções de setor uma vez
setores_disponiveis = [""] + sorted(list(MAPA_CENTRO_CUSTO.keys()))

if modo_operacao == "Criar Novas Credenciais Completas":
    st.subheader("Modo: Criar Novas Credenciais Completas")
    with st.form("formulario_colaborador_completo"):
        nome_completo_colab = st.text_input("Nome Completo do Colaborador*", placeholder="Ex: Thalita Rosa Cazão", key="nome_full")
        email_colab = st.text_input("E-mail do Colaborador*", placeholder="Ex: thalita.rosa@empresa.com.br", key="email_full")
        setor_colab = st.selectbox("Setor*", options=setores_disponiveis, key="setor_full", help="Selecione o setor do colaborador.")
        usuario_referencia_colab = st.text_input("Usuário de Referência (para GLPI)*", placeholder="Ex: Kaiky Souza", key="ref_full")
        
        st.markdown("##### Selecionar Sistemas (para criação completa):")
        col1, col2, col3 = st.columns(3)
        with col1:
            cb_cloud = st.checkbox("Senior Cloud", value=True, key="cb_cloud_full")
        with col2:
            cb_senior = st.checkbox("Senior Principal", value=True, key="cb_senior_full")
        with col3:
            cb_glpi = st.checkbox("GLPI Chamados", value=True, key="cb_glpi_full")
        
        botao_gerar_completo = st.form_submit_button("Gerar Credenciais Completas")

    if botao_gerar_completo:
        erro_completo = False
        if not nome_completo_colab: st.error("O campo 'Nome Completo' é obrigatório."); erro_completo = True
        if not email_colab: st.error("O campo 'E-mail' é obrigatório."); erro_completo = True
        if not setor_colab: st.error("O campo 'Setor' é obrigatório."); erro_completo = True
        if cb_glpi and not usuario_referencia_colab: st.error("O 'Usuário de Referência' é obrigatório para GLPI."); erro_completo = True

        if not erro_completo:
            primeiro_nome, ultimo_sobrenome, primeiro_nome_cap = processar_nome_completo(nome_completo_colab)
            setor_normalizado = normalizar_texto(setor_colab)

            output_lines = []
            first_section_added = False

            if cb_cloud:
                if first_section_added: output_lines.append("")
                user_c, pass_c = gerar_credenciais_cloud(primeiro_nome, ultimo_sobrenome, setor_normalizado)
                output_lines.append(f"Acessar a Cloud: [{URL_CLOUD.split('//')[1].split('/')[0]}]({URL_CLOUD})") # Texto do link mais curto
                output_lines.append(f"Usuário: `{user_c}` Senha: `{pass_c}`")
                first_section_added = True
            if cb_senior:
                if first_section_added: output_lines.append("")
                user_s, pass_s = gerar_credenciais_senior(primeiro_nome, ultimo_sobrenome)
                output_lines.append(f"Senior:")
                output_lines.append(f"Usuário: `{user_s}` Senha: `{pass_s}`")
                first_section_added = True
            if cb_glpi:
                if first_section_added: output_lines.append("")
                nome_formatado_para_senha_glpi = unidecode(primeiro_nome_cap)
                user_g, pass_g = gerar_credenciais_glpi(primeiro_nome, ultimo_sobrenome, nome_formatado_para_senha_glpi)
                output_lines.append(f"Para realizar chamados para o TI: [{URL_GLPI.split('//')[1].split('/')[0]}]({URL_GLPI})") # Texto do link mais curto
                output_lines.append(f"Usuário: `{user_g}` Senha: `{pass_g}`")
                first_section_added = True
            
            if not output_lines:
                st.info("Nenhum sistema selecionado para gerar credenciais.")
            else:
                output_string = "\n".join(output_lines)
                st.markdown(output_string)
                nome_arquivo_download = normalizar_texto(nome_completo_colab.split()[0]) if nome_completo_colab else "credenciais"
                st.download_button(
                    label="Baixar Credenciais em TXT",
                    data=output_string.replace("`", ""),
                    file_name=f"credenciais_{nome_arquivo_download}.txt",
                    mime="text/plain"
                )
        else:
            st.warning("Corrija os erros no formulário.")

elif modo_operacao == "Redefinir Apenas Senha da Cloud":
    st.subheader("Modo: Redefinir Apenas Senha da Cloud")
    with st.form("formulario_reset_cloud"):
        nome_completo_colab_reset = st.text_input("Nome Completo do Colaborador*", key="nome_reset", placeholder="Ex: Thalita Rosa Cazão")
        setor_colab_reset = st.selectbox("Setor do Colaborador*", options=setores_disponiveis, key="setor_reset", help="Selecione o setor para a regra da senha da Cloud.")
        
        botao_reset_cloud = st.form_submit_button("Gerar Nova Senha Cloud")

    if botao_reset_cloud:
        erro_reset = False
        if not nome_completo_colab_reset: st.error("O campo 'Nome Completo' é obrigatório."); erro_reset = True
        if not setor_colab_reset: st.error("O campo 'Setor' é obrigatório."); erro_reset = True
        
        if not erro_reset:
            primeiro_nome, ultimo_sobrenome, _ = processar_nome_completo(nome_completo_colab_reset)
            setor_normalizado = normalizar_texto(setor_colab_reset)
            
            if not primeiro_nome or not setor_normalizado :
                st.error("Não foi possível processar o nome ou setor fornecido.")
            else:
                usuario_cloud, nova_senha_cloud = gerar_credenciais_cloud(primeiro_nome, ultimo_sobrenome, setor_normalizado)
                
                st.success(f"Nova senha da Cloud gerada para: **{nome_completo_colab_reset}**")
                reset_output_lines = []
                reset_output_lines.append(f"Usuário Cloud: `{usuario_cloud}`")
                reset_output_lines.append(f"Nova Senha Cloud: `{nova_senha_cloud}`")
                
                st.markdown("\n".join(reset_output_lines))
                st.text_area("Nova Senha Cloud (para copiar):", nova_senha_cloud, height=50, key="pwd_copy_area_cloud_reset", help="Selecione e copie a senha.")
        else:
            st.warning("Corrija os erros no formulário.")

st.markdown("---")
st.caption(f"Parceiro de Programação - Gerador de Credenciais v1.2 (Atualizado em {datetime.date.today().strftime('%d/%m/%Y')})")