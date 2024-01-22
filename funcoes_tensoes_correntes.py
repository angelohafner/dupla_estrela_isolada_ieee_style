import numpy as np
import streamlit as st



def calcular_correntes_tensoes(resultados_capacitancia_nos_ramos,
                               resultados_matrizes_internas,
                               frequencia_fundamental_Hz, tensao_nominal_fase_fase, a, nr_lin_ext, nr_col_ext):

    eq_paral_externos_fAr1, eq_serie_externos_fAr1, eq_ramo_fAr1, \
        eq_paral_externos_fBr1, eq_serie_externos_fBr1, eq_ramo_fBr1, \
        eq_paral_externos_fCr1, eq_serie_externos_fCr1, eq_ramo_fCr1, \
        eq_paral_externos_fAr2, eq_serie_externos_fAr2, eq_ramo_fAr2, \
        eq_paral_externos_fBr2, eq_serie_externos_fBr2, eq_ramo_fBr2, \
        eq_paral_externos_fCr2, eq_serie_externos_fCr2, eq_ramo_fCr2 = resultados_capacitancia_nos_ramos

    super_matriz_fAr1, eq_paral_internos_fAr1, eq_serie_internos_fAr1, eq_unidades_fAr1, \
        super_matriz_fAr2, eq_paral_internos_fAr2, eq_serie_internos_fAr2, eq_unidades_fAr2, \
        super_matriz_fBr1, eq_paral_internos_fBr1, eq_serie_internos_fBr1, eq_unidades_fBr1, \
        super_matriz_fBr2, eq_paral_internos_fBr2, eq_serie_internos_fBr2, eq_unidades_fBr2, \
        super_matriz_fCr1, eq_paral_internos_fCr1, eq_serie_internos_fCr1, eq_unidades_fCr1, \
        super_matriz_fCr2, eq_paral_internos_fCr2, eq_serie_internos_fCr2, eq_unidades_fCr2 = resultados_matrizes_internas

    omega = 2 * np.pi * frequencia_fundamental_Hz

    Ca = eq_ramo_fAr1 + eq_ramo_fAr2
    Cb = eq_ramo_fBr1 + eq_ramo_fBr2
    Cc = eq_ramo_fBr1 + eq_ramo_fCr2

    Ya = 1j * omega * Ca
    Yb = 1j * omega * Cb
    Yc = 1j * omega * Cc

    Za = 1 / Ya
    Zb = 1 / Yb
    Zc = 1 / Yc

    Z_abc = np.array([[Za, 0, 0],
                      [0, Zb, 0],
                      [0, 0, Zc]])
    V_linha = tensao_nominal_fase_fase
    Z_malha = np.array([[Za + Zb, -Zb],
                        [-Zb, Zb + Zc]])
    V_malha = np.array([[V_linha], [V_linha * (a ** 2)]])
    I_alphabeta = np.linalg.inv(Z_malha) @ V_malha
    I_alpha = I_alphabeta[0, 0]
    I_beta = I_alphabeta[1, 0]
    I_abc = np.array([[I_alpha], [I_beta - I_alpha], [-I_beta]])
    Vabco = Z_abc @ I_abc
    Von = np.sum(Vabco) / 3

    # Corrente de cada ramo paralelo
    I_fAr1 = Vabco[0] * 1j * omega * eq_ramo_fAr1
    I_fBr1 = Vabco[1] * 1j * omega * eq_ramo_fBr1
    I_fCr1 = Vabco[2] * 1j * omega * eq_ramo_fCr1
    I_fAr2 = Vabco[0] * 1j * omega * eq_ramo_fAr2
    I_fBr2 = Vabco[1] * 1j * omega * eq_ramo_fBr2
    I_fCr2 = Vabco[2] * 1j * omega * eq_ramo_fCr2

    I_n1 = I_fAr1 + I_fBr1 + I_fCr1
    I_n2 = I_fAr2 + I_fBr2 + I_fCr2

    # Tensão de cada capacitor externo de cada ramo
    tensao_unidades_fAr1, corrente_unidades_fAr1 = \
        tensoes_e_correntes_capacitores_externos_cada_ramo(I_fAr1, eq_paral_externos_fAr1, eq_unidades_fAr1, omega)
    tensao_unidades_fBr1, corrente_unidades_fBr1 = \
        tensoes_e_correntes_capacitores_externos_cada_ramo(I_fBr1, eq_paral_externos_fBr1, eq_unidades_fBr1, omega)
    tensao_unidades_fCr1, corrente_unidades_fCr1 = \
        tensoes_e_correntes_capacitores_externos_cada_ramo(I_fCr1, eq_paral_externos_fCr1, eq_unidades_fCr1, omega)
    tensao_unidades_fAr2, corrente_unidades_fAr2 = \
        tensoes_e_correntes_capacitores_externos_cada_ramo(I_fAr2, eq_paral_externos_fAr2, eq_unidades_fAr2, omega)
    tensao_unidades_fBr2, corrente_unidades_fBr2 = \
        tensoes_e_correntes_capacitores_externos_cada_ramo(I_fBr2, eq_paral_externos_fBr2, eq_unidades_fBr2, omega)
    tensao_unidades_fCr2, corrente_unidades_fCr2 = \
        tensoes_e_correntes_capacitores_externos_cada_ramo(I_fCr2, eq_paral_externos_fCr2, eq_unidades_fCr2, omega)

    tensoes_unidades = [tensao_unidades_fAr1, tensao_unidades_fBr1, tensao_unidades_fCr1,
                        tensao_unidades_fAr2, tensao_unidades_fBr2, tensao_unidades_fCr2]

    corrente_unidades = [corrente_unidades_fAr1, corrente_unidades_fBr1, corrente_unidades_fCr1,
                         corrente_unidades_fAr2, corrente_unidades_fBr2, corrente_unidades_fCr2]

    deslocamento_neutro = [I_abc, Vabco, Von, I_n1, I_n2]

    # =============================================================

    tensoes_internos_fAr1, correntes_internos_fAr1 = \
        tensoes_correntes_internos(corrente_unidades_fAr1, super_matriz_fAr1, eq_paral_internos_fAr1,
                                   nr_lin_ext, nr_col_ext, omega)


    return [deslocamento_neutro, tensoes_unidades, corrente_unidades, tensoes_internos_fAr1, correntes_internos_fAr1]

def tensoes_e_correntes_capacitores_externos_cada_ramo(I_FR, eq_paral_externos_FR, original_externos_FR, omega):
    """
    super_matriz_fAr1.shape ==> ex. (2, 3, 5, 9)
    eq_paral_internos_fAr1.shape ==> ex. (2, 3, 5)
    eq_serie_internos_fAr2.shape ==> ex. (2, 3)
    eq_paral_externos_fAr1.shape ==> (2)
    eq_serie_externos_fAr1.shape ==> ()
    """

    Y_original_FR = 1j * omega * original_externos_FR
    Y_ser_ext_FR = 1j * omega * eq_paral_externos_FR
    V_ser_ext_FR = I_FR / Y_ser_ext_FR
    I_par_ext_FR = V_ser_ext_FR[:, np.newaxis] * Y_original_FR
    corrente_unidades_FR = I_par_ext_FR
    tensao_unidades_FR = I_par_ext_FR / Y_original_FR

    return [tensao_unidades_FR, corrente_unidades_FR]

def tensoes_correntes_internos(corrente_unidades_fAr1, super_matriz_fAr1, eq_paral_internos_fAr1, nr_lin_ext, nr_col_ext, omega):
    """"
    Grandezas elétricas de todos os elementos internos de cada ramo
    """
    forma_matriz = np.shape(super_matriz_fAr1)
    tensoes_internos = np.ones(shape=forma_matriz, dtype=complex)
    correntes_internos = np.ones(shape=forma_matriz, dtype=complex)
    for i_ext in range(nr_lin_ext):
        for j_ext in range(nr_col_ext):
            Y_interna = 1j * omega * super_matriz_fAr1[i_ext, j_ext]
            Y_paral_internos = 1j * omega * eq_paral_internos_fAr1[i_ext, j_ext]
            V_paral_internos = corrente_unidades_fAr1[i_ext, j_ext] / Y_paral_internos
            I_internos = V_paral_internos[:, np.newaxis] * Y_interna
            V_paral_internos = I_internos / Y_interna
            tensoes_internos[i_ext, j_ext, :, :] = V_paral_internos
            correntes_internos[i_ext, j_ext, :, :] = I_internos

    return [tensoes_internos, correntes_internos]