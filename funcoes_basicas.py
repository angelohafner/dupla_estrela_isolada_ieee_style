import streamlit as st
import os
from typing import List, Dict
import numpy as np
from engineering_notation import EngNumber

# %%
def text_to_int(num):
    """"
    É necessário tratar número como texto para suprimir a opção de apertar nos botões de incremento e decremento
    O fato de incrementar e decrementar via botões torna o programa lento e sujeito a erros.
    Assim é melhor o usuário digitar diretamente o número.
    """
    try:
        num = int(num)
        saida = num
    except ValueError:
        st.error("Por favor, insira um número válido")
        saida = "Por favor, insira um número válido"
    return saida

# %%
def text_to_decimal(num_text):
    """
    Esta função converte um texto em um número decimal.
    Ela aceita tanto ponto quanto vírgula como separadores decimais.
    Se a conversão não for possível, um erro é exibido.
    """
    # Substituir vírgula por ponto para padrão decimal
    num_text = num_text.replace(",", ".")

    try:
        num = float(num_text)
        saida = num
    except ValueError:
        st.error("Por favor, insira um número válido")
        saida = "Por favor, insira um número válido"
    return saida

# %%
def remove_file_if_exists(file_path):
    """"
    Remove arquivos, caso eles existam.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo removido: {file_path}")
    except OSError as e:
        print(f"Erro ao remover o arquivo {file_path}: {e}")

# %%
def text_to_decimal(num_text):
    """
    Esta função converte um texto em um número decimal.
    Ela aceita tanto ponto quanto vírgula como separadores decimais.
    Se a conversão não for possível, um erro é exibido.
    """
    # Substituir vírgula por ponto para padrão decimal
    num_text = num_text.replace(",", ".")

    try:
        num = float(num_text)
        saida = num
    except ValueError:
        st.error("Por favor, insira um número válido")
        saida = "Por favor, insira um número válido"
    return saida

# %%
def calculos_iniciais_banco(frequencia_fudamental_Hz: float,
                            tensao_nominal_fase_fase: float,
                            potencia_nominal_trifásica: float,
                            nr_lin_ext: int, nr_col_ext:int,
                            nr_lin_int: int, nr_col_int:int) -> List[Dict[str, float]]:

    omega = 2 * np.pi * frequencia_fudamental_Hz
    Vff = tensao_nominal_fase_fase * np.exp(1j * np.pi / 6)
    tensao_fase_neutro = tensao_nominal_fase_fase / np.sqrt(3)
    potencia_monofasica = (potencia_nominal_trifásica / 3)
    corrente_fase_neutro = potencia_monofasica / tensao_fase_neutro
    reatancia_fase_neutro = tensao_fase_neutro / corrente_fase_neutro
    capacitancia_fase_neutro = 1 / (omega * reatancia_fase_neutro)
    cap_externa = capacitancia_fase_neutro/(2*nr_col_ext) * nr_lin_ext
    # ⚠ cuidado que são dois ramos e três fases
    potencia_unidade_capacitiva = potencia_nominal_trifásica/(3*2*nr_lin_ext*nr_col_ext)
    tensao_unidade_capacitiva = tensao_fase_neutro / nr_lin_ext
    corrente_unidade_capacitiva = potencia_unidade_capacitiva / tensao_unidade_capacitiva
    reatancia_unidade_capacitiva = tensao_unidade_capacitiva / corrente_unidade_capacitiva
    capacitancia_unidade_capacitiva = 1 / ( reatancia_unidade_capacitiva * omega )
    capacitancia_elemento = (cap_externa / nr_col_int) * nr_lin_int
    reatancia_elemento = 1 / ( omega * capacitancia_elemento )
    corrente_elemento = corrente_unidade_capacitiva / nr_col_int
    tensao_elemento = tensao_unidade_capacitiva / nr_lin_int
    potencia_elemento = tensao_elemento * corrente_elemento



    dicionario_fase_neutro = {
        "Potência monofásica [VAr]": (potencia_monofasica),
        "Tensão fase-neutro [V]": (tensao_fase_neutro),
        "Corrente fase-neutro [A]": (corrente_fase_neutro),
        "Reatância fase-neutro [Ω]": (reatancia_fase_neutro),
        "Capacitância fase-neutro [F]": (capacitancia_fase_neutro)
    }

    dicionario_unidade = {
        "Potência unidade [VAr]": (potencia_unidade_capacitiva),
        "Tensão unidade [V]": (tensao_unidade_capacitiva),
        "Corrente unidade [A]": (corrente_unidade_capacitiva),
        "Reatância unidade [Ω]": (reatancia_unidade_capacitiva),
        "Capacitância unidade [F]": (capacitancia_unidade_capacitiva)
    }

    dicionario_elemento = {
        ("Potência elemento [VAr]"): [potencia_elemento],
        ("Tensão elemento [V]"): [tensao_elemento],
        ("Corrente elemento [A]"): [corrente_elemento],
        ("Reatância elemento [Ω]"): [reatancia_elemento],
        ("Capacitância elemento [F]"): [capacitancia_elemento]
    }

    dicionario_fase_neutro_formatado = {
        "Potência monofásica [VAr]": EngNumber(potencia_monofasica),
        "Tensão fase-neutro [V]": EngNumber(tensao_fase_neutro),
        "Corrente fase-neutro [A]": EngNumber(corrente_fase_neutro),
        "Reatância fase-neutro [Ω]": EngNumber(reatancia_fase_neutro),
        "Capacitância fase-neutro [F]": EngNumber(capacitancia_fase_neutro)
    }

    dicionario_unidade_formatado = {
        "Potência unidade [VAr]": EngNumber(potencia_unidade_capacitiva),
        "Tensão unidade [V]": EngNumber(tensao_unidade_capacitiva),
        "Corrente unidade [A]": EngNumber(corrente_unidade_capacitiva),
        "Reatância unidade [Ω]": EngNumber(reatancia_unidade_capacitiva),
        "Capacitância unidade [F]": EngNumber(capacitancia_unidade_capacitiva)
    }

    dicionario_elemento_formatado = {
        "Potência elemento [VAr]": EngNumber(potencia_elemento),
        "Tensão elemento [V]": EngNumber(tensao_elemento),
        "Corrente elemento [A]": EngNumber(corrente_elemento),
        "Reatância elemento [Ω]": EngNumber(reatancia_elemento),
        "Capacitância elemento [F]": EngNumber(capacitancia_elemento)
    }

    return [dicionario_fase_neutro, dicionario_unidade, dicionario_elemento,
            dicionario_fase_neutro_formatado, dicionario_unidade_formatado, dicionario_elemento_formatado]