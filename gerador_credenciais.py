import streamlit as st
import datetime
from unidecode import unidecode # Para remover acentos

# --- Dicionários e Constantes ---
MAPA_CENTRO_CUSTO = {
    "Fiscal": "4020",
    "TI": "1010",
    "Recursos Humanos": "3015",
    "Producao": "5050",
    # Adicione outros setores e seus centros de custo aqui
}

URL_CLOUD = "https://antares-s3.seniorcloud.com.br/?utm_medium=email&_hsenc=p2ANqtz-9VYNrv3-RJ4vxW-PlKV0Yt-sGD_3pfWGutm2VbCMZ0XjlDWMcQ3evC1qPxH2s6AE0l7zz8443jyxq3JrK1c7vxnaw4pXQzL33e0DZYAUq145Xbguc&_hsmi=335519716&utm_content=335519716&utm_source=hs_email"
URL_GLPI = "https://glpi.masfatech.com.br/glpi/marketplace/formcreator/front/formlist.php"

# --- Funções Auxiliares ---
def normalizar_texto(texto):
    # Remove acentos e converte para minúsculas.
    return unidecode(texto).lower()

def processar_nome_completo(nome_completo):
    # Extrai o primeiro nome e o último sobrenome, ignorando 'de', 'da', 'dos'.
    # Retorna (primeiro_nome_normalizado, ultimo_sobrenome_normalizado, primeiro_nome_original_capitalizado)
    partes_nome = nome_completo.strip().split()
    artigos = ["de", "da", "do", "dos", "e"]
    nomes_validos = [p for p in partes_nome if p.lower() not in artigos]

    if not nomes_validos:
        return "", "", ""

    primeiro_nome_original = nomes_validos[0]
    primeiro_nome_norm = normalizar_texto(primeiro_nome_original)
    
    ultimo_sobrenome_norm = ""
    if len(nomes_validos) > 1:
        ultimo_sobrenome_norm = normalizar_texto(nomes_validos[-1])
    else: # Caso de nome único, usa o próprio nome como sobrenome para lógicas
        ultimo_sobrenome_norm = primeiro_nome_norm 
        
    return primeiro_nome_norm, ultimo_sobrenome_norm, primeiro_nome_original.capitalize()

# --- Funções de Geração de Credenciais ---
def gerar_credenciais_cloud(primeiro_nome_norm, ultimo_sobrenome_norm, setor_norm):
    # Usuário Cloud: gala. + 1ª letra nome + ultimo sobrenome (REGRA MANTIDA)
    usuario_cloud = f"gala.{primeiro_nome_norm[0]}{ultimo_sobrenome_norm}"

    # Senha Cloud: Novo Padrão XXXX@YYY#NN! (Ex: Thal@Fis#25!)
    ano_atual_curto = str(datetime.datetime.now().year)[-2:]

    # Parte do nome (4 caracteres: 1ª Maiúscula, 3 minúsculas)
    nome_str = primeiro_nome_norm
    if not nome_str: nome_str = "xxxx" 
    
    pass_nome_part = nome_str[0].upper()
    if len(nome_str) > 1:
        pass_nome_part += nome_str[1:4].lower()
    else:
        pass_nome_part += "xxx" 
    pass_nome_part = (pass_nome_part + "xxxx")[:4]

    # Parte do setor (3 caracteres: 1ª Maiúscula, 2 minúsculas)
    setor_str = setor_norm
    if not setor_str: setor_str = "xxx"

    pass_setor_part = setor_str[0].upper()
    if len(setor_str) > 1:
        pass_setor_part += setor_str[1:3].lower()
    else:
        pass_setor_part += "xx"
    pass_setor_part = (pass_setor_part + "xxx")[:3]
    
    senha_cloud = f"{pass_nome_part}@{pass_setor_part}#{ano_atual_curto}!"
    
    return usuario_cloud, senha_cloud

def gerar_credenciais_senior(primeiro_nome_norm, ultimo_sobrenome_norm):
    # Usuário Senior: primeiro_nome.ultimo_sobrenome
    usuario_senior = f"{primeiro_nome_norm}.{ultimo_sobrenome_norm}"
    
    # Senha Senior: Gala@ANO
    ano_atual = str(datetime.datetime.now().year)
    senha_senior = f"Gala@{ano_atual}"
    return usuario_senior, senha_senior

def gerar_credenciais_glpi(primeiro_nome_norm, ultimo_sobrenome_norm, primeiro_nome_cap_original):
    # Usuário GLPI: primeiro_nome.ultimo_sobrenome (mesmo do Senior)
    usuario_glpi = f"{primeiro_nome_norm}.{ultimo_sobrenome_norm}"
    
    # Senha GLPI: NomeOriginalCapitalizado@123
    senha_glpi = f"{primeiro_nome_cap_original}@123" # Usa o primeiro nome original capitalizado e sem acentos
    return usuario_glpi, senha_glpi

# --- Interface Streamlit ---
st.set_page_config(page_title="Gerador de Credenciais", layout="wide")
st.title("⚙️ Gerador de Credenciais de Colaboradores")
st.markdown("Preencha os dados do colaborador para gerar as credenciais de acesso.")

with st.form("formulario_colaborador"):
    nome_completo_colab = st.text_input("Nome Completo do Colaborador*", placeholder="Ex: Henrique Matere Coelho Oliveira")
    email_colab = st.text_input("E-mail do Colaborador*", placeholder="Ex: henrique.matere@gala.com.br")
    
    setores_disponiveis = list(MAPA_CENTRO_CUSTO.keys())
    setor_colab = st.selectbox("Setor*", options=[""] + setores_disponiveis, help="Selecione o setor do colaborador.")
    
    usuario_referencia_colab = st.text_input("Usuário de Referência (para GLPI)*", placeholder="Ex: henrique.matere")

    st.subheader("Selecionar Sistemas:")
    cb_cloud = st.checkbox("Senior Cloud (Antares S3)", value=True)
    cb_senior = st.checkbox("Senior (Sistema Principal)", value=True)
    cb_glpi = st.checkbox("GLPI (Chamados TI)", value=True)

    botao_gerar = st.form_submit_button("Gerar Credenciais")

if botao_gerar:
    erro = False
    if not nome_completo_colab:
        st.error("O campo 'Nome Completo do Colaborador' é obrigatório.")
        erro = True
    if not email_colab: # Adicionar validação básica de e-mail seria bom no futuro
        st.error("O campo 'E-mail do Colaborador' é obrigatório.")
        erro = True
    if not setor_colab:
        st.error("O campo 'Setor' é obrigatório.")
        erro = True
    if not usuario_referencia_colab and cb_glpi: # Obrigatório apenas se GLPI for selecionado
        st.error("O campo 'Usuário de Referência' é obrigatório para acesso ao GLPI.")
        erro = True
    
    if not erro:
        st.success("Credenciais geradas com sucesso!")

        primeiro_nome, ultimo_sobrenome, primeiro_nome_cap = processar_nome_completo(nome_completo_colab)
        setor_normalizado = normalizar_texto(setor_colab)
        centro_custo = MAPA_CENTRO_CUSTO.get(setor_colab, "N/A (Setor não mapeado)")

        # Prepara a string de saída
        output_string = f"""
**Nome do colaborador:** {nome_completo_colab}
**Setor:** {setor_colab}
**Centro de Custos:** {centro_custo}
**E-mail:** {email_colab}
**Usuário de referência:** {usuario_referencia_colab}
---
"""

        if cb_cloud:
            user_c, pass_c = gerar_credenciais_cloud(primeiro_nome, ultimo_sobrenome, setor_normalizado)
            output_string += f"""
**Acessar a Cloud pelo link {URL_CLOUD} :**
    **Usuário:** `{user_c}`
    **Senha:** `{pass_c}`
---
"""
        if cb_senior:
            user_s, pass_s = gerar_credenciais_senior(primeiro_nome, ultimo_sobrenome)
            output_string += f"""
**Senior:**
    **Usuário:** `{user_s}`
    **Senha:** `{pass_s}`
---
"""
        if cb_glpi:
            # Para a senha do GLPI, usamos o primeiro nome original capitalizado e sem acentos
            primeiro_nome_glpi_norm_cap, _, _ = processar_nome_completo(unidecode(primeiro_nome_cap))

            user_g, pass_g = gerar_credenciais_glpi(primeiro_nome, ultimo_sobrenome, primeiro_nome_glpi_norm_cap)
            output_string += f"""
**Para realizar chamados para o TI, no {URL_GLPI} :**
    **Usuário:** `{user_g}`
    **Senha:** `{pass_g}`
"""
        st.markdown(output_string)

        st.download_button(
            label="Baixar Credenciais em TXT",
            data=output_string.replace("**", "").replace("`", ""), # Remove formatação markdown para TXT
            file_name=f"credenciais_{normalizar_texto(nome_completo_colab.split()[0])}.txt",
            mime="text/plain"
        )
    else:
        st.warning("Por favor, corrija os erros acima para gerar as credenciais.")

st.markdown("---")
st.caption("Parceiro de Programação - Gerador de Credenciais v1.0")