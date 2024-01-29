import streamlit as st
import numpy as np
import pandas as pd
from funcoes_basicas import *
from funcoes_avancadas import *
from funcoes_tensoes_correntes import *

a = np.exp(1j * 2 * np.pi / 3)

st.markdown("# Ungrounded Double Star Bank")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Sistema")
    frequencia_fundamental_Hz = st.selectbox("Frequência Fundamental [Hz]", options=[60, 50])
    tensao_nominal_fase_fase = st.text_input("Tensao de Linha [kV]", value="34,500")
    tensao_nominal_fase_fase = 1e3 * text_to_decimal(tensao_nominal_fase_fase)

with col2:
    st.markdown("### Banco")
    nr_lin_ext = st.selectbox("Quantidade Série", options=np.arange(1, 11, 1), index=1)
    nr_col_ext = st.selectbox("Quantidade Paralelo", options=np.arange(1, 11, 1), index=2)
    potencia_nominal_trifasica = st.text_input("Potência Reativa Trifásica [kVAr]", value="25020")
    potencia_nominal_trifasica = 1e3 * text_to_decimal(potencia_nominal_trifasica)

with col3:
    st.markdown("### Unidade")
    nr_lin_int = st.selectbox("Quantidade Série", options=np.arange(1, 11, 1), index=4)
    nr_col_int = st.selectbox("Quantidade Paralelo", options=np.arange(1, 11, 1), index=8)
    # nfiq = st.selectbox("Fusíveis internos queimados no grupo", options=np.arange(0, 6, 1), index=0)

resultados = calculos_iniciais_banco(frequencia_fundamental_Hz,
                                     tensao_nominal_fase_fase,
                                     potencia_nominal_trifasica,
                                     nr_lin_ext, nr_col_ext,
                                     nr_lin_int, nr_col_int)

dicionario_fase_neutro, dicionario_unidade, dicionario_elemento, \
    dicionario_fase_neutro_formatado, dicionario_unidade_formatado, dicionario_elemento_formatado = resultados

df_fase_neutro_formatado = pd.DataFrame([dicionario_fase_neutro_formatado])
df_unidade_formatado = pd.DataFrame([dicionario_unidade_formatado])
df_elemento_formatado = pd.DataFrame([dicionario_elemento_formatado])

# Convertendo os DataFrames para HTML sem índices de linha
html_fase_neutro = df_fase_neutro_formatado.to_html(index=False)
html_unidade = df_unidade_formatado.to_html(index=False)
html_elemento = df_elemento_formatado.to_html(index=False)

# CSS para alinhar o texto à direita em todas as células da tabela
align_right_css = """
<style>
table, th, td {
  text-align: right;
}
</style>
"""

# Exibindo as tabelas HTML no Streamlit com CSS personalizado
st.markdown("### Dados nominais de uma fase do banco")
st.markdown(align_right_css + html_fase_neutro, unsafe_allow_html=True)

st.markdown("### Dados nominais de uma unidade capacitiva")
st.markdown(align_right_css + html_unidade, unsafe_allow_html=True)

st.markdown("### Dados nominais de um elemento interno")
st.markdown(align_right_css + html_elemento, unsafe_allow_html=True)

# %%
capacitancia_elemento = dicionario_elemento["Capacitância elemento [F]"]
matriz = capacitancia_elemento * np.ones((3, nr_lin_ext * nr_lin_int, 2 * nr_col_ext * nr_col_int), dtype=float)

matriz_fAr1 = matriz[0, :, 0:nr_col_ext * nr_col_int]
matriz_fAr2 = matriz[0, :, nr_col_ext * nr_col_int: 2 * nr_col_ext * nr_col_int]
matriz_fBr1 = matriz[1, :, 0:nr_col_ext * nr_col_int]
matriz_fBr2 = matriz[1, :, nr_col_ext * nr_col_int: 2 * nr_col_ext * nr_col_int]
matriz_fCr1 = matriz[2, :, 0:nr_col_ext * nr_col_int]
matriz_fCr2 = matriz[2, :, nr_col_ext * nr_col_int: 2 * nr_col_ext * nr_col_int]

# Adicioanr os capacitores internos queimados
# nfiq = número de fusíveis internos queimados em um mesmo grupo
corrente_entre_estrelas = []
tensao_de_deslocamento_de_neutro = []
tensao_no_grupo_afetado = []
capacitancia_da_fase_afetada = []
capacitancia_da_unidade_afetada = []
nfiq_possibilidades = np.arange(0, nr_col_int, 1)
for nfiq in nfiq_possibilidades:
    if nfiq != 0:
        matriz_fAr1[0, np.arange(nfiq)] = 1e-99

    resultados_matrizes_internas = \
        gerar_matrizes_internas_e_equivalentes_internos(matriz_fAr1, matriz_fBr1, matriz_fCr1,
                                                        matriz_fAr2, matriz_fBr2, matriz_fCr2,
                                                        nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int)

    # Matrizes são separadas como matrizes de matrizes
    # Também são calculados os equivalentes paraelos e os equivalentes séries das matrizes internas.
    # Estes equivalentes são indexados de acordo com o índice da unidade capacitiva correspondente.
    super_matriz_fAr1, eq_paral_internos_fAr1, eq_serie_internos_fAr1, eq_unidades_fAr1, \
        super_matriz_fAr2, eq_paral_internos_fAr2, eq_serie_internos_fAr2, eq_unidades_fAr2, \
        super_matriz_fBr1, eq_paral_internos_fBr1, eq_serie_internos_fBr1, eq_unidades_fBr1, \
        super_matriz_fBr2, eq_paral_internos_fBr2, eq_serie_internos_fBr2, eq_unidades_fBr2, \
        super_matriz_fCr1, eq_paral_internos_fCr1, eq_serie_internos_fCr1, eq_unidades_fCr1, \
        super_matriz_fCr2, eq_paral_internos_fCr2, eq_serie_internos_fCr2, eq_unidades_fCr2 = resultados_matrizes_internas

    resultados_capacitancia_nos_ramos = \
        capacitancias_equivalentes_nos_ramos(eq_unidades_fAr1, eq_unidades_fBr1, eq_unidades_fCr1,
                                             eq_unidades_fAr2, eq_unidades_fBr2, eq_unidades_fCr2)

    eq_paral_externos_fAr1, eq_serie_externos_fAr1, eq_ramo_fAr1, \
        eq_paral_externos_fBr1, eq_serie_externos_fBr1, eq_ramo_fBr1, \
        eq_paral_externos_fCr1, eq_serie_externos_fCr1, eq_ramo_fCr1, \
        eq_paral_externos_fAr2, eq_serie_externos_fAr2, eq_ramo_fAr2, \
        eq_paral_externos_fBr2, eq_serie_externos_fBr2, eq_ramo_fBr2, \
        eq_paral_externos_fCr2, eq_serie_externos_fCr2, eq_ramo_fCr2 = resultados_capacitancia_nos_ramos

    deslocamento_neutro, tensoes_unidades, corrente_unidades, tensoes_internos_fAr1, correntes_internos_fAr1 = \
        calcular_correntes_tensoes(resultados_capacitancia_nos_ramos,
                                   resultados_matrizes_internas,
                                   frequencia_fundamental_Hz,
                                   tensao_nominal_fase_fase,
                                   a, nr_lin_ext, nr_col_ext)


    corrente_entre_estrelas.append(np.abs(deslocamento_neutro[4])[0])
    tensao_de_deslocamento_de_neutro.append(np.abs(deslocamento_neutro[2]))
    tensao_no_grupo_afetado.append(np.abs(tensoes_internos_fAr1[0, 0, 0, 0]))
    capacitancia_da_fase_afetada.append(1e6*eq_ramo_fAr1)
    capacitancia_da_unidade_afetada.append(1e6*eq_unidades_fAr1[0,0])

st.markdown("### Variação das grandezas elétricas em função do número de fusíveis internos queimados (ajuste de alarme e trip)")
nfiq_possibilidades_formatado = [str(x) for x in nfiq_possibilidades]
corrente_entre_estrelas_formatado = [f"{x:.3}" for x in corrente_entre_estrelas]
tensao_de_deslocamento_de_neutro_formatado = [f"{x:.1f}" for x in tensao_de_deslocamento_de_neutro]
tensao_no_grupo_afetado_formatado = [f"{x:.1f}" for x in tensao_no_grupo_afetado]
tensao_no_grupo_afetado_pu = [f"{x:.3f}" for x in tensao_no_grupo_afetado/tensao_no_grupo_afetado[0]]
capacitancia_da_fase_afetada_formatado = [f"{x:.1f}" for x in capacitancia_da_fase_afetada]
capacitancia_da_fase_afetada_pu = [f"{x:.3f}" for x in capacitancia_da_fase_afetada/capacitancia_da_fase_afetada[0]]
capacitancia_da_unidade_afetada_formatado = [f"{x:.1f}" for x in capacitancia_da_unidade_afetada]
capacitancia_da_unidade_afetada_pu = [f"{x:.3f}" for x in capacitancia_da_unidade_afetada/capacitancia_da_unidade_afetada[0]]


my_array = [nfiq_possibilidades_formatado,
            corrente_entre_estrelas_formatado,
            tensao_de_deslocamento_de_neutro_formatado,
            tensao_no_grupo_afetado_formatado,
            tensao_no_grupo_afetado_pu,
            capacitancia_da_fase_afetada_formatado,
            capacitancia_da_fase_afetada_pu,
            capacitancia_da_unidade_afetada_formatado,
            capacitancia_da_unidade_afetada_pu]

columns = pd.MultiIndex.from_tuples([
    ('Número de elementos perdidos', 'f'),
    ('Corrente entre as estrelas', '[A]'),
    ('Tensão neutro-terra', '[V]'),
    ('Tensão no grupo afetado', '[V]'),
    ('Tensão no grupo afetado', '[pu]'),
    ('Capacitância da fase afetada', '[μF]'),
    ('Capacitância da fase afetada', '[pu]'),
    ('Capacitância da unidade afetada', '[μF]'),
    ('Capacitância da unidade afetada', '[pu]')
])

# Criando o DataFrame e transpondo
df_tabela_resumo_ieee = pd.DataFrame(my_array, columns).T

# Convertendo o DataFrame em HTML sem mostrar o índice
html = df_tabela_resumo_ieee.to_html(index=False)

# Exibindo o HTML no Streamlit
st.markdown(html, unsafe_allow_html=True)

