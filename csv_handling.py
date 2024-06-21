import pandas as pd
import sklearn.metrics.pairwise as pw

def avaliar(id_usuario, id_jogo, nota):
    df_teste = pd.read_csv('banco/usuario_jogos.csv')
    usuario = str(id_usuario)
    jogo = str(id_jogo)
    coluna_usu = 'usuario_id_fk'
    coluna_jo = 'jogos_id_fk'

    linhas_encontradas = df_teste[
        df_teste[coluna_usu].astype(str).str.contains(usuario, case=False) &
        df_teste[coluna_jo].astype(str).str.contains(jogo, case=False)
        ]

    # Exibe as linhas encontradas
    print(f'\n\n\n{linhas_encontradas}')

    if len(linhas_encontradas) == 1:
        # Pega o índice da linha encontrada
        indice = linhas_encontradas.index[0]

        df_teste.at[indice, 'avaliacao_usuario_jogos'] = str(nota)

        df_teste.to_csv('banco/usuario_jogos.csv', index=False)

def recomendar(user_top_avaliacao):
    print(user_top_avaliacao)
    avaliacoes = pd.read_csv("banco/usuario_jogos.csv", sep=",")
    jogos = pd.read_csv("banco/jogos.csv", sep=",")
    print(avaliacoes.head())
    print(jogos.head())

    df = jogos.merge(avaliacoes, left_on='id_jogos', right_on='jogos_id_fk')

    tabela_jogos = pd.pivot_table(df, index='nome_jogos', columns='usuario_id_fk', values='avaliacao_usuario_jogos').fillna(0)
    print(tabela_jogos.head())

    rec = pw.cosine_similarity(tabela_jogos)
    rec_df = pd.DataFrame(rec, columns=tabela_jogos.index, index=tabela_jogos.index)
    print(rec_df.head())

    cosine_df = pd.DataFrame(rec_df[str(user_top_avaliacao)].sort_values(ascending=False))
    cosine_df.columns = ['Recommendations']
    print(f'\n\n\n\n\n{cosine_df.head(2).index[0]}')
    caminho_arquivo = 'banco/cosine.csv'
    cosine_df.to_csv(caminho_arquivo, index=False)
    lista_recomedacoes = [cosine_df.head(6).index[1], cosine_df.head(6).index[2], cosine_df.head(6).index[3], cosine_df.head(6).index[4], cosine_df.head(6).index[5]]
    print(lista_recomedacoes)

    return lista_recomedacoes