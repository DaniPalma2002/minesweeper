# Daniel Pereira 199194
# TODO gerador pode ser objeto?
# TODO gerador n_bits pode ser o que quiser?


# TAD gerador ******************************************************************
from inspect import stack
from textwrap import indent


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

def eh_str_coordenada(arg):
    '''
    Reconhecedor

    Devolve True se arg for do tipo str_coordenada (ex:A01, Z99)

    eh_str_coordenada: universal -> boleano
    '''
    return (isinstance(arg, str) and len(arg) == 3 and
        eh_coordenada(str_para_coordenada(arg)))


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
    return [s[0], int(s[1:])]


def coluna_para_int(col):
    '''
    Transformador

    Recebe uma coluna bem formatada (entre A e Z maiuscula) e devolve o seu valor
    inteiro entre A e col (0 a 25)

    coluna_para_int: str -> int
    '''
    return ord(col) - ord('A')


def int_para_coluna(i):
    '''
    Transformador

    Recebe um inteiro entre 0 e 25 e retorna o caracter maiusculo entre A e Z

    int_para_coluna: int -> str
    '''
    return chr(i + ord('A'))


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
        if eh_args_coordenada(col_viz, lin_viz) and col_viz:
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


# TODO modificadores nao estao a alterar destrutivamente p?
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
    p[1] = 'minada'
    return p

def eh_parcela(arg):
    '''
    Reconhecedor

    Devolve True caso o seu argumento seja um TAD parcela e False caso contrario

    eh_parcela: universal -> booleano
    '''
    return (isinstance(arg, list) and len(arg) == 2 and
            arg[0] in ('tapada', 'limpa', 'marcada') and
            arg[1] in ('minada', 'sem mina'))


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
    return p[1] == 'minada'


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

    Devolve a cadeia de caracteres que representa a parcela em funcao do seu estado:
    - parcelas tapadas ('#'),
    - parcelas marcadas ('@'),
    - parcelas limpas sem mina ('?')
    - parcelas limpas minada ('X')

    parcela_para_str : parcela -> str
    '''
    #TODO caso nao for um destes casos
    if eh_parcela_tapada(p):
        return '#'
    elif eh_parcela_marcada(p):
        return '@'
    elif eh_parcela_limpa(p):
        if not eh_parcela_minada(p):
            return '?'
        elif eh_parcela_minada(p):
            return 'X'
    return ' '


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
    return [[cria_parcela() for _ in range(coluna_para_int(col) + 1)]
            for _ in range(lin)]


def cria_copia_campo(campo):
    '''
    Construtor

    Recebe um campo e devolve uma nova copia do campo

    cria_copia_campo: campo -> campo
    '''
    return [copia_campo[:] for copia_campo in campo]


def obtem_ultima_coluna(campo):
    '''
    Seletor

    Devolve a cadeia de caracteres que corresponde a ultima coluna do
    campo de minas

    obtem_ultima_coluna: campo -> str
    '''
    return int_para_coluna(len(campo[0]) - 1)


def obtem_ultima_linha(campo):
    '''
    Seletor

    Devolve o valor inteiro que corresponde a ultima linha do campo de minas

    obtem_ultima_linha: campo -> int
    '''
    return len(campo)


def obtem_parcela(campo, coord):
    '''
    Seletor

    Devolve a parcela do campo m que se encontra na coordenada coord

    obtem_parcela: campo * coordenada -> parcela
    '''
    #print('obtem_parcela: ', coord)
    return campo[obtem_linha(coord)-1][coluna_para_int(obtem_coluna(coord))]


def obtem_coordenadas(campo, s):
    '''
    Seletor

    Devolve o tuplo formado pelas coordenadas ordenadas em ordem ascendente de
    esquerda a direita e de cima a baixo das parcelas dependendo do valor de s:
        - 'limpas' para as parcelas limpas,
        - 'tapadas' para as parcelas tapadas,
        - 'marcadas' para as parcelas marcadas, e
        - 'minadas' para as parcelas que escondem minas

    obtem_coordenadas: campo * str -> tuplo
    '''
    res_coord = ()
    tipos_de_s = ('limpas', 'tapadas', 'marcadas', 'minadas')
    func_de_s = (eh_parcela_limpa, eh_parcela_tapada,
                 eh_parcela_marcada, eh_parcela_minada)
    index_s = tipos_de_s.index(s)

    if s not in tipos_de_s:
        return res_coord

    for i in range(len(campo)):
        for j in range(len(campo[i])):
            coord = cria_coordenada(int_para_coluna(j), i+1)
            if func_de_s[index_s](obtem_parcela(campo, coord)):
                res_coord += (coord,)

    return res_coord



def obtem_numero_minas_vizinhas(campo, coord):
    '''
    Seletor

    Devolve o numero de parcelas vizinhas da parcela na coordenada coord que
    escondem uma mina.

    obtem_numero_minas_vizinhas: campo * coordenada -> int
    '''
    res_viz = 0
    coord_vizinhas = obtem_coordenadas_vizinhas(coord) # ainda pode vir coordenadas
    if len(coord_vizinhas) == 0:                       # que nao pertencem ao campo
        return 0

    for c in coord_vizinhas:
        if eh_coordenada_do_campo(campo, c):
            if eh_parcela_minada(obtem_parcela(campo, c)):
                res_viz += 1

    return res_viz


def eh_campo(arg):
    '''
    Reconhecedor

    Devolve True caso o seu argumento seja um TAD campo e False caso contrario
    Um TAD campo e uma lista de sublistas (de parcelas) com tamanho igual

    eh_campo: universal -> booleano
    '''
    return (isinstance(arg, list) and
            all(isinstance(i, list) and len(i) == len(arg[0]) and
                all(eh_parcela(j) for j in i) for i in arg))


def eh_coordenada_do_campo(campo, coord):
    '''
    Reconhecedor

    Devolve True se coord e uma coordenada valida dentro do campo

    eh_coordenada_do_campo: campo * coordenada -> booleano
    '''
    return (obtem_coluna(coord) <= obtem_ultima_coluna(campo) and
            obtem_linha(coord) <= obtem_ultima_linha(campo))


def eh_coord_campo_tapada(campo, coord):
    '''
    Reconhecedor

    Devolve True se coord e uma coordenada valida dentro do campo e a sua parcela
    tapada

    eh_coord_campo_tapada: campo * coordenada -> booleano
    '''
    return (eh_coordenada_do_campo(campo, coord) and
            eh_parcela_tapada(obtem_parcela(campo, coord)))


def campos_iguais(c1, c2):
    '''
    Teste

    Devolve True apenas se c1 e c2 forem campos e forem iguais

    campos_iguais: campo * campo -> booleano
    '''
    return (eh_campo(c1) and eh_campo(c2) and c1 == c2)


def campo_para_str(campo):
    '''
    Transformador

    Devolve uma cadeia de caracteres que representa o campo de minas como
    mostrado nos exemplos:
       ABCDE
      +-----+
    01|###2 |
    02|3##2#|
    03|1221 |
    04|###@#|
    05|#####|
      +-----+

    campo_para_str : campo -> str
    '''
    res_string = '   '
    tam_coluna = coluna_para_int(obtem_ultima_coluna(campo)) + 1
    # Criar coluna de A a coluna maxima do campo
    res_string += ''.join(chr(ord('A') + i) for i in range(tam_coluna))
    res_string += f'\n  +{"-"*tam_coluna}+\n'

    for i in range(obtem_ultima_linha(campo)):
        res_string += f'{i+1:0>2d}|' # numero de linha
        for j in range(tam_coluna):
            col = int_para_coluna(j)
            coord = cria_coordenada(col, i + 1)

            parcela_str = parcela_para_str(obtem_parcela(campo, coord))
            if parcela_str == '?': # verificar nº vizinhos para parcelas limpas
                                    # nao minadas
                n_vizinhos = obtem_numero_minas_vizinhas(campo, coord)
                parcela_str = ' ' if n_vizinhos == 0 else str(n_vizinhos)

            res_string += parcela_str

        res_string += '|\n' if i < obtem_ultima_linha(campo)-1 else \
            f'|\n  +{"-"*tam_coluna}+'

    return res_string


def coloca_minas(campo, coord, gerador, n):
    '''
    Funcao alto nivel

    Modifica destrutivamente o campo m escondendo n minas em parcelas dentro do
    campo. As n coordenadas sao geradas em sequencia utilizando o gerador g, de
    modo a que nao coincidam com a coordenada c nem com nenhuma parcela vizinha
    desta, nem se sobreponham com minas colocadas anteriormente

    coloca_minas: campo * coordenada * gerador * int -> campo
    '''
    coord_max = cria_coordenada(obtem_ultima_coluna(campo), obtem_ultima_linha(campo))
    while n > 0:
        coord_aleatoria = obtem_coordenada_aleatoria(coord_max, gerador)
        if (coord_aleatoria not in obtem_coordenadas_vizinhas(coord) and
            not coordenadas_iguais(coord_aleatoria, coord)):
            esconde_mina(obtem_parcela(campo, coord_aleatoria))
            n -= 1
    return campo


def limpa_campo(campo, coord):
    '''
    Funcao alto nivel

    Modifica destrutivamente o campo limpando a parcela na coordenada coord e o
    devolvendo-a. Se nao houver nenhuma mina vizinha escondida, limpa
    iterativamente todas as parcelas vizinhas. Caso a parcela se encontre ja limpa, a
    operacao nao tem efeito

    limpa_campo: campo * coordenada -> campo
    '''
    # TODO saber o output desta funcao é quebrar a abstracao??
    # TODO ainda nao esta perfeito??
    limpa_parcela(obtem_parcela(campo, coord))

    if (obtem_numero_minas_vizinhas(campo, coord) != 0 or
        eh_parcela_minada(obtem_parcela(campo, coord))):
        return campo

    stack_vizinhos = []
    #primeira iteracao da coordenada principal
    for v in obtem_coordenadas_vizinhas(coord):
        if (eh_coord_campo_tapada(campo, v)):
            stack_vizinhos.append(v)

    #print(stack_vizinhos)
    while len(stack_vizinhos) > 0:
        c_atual = stack_vizinhos.pop()
        limpa_parcela(obtem_parcela(campo, c_atual))
        # so se c_atual nao ter minas na vizinhanca e que vamos aos seus vizinhos
        if obtem_numero_minas_vizinhas(campo, c_atual) == 0:
            for v in obtem_coordenadas_vizinhas(c_atual):
                if (eh_coord_campo_tapada(campo, v) and
                    v not in stack_vizinhos):
                    stack_vizinhos.append(v)

    return campo



# Funcoes adicionais ***********************************************************
def jogo_ganho(campo):
    '''
    Funcao auxiliar que recebe um campo do jogo das minas e devolve True se
    todas as parcelas sem minas se encontram limpas, ou False caso contrario

    jogo_ganho: campo -> booleano
    '''
    # verificando todas as parcelas tapadas, se uma delas nao tiver minas, o jogo
    # ainda nao acabou
    return not any(not eh_parcela_minada(obtem_parcela(campo, c))
                   for c in obtem_coordenadas(campo, 'tapadas'))


def turno_jogador(campo):
    '''
    Recebe um campo de minas e pede para escolher L ou M (limpar ou marcar) e a
    coordenada para limpar, caso L retorna False caso limpamos uma parcela com mina

    turno_jogador: campo -> booleano
    '''
    escolha = '0'
    while escolha not in ('L', 'M'):
        escolha = input('Escolha uma ação, [L]impar ou [M]arcar:')

    coord_input = '0'
    while not (eh_str_coordenada(coord_input) and
               eh_coordenada_do_campo(campo, str_para_coordenada(coord_input))):
        coord_input = input('Escolha uma coordenada:')

    if escolha == 'L':
        # TODO perguntar para limpar antes ou verificar antes?
        coord = str_para_coordenada(coord_input)
        limpa_campo(campo, coord)
        if eh_parcela_minada(obtem_parcela(campo, coord)):
            return False

    return True



def main():
    m = cria_campo('M',5)
    g = cria_gerador(32, 2)
    c = cria_coordenada('G', 3)
    m = coloca_minas(m, c, g, 5)
    print(turno_jogador(m))
    print(campo_para_str(m))

if __name__ == '__main__':
    main()