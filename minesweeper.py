# Daniel Pereira 199194
# TODO gerador pode ser objeto?
# TODO gerador n_bits pode ser o que quiser?


# TAD gerador ******************************************************************
def cria_gerador(n_bits, seed):
    '''
    Construtor

    Recebe n_bits (nº de bits do gerador) e uma seed (estado inicial)
    e devolve o gerador correspondente

    cria_gerador: int * int -> gerador
    '''
    if not (eh_args_gerador(n_bits, seed)):
        raise ValueError('cria gerador: argumentos invalidos')

    return [n_bits, seed]


def cria_copia_gerador(gerador):
    '''
    Construtor

    recebe um gerador e devolve uma copia nova do mesmo

    cria_copia_gerador: gerador -> gerador
    '''
    return gerador.copy()


def obtem_estado(gerador):
    '''
    Seletor

    devolve o estado atual do gerador sem o alterar

    obtem_estado: gerador -> int
    '''
    return gerador[1]


def define_estado(gerador, i):
    '''
    Modificador

    define novo valor i para a seed do gerador

    define_estado: gerador * int -> int
    '''
    gerador[1] = i
    return i


def atualiza_estado(gerador):
    '''
    Modificador

    atualiza a seed do gerador de acordo com o algoritmo xorshift (geracao de nºs
    pseudoaleatorios) e devolve-o

    atualiza_estado: gerador -> int
    '''
    if gerador[0] == 32:
        valor_hexa = 0xFFFFFFFF
        valores_deslocamento = (13, 17, 5)
    else:
        valor_hexa = 0xFFFFFFFFFFFFFFFF
        valores_deslocamento = (13, 7, 17)
    s = gerador[1]

    s ^= (s << valores_deslocamento[0]) & valor_hexa
    s ^= (s >> valores_deslocamento[1]) & valor_hexa
    s ^= (s << valores_deslocamento[2]) & valor_hexa


    return define_estado(gerador, s)


def eh_args_gerador(n1, n2):
    '''
    Reconhecedor

    Retorna True se n1 for um numero de bits (inteiro 32 ou 64) e n2 for uma seed
    (inteiro positivo)

    eh_args_gerador: universal * universal -> booleano
    '''
    return type(n1) == int and type(n2) == int and n1 in (32, 64) and n2 > 0



def eh_gerador(arg):
    '''
    Reconhecedor

    Retorna True se arg for um TAD gerador, False caso contrario

    eh_gerador : universal -> booleano
    '''

    return isinstance(arg, list) and len(arg) == 2 and \
            eh_args_gerador(arg[0], arg[1])


def geradores_iguais(g1, g2):
    '''
    Teste

    Compara 2 geradores e devolve True se forem iguais

    geradores_iguais: gerador * gerador -> booleano
    '''
    # TODO isto é abstrato?
    return eh_gerador(g1) and eh_gerador(g2) and g1 == g2


def gerador_para_str(gerador):
    '''
    Transformador

    transforma o gerador numa string do tipo 'xorshift32(s=1)' se numero de bits
    for 32 e seed 1

    gerador_para_str : gerador -> str
    '''
    return f'xorshift{gerador[0]}(s={gerador[1]})'


def gera_numero_aleatorio(gerador, n):
    '''
    Funcao de alto nivel

    Atualiza a seed do gerador e devolve um numero aleatorio entre 1 e n, obtido
    a partir do novo estado s do gerador como 1 + mod(s, n)

    gera_numero_aleatorio: gerador * int -> int
    '''
    #TODO verificar n>0??
    atualiza_estado(gerador)
    seed = obtem_estado(gerador)
    return 1 + (seed % n)


def gera_carater_aleatorio(gerador, c):
    '''
    Funcao de alto nivel

    Atualiza o seed do gerador e devolve um caracter aleatorio entre 'A' e o
    caracter maiusculo c, obtido a partir da nova seed como o caracter na posicao
    mod(s, l) da cadeia de caracteres de tamanho l entre 'A' e c

    gera_carater_aleatorio: gerador * str -> int
    '''
    atualiza_estado(gerador)
    seed = obtem_estado(gerador)
    print(seed)
    l = ord(c.upper()) - ord('A') + 1
    return chr(seed % l + 65) #carater A (ord = 65)



# TAD coordenada ***************************************************************
def cria_coordenada(col, lin):
    '''
    Construtor

    Recebe os valores correspondentes À coluna col e linha lin e devolve a coord
    correspondente

    cria_coordenada: str * int -> coordenada
    '''
    if not eh_args_coordenada(col, lin):
        raise ValueError('cria_coordenada: argumentos invalidos')

    return [col, lin]


def obtem_coluna(c):
    '''
    Seletor

    Devolve a coluna da coordenada c

    obtem_coluna: coordenada -> str
    '''
    return c[0]


def obtem_linha(c):
    '''
    Seletor

    Devolve a linha de coordenada c

    obtem_linha: coordenada -> int
    '''
    return c[1]


def eh_coordenada(arg):
    '''
    Reconhecedor

    Devolve True se arg for uma TAD coordenada

    eh_coordenada: universal -> booleano
    '''
    return isinstance(arg, list) and len(arg) == 2 and \
            eh_args_coordenada(arg[0], arg[1])


def eh_args_coordenada(c, l):
    '''
    Reconhecedor

    Devolve True se coluna c e um caracter maiusculo entre A e Z e linha l um numero
    inteiro entre 1 e 99

    eh_args_coordenada: universal * universal -> boolean
    '''
    return isinstance(c, str) and len(c) == 1 and c.isupper() \
            and type(l) == int and 1 <= l <= 99


def coordenadas_iguais(c1, c2):
    '''
    Teste

    Devolve True apenas se c1 e c2 forem coordenadas e iguais

    coordenadas_iguais: coordenada * coordenada -> booleano
    '''
    #TODO perguntar abstracao
    return eh_coordenada(c1) and eh_coordenada(c2) and \
        obtem_linha(c1) == obtem_linha(c2) and obtem_coluna(c1) == obtem_coluna(c2)


def coordenada_para_str(c):
    '''
    Transformador

    Transforma a coordenada numa string do tipo B01 caso coluna for B e linha 1

    coordenada_para_str : coordenada -> str
    '''
    return f'{obtem_coluna(c)}{obtem_linha(c):0>2d}' # para o numero da linha
                                                    # ter sempre dimensao de 2,
                                                    # adiciona-se zeros a esquerda

def str_para_coordenada(s):
    '''
    Transformador

    A partir da sua representacao em string, devolve a coordenada representada

    str_para_coordenada: str -> coordenada
    '''
    # TODO abstracao, criar?
    return [s[0], s[1:]]


def coluna_para_int(col):
    '''
    Transformador

    Recebe uma coluna bem formatada (entre A e Z maiuscula) e devolve o seu valor
    inteiro entre A e col

    coluna_para_int: str -> int
    '''
    return ord(col) - ord('A') + 1


def obtem_coordenadas_vizinhas(c):
    '''
    Funcao de alto nivel

    Retorna num tuplo todas as coordenadas vizinhas de c, comecando do topo a
    esquerda e seguindo no sentido horario

    obtem_coordenadas_vizinhas: coordenada -> tuplo
    '''
    #TODO perguntar abstracao vizinha
    coord_vizinhas = ()
    col = obtem_coluna(c)
    lin = obtem_linha(c)
    # considerando c com coluna 0 e linha 0, percorer os vizinhos pelo sentido
    # horario tem este aspeto de tuplo de tuplos
    for c_l in ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)):
        col_viz = chr(ord(col) + c_l[0])
        lin_viz = lin + c_l[1]
        if eh_args_coordenada(col_viz, lin_viz):
            coord_vizinhas += (cria_coordenada(col_viz, lin_viz),)
    return coord_vizinhas


def obtem_coordenada_aleatoria(c, gerador):
    '''
    Funcao alto nivel

    Recebe uma coordenada c e uma TAD gerador e devolve uma coordenada
    gerada aleatoriamente em que c define a maior coluna e linha possiveis

    obtem_coordenada_aleatoria: coordenada * gerador -> coordenada
    '''
    max_coluna = obtem_coluna(c)
    max_linha = obtem_linha(c)

    col_aleatorio = gera_carater_aleatorio(gerador, max_coluna)
    lin_aleatorio = gera_numero_aleatorio(gerador, max_linha)

    return cria_coordenada(col_aleatorio, lin_aleatorio)



# TAD parcela ******************************************************************
def cria_parcela():
    '''
    Construtor

    Devolve uma parcela tapada sem mina escondida
    As parcelas sao do tipo [estado, mina], em que estado pode ser tapada, limpa
    ou marcada, mina se tem ou nao

    cria_pacela: {} -> parcela
    '''
    return ['tapada', 'sem mina']


def cria_copia_parcela(p):
    '''
    Construtor

    Devolve uma copia da parcela p

    cria_copia_parcela: parcela -> parcela
    '''
    return p.copy()

# TODO modificadores nao estao a alterar destrutivamente p
def limpa_parcela(p):
    '''
    Modificador

    Modifica destrutivamente a parcela p para estado limpa e devolve a propria parcela

    limpa_parcela: parcela -> parcela
    '''
    p[0] = 'limpa'
    return p


def marca_parcela(p):
    '''
    Modificador

    Modifica destrutivamente o estado da parcela para marcada com bandeira e
    devolve a propria parcela

    marca_parcela: parcela -> parcela
    '''
    p[0] = 'marcada'
    return p


def desmarca_parcela(p):
    '''
    Modificador

    Modifica destrutivamente a parcela p modificando o seu estado para tapada e
    devolve a propria parcela

    desmarca_parcela: parcela -> parcela
    '''
    p[0] = 'tapada'
    return p


def esconde_mina(p):
    '''
    Modificador

    Modifica destrutivamente a parcela p escondendo uma mina nela, e devolve a
    propria parcela.

    esconde_mina: parcela -> parcela
    '''
    p[1] = 'com mina'
    return p

def eh_parcela(arg):
    '''
    Reconhecedor

    Devolve True caso o seu argumento seja um TAD parcela e False caso contrario

    eh_parcela: universal -> booleano
    '''
    return (isinstance(arg, list) and len(arg) == 2 and
            arg[0] in ('tapada', 'limpa', 'marcada') and
            arg[1] in ('com mina', 'sem mina'))


def eh_parcela_tapada(p):
    '''
    Reconhecedor

    Devolve True caso a parcela p se encontre tapada e False caso contrario

    eh_parcela_tapada: parcela -> booleano
    '''
    return p[0] == 'tapada'


def eh_parcela_marcada(p):
    '''
    Reconhecedor

    Devolve True caso a parcela p se encontre marcada com uma bandeira e False
    caso contrario

    eh_parcela_marcada: parcela -> booleano
    '''
    return p[0] == 'marcada'


def eh_parcela_limpa(p):
    '''
    Reconhecedor

    Devolve True caso a parcela p se encontre limpa e False caso contrario

    eh_parcela_limpa: parcela -> booleano
    '''
    return p[0] == 'limpa'


def eh_parcela_minada(p):
    '''
    Reconhecedor

    Devolve True caso a parcela p esconda uma mina e False caso contrario

    eh_parcela_minada: parcela -> booleano
    '''
    return p[1] == 'com mina'


def parcelas_iguais(p1, p2):
    '''
    Teste

    Devolve True apenas se p1 e p2 sao parcelas e sao iguais

    parcelas_iguais: parcela * parcela -> booleano
    '''
    return eh_parcela(p1) and eh_parcela(p2) and p1 == p2


def parcela_para_str(p):
    '''
    Transformador

    Devolve a cadeia de caracteres que representa a parcela em funcao do seu
    estado: parcelas tapadas ('#'), parcelas marcadas ('@'),
    parcelas limpas sem mina ('?') e parcelas limpas com mina ('X')

    parcela_para_str : parcela -> str
    '''
    if eh_parcela_tapada(p):
        return '#'
    elif eh_parcela_marcada(p):
        return '@'
    elif eh_parcela_limpa(p):
        if not eh_parcela_minada(p):
            return '?'
        elif eh_parcela_minada(p):
            return 'X'


def alterna_bandeira(p):
    '''
    Funcao de alto nivel

    recebe uma parcela p e modifica-a destrutivamente da seguinte forma: desmarca
    se estiver marcada e marca se estiver tapada, devolvendo True.
    Em qualquer outro caso, nao modifica a parcela e devolve False

    alterna_bandeira: parcela -> booleano
    '''
    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    elif eh_parcela_tapada(p):
        marca_parcela(p)
        return True
    else:
        return False



# TAD campo ********************************************************************
def cria_campo(col, lin):
    '''
    Construtor

    Recebe uma cadeia de carateres e um inteiro correspondentes a ultima coluna
    e a ultima linha de um campo de minas, e devolve o campo do tamanho
    pretendido formado por parcelas tapadas sem minas

    cria_campo: str * int -> campo
    '''
    if not eh_args_coordenada(col, lin):
        raise ValueError('cria_campo: argumentos invalidos')

    # cria uma lista de tamanho nº linhas e sublistas de tamanho nº colunas
    return [[cria_parcela() for _ in range(coluna_para_int(col))]
            for _ in range(lin)]


def cria_copia_campo(campo):
    '''
    Construtor

    Recebe um campo e devolve uma nova copia do campo

    cria_copia_campo: campo -> campo
    '''
    return [copia_campo[:] for copia_campo in campo]


def obtem_ultima_coluna(campo):
    pass




def main():
    c = cria_campo('A', 2)
    c2 = cria_copia_campo(c)
    print(id(c2))


if __name__ == '__main__':
    main()