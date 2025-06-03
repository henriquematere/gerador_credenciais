import streamlit as st
import datetime
from unidecode import unidecode

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

st.set_page_config(page_title="Gerador de Credenciais", layout="wide")
st.title("⚙️ Gerador de Credenciais de Colaboradores")
st.markdown("Preencha os dados do colaborador e selecione os sistemas para gerar as credenciais.")

mapa_opcao_formatada_para_setor = {f"{setor} (CC: {cc})": setor for setor, cc in MAPA_CENTRO_CUSTO.items()}
opcoes_setor_formatadas_sorted = sorted(list(mapa_opcao_formatada_para_setor.keys()))
setores_para_selectbox = [""] + opcoes_setor_formatadas_sorted

with st.form("formulario_gerador_credenciais"):
    nome_completo_colab = st.text_input("Nome Completo do Colaborador*", placeholder="Ex: Fulano Siclano da Silva", key="nome_colab")
    setor_selecionado_formatado = st.selectbox(
        "Setor (com Centro de Custo)*", 
        options=setores_para_selectbox, 
        key="setor_colab_fmt", 
        placeholder="Selecione ou digite nome/CC do setor"
    )
    
    st.markdown("##### Selecionar Sistemas:")
    col1, col2, col3 = st.columns(3)
    with col1:
        cb_cloud = st.checkbox("Senior Cloud", value=True, key="cb_cloud_sys")
    with col2:
        cb_senior = st.checkbox("Senior Principal", value=True, key="cb_senior_sys")
    with col3:
        cb_glpi = st.checkbox("GLPI Chamados", value=True, key="cb_glpi_sys")
    
    botao_gerar = st.form_submit_button("Gerar Credenciais")

if botao_gerar:
    erro = False
    setor_real_colab = None 

    if not nome_completo_colab: 
        st.error("O campo 'Nome Completo do Colaborador' é obrigatório.")
        erro = True
    
    if not setor_selecionado_formatado:
        st.error("O campo 'Setor' é obrigatório.")
        erro = True
    else:
        setor_real_colab = mapa_opcao_formatada_para_setor.get(setor_selecionado_formatado)
        if not setor_real_colab:
            st.error("Seleção de setor inválida.")
            erro = True
    
    if not erro and setor_real_colab:
        primeiro_nome, ultimo_sobrenome, primeiro_nome_cap = processar_nome_completo(nome_completo_colab)
        setor_normalizado = normalizar_texto(setor_real_colab)

        output_lines = []
        first_section_added = False

        if cb_cloud:
            if first_section_added: output_lines.append("")
            user_c, pass_c = gerar_credenciais_cloud(primeiro_nome, ultimo_sobrenome, setor_normalizado)
            output_lines.append(f"Acessar a Cloud: [{URL_CLOUD.split('//')[1].split('/')[0]}]({URL_CLOUD})")
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
            output_lines.append(f"Para realizar chamados para o TI: [{URL_GLPI.split('//')[1].split('/')[0]}]({URL_GLPI})")
            output_lines.append(f"Usuário: `{user_g}` Senha: `{pass_g}`")
            first_section_added = True
        
        if not output_lines:
            st.info("Nenhum sistema selecionado para gerar credenciais.")
        else:
            output_string = "\n".join(output_lines)
            st.markdown(output_string)
            
    elif not erro and not setor_real_colab:
        st.warning("Problema ao identificar o setor selecionado. Verifique a seleção.")