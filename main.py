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
    nfiq = st.selectbox("Fusíveis internos queimados no grupo", options=np.arange(0, 6, 1), index=0)

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
st.markdown("### Banco sadio")
st.markdown(align_right_css + html_fase_neutro, unsafe_allow_html=True)

st.markdown("### Unidades capacitivas sadias")
st.markdown(align_right_css + html_unidade, unsafe_allow_html=True)

st.markdown("### Elementos sadios")
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

st.markdown("### Tensões na unidade afetada [kV]")
df = pd.DataFrame((np.abs(tensoes_internos_fAr1[0, 0, :, :])/1e3))
st.table(df)

st.markdown("### Corrente entre as duas estrelas [A]")
st.markdown(f"{np.abs(deslocamento_neutro[4])[0]}")