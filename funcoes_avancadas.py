import numpy as np


# %%
def matrizes_internas(matriz_FR, nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int):
    """"
    super_matriz_FR é uma forma de organizar em matriz de matrizes
    para cada matriz externa é atribuido um valor de eq_paral_internos e eq_serie_internos
    """
    super_matriz_FR = np.ones((nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int))
    eq_paral_internos = np.ones((nr_lin_ext, nr_col_ext, nr_lin_int))
    eq_serie_internos = np.ones((nr_lin_ext, nr_col_ext))
    for i_ext in range(nr_lin_ext):
        for j_ext in range(nr_col_ext):
            rs = i_ext * nr_lin_int
            re = rs + nr_lin_int
            cs = j_ext * nr_col_int
            ce = cs + nr_col_int
            super_matriz_FR[i_ext, j_ext, :, :] = np.array(matriz_FR[rs:re, cs:ce])
            submatriz = super_matriz_FR[i_ext, j_ext, :, :]
            eq_paral_internos[i_ext, j_ext, :] = np.sum(submatriz, axis=1)

            # Lidando com divisão por zero ou por infinito
            with np.errstate(divide='ignore', invalid='ignore'):
                inverso = 1 / eq_paral_internos[i_ext, j_ext, :]
                soma_inversos = np.sum(inverso)

            # Verificando se o resultado da soma é infinito ou NaN
            if np.isinf(soma_inversos) or np.isnan(soma_inversos):
                eq_serie_internos[i_ext, j_ext] = 0
            else:
                eq_serie_internos[i_ext, j_ext] = 1 / soma_inversos

        eq_unidades = eq_serie_internos

    return super_matriz_FR, eq_paral_internos, eq_serie_internos, eq_unidades


# %%
def gerar_matrizes_internas_e_equivalentes_internos(matriz_fAr1, matriz_fBr1, matriz_fCr1,
                                                    matriz_fAr2, matriz_fBr2, matriz_fCr2,
                                                    nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int):
    """"

    """

    super_matriz_fAr1, eq_paral_internos_fAr1, eq_serie_internos_fAr1, eq_unidades_fAr1 = \
        matrizes_internas(matriz_fAr1, nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int)

    super_matriz_fAr2, eq_paral_internos_fAr2, eq_serie_internos_fAr2, eq_unidades_fAr2 = \
        matrizes_internas(matriz_fAr2, nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int)

    super_matriz_fBr1, eq_paral_internos_fBr1, eq_serie_internos_fBr1, eq_unidades_fBr1 = \
        matrizes_internas(matriz_fBr1, nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int)

    super_matriz_fBr2, eq_paral_internos_fBr2, eq_serie_internos_fBr2, eq_unidades_fBr2 = \
        matrizes_internas(matriz_fBr2, nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int)

    super_matriz_fCr1, eq_paral_internos_fCr1, eq_serie_internos_fCr1, eq_unidades_fCr1 = \
        matrizes_internas(matriz_fCr1, nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int)

    super_matriz_fCr2, eq_paral_internos_fCr2, eq_serie_internos_fCr2, eq_unidades_fCr2 = \
        matrizes_internas(matriz_fCr2, nr_lin_ext, nr_col_ext, nr_lin_int, nr_col_int)

    return [super_matriz_fAr1, eq_paral_internos_fAr1, eq_serie_internos_fAr1, eq_unidades_fAr1,
            super_matriz_fAr2, eq_paral_internos_fAr2, eq_serie_internos_fAr2, eq_unidades_fAr2,
            super_matriz_fBr1, eq_paral_internos_fBr1, eq_serie_internos_fBr1, eq_unidades_fBr1,
            super_matriz_fBr2, eq_paral_internos_fBr2, eq_serie_internos_fBr2, eq_unidades_fBr2,
            super_matriz_fCr1, eq_paral_internos_fCr1, eq_serie_internos_fCr1, eq_unidades_fCr1,
            super_matriz_fCr2, eq_paral_internos_fCr2, eq_serie_internos_fCr2, eq_unidades_fCr2]


# %%
def capacitancia_equivalente_externa_FR(eq_unidades_FR):
    eq_paral_externos = np.sum(eq_unidades_FR, axis=1)
    # Lidando com divisão por zero ou por infinito
    with np.errstate(divide='ignore', invalid='ignore'):
        inverso = 1 / eq_paral_externos
        soma_inversos = np.sum(inverso)

    # Verificando se o resultado da soma é infinito ou NaN
    if np.isinf(soma_inversos) or np.isnan(soma_inversos):
        eq_serie_externos = 0
    else:
        eq_serie_externos = 1 / soma_inversos

    eq_ramo = eq_serie_externos

    return eq_paral_externos, eq_serie_externos, eq_ramo

# %%
def capacitancias_equivalentes_nos_ramos(eq_unidades_fAr1, eq_unidades_fBr1, eq_unidades_fCr1,
                                         eq_unidades_fAr2, eq_unidades_fBr2, eq_unidades_fCr2):
    eq_paral_externos_fAr1, eq_serie_externos_fAr1, eq_ramo_fAr1 = capacitancia_equivalente_externa_FR(eq_unidades_fAr1)
    eq_paral_externos_fBr1, eq_serie_externos_fBr1, eq_ramo_fBr1 = capacitancia_equivalente_externa_FR(eq_unidades_fBr1)
    eq_paral_externos_fCr1, eq_serie_externos_fCr1, eq_ramo_fCr1 = capacitancia_equivalente_externa_FR(eq_unidades_fCr1)
    eq_paral_externos_fAr2, eq_serie_externos_fAr2, eq_ramo_fAr2 = capacitancia_equivalente_externa_FR(eq_unidades_fAr2)
    eq_paral_externos_fBr2, eq_serie_externos_fBr2, eq_ramo_fBr2 = capacitancia_equivalente_externa_FR(eq_unidades_fBr2)
    eq_paral_externos_fCr2, eq_serie_externos_fCr2, eq_ramo_fCr2 = capacitancia_equivalente_externa_FR(eq_unidades_fCr2)

    return [eq_paral_externos_fAr1, eq_serie_externos_fAr1, eq_ramo_fAr1,
            eq_paral_externos_fBr1, eq_serie_externos_fBr1, eq_ramo_fBr1,
            eq_paral_externos_fCr1, eq_serie_externos_fCr1, eq_ramo_fCr1,
            eq_paral_externos_fAr2, eq_serie_externos_fAr2, eq_ramo_fAr2,
            eq_paral_externos_fBr2, eq_serie_externos_fBr2, eq_ramo_fBr2,
            eq_paral_externos_fCr2, eq_serie_externos_fCr2, eq_ramo_fCr2]

# %%
