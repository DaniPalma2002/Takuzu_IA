import requests


def html_to_matrix(text2):
    res = []
    text = text2.split('<p id="celpar')

    for el in text:
        if el[0] == '_' and el[1] in ('1', '2', '3', '4', '5', '6', '7', '8', '9') and el[2] in (
        '_', '1', '2', '3', '4', '5', '6', '7', '8', '9') and len(el) < 1000:
            res.append(el.split('/p'))

    aux = []
    for el in res:
        aux.append(el[0].split('\n'))

    resres = []
    for el in aux:
        resres.append(el[1].strip('<').strip())

    matrix = {}
    for i in range(14):
        for j in range(14):
            matrix[(i, j)] = 2

    for i in range(len(resres)):
        if resres[i] == '':
            continue
        matrix[(i % 14, i // 14)] = int(resres[i])
    text = text2.split('celpar_14_14')

    if text[1][0:100].split('/p')[0].strip('<').strip().strip('"').strip('>').strip() != '':
        matrix[(13, 13)] = int(text[1][0:100].split('/p')[0].strip('<').strip().strip('"').strip('>').strip())

    return matrix


def to_string_matrix(matrix):
    res = ''
    size = int(len(matrix) ** 0.5)
    for i in range(size):
        for j in range(size):
            if j != size - 1:
                res += str(matrix[(i, j)]) + '\t'
            else:
                res += str(matrix[(i, j)])
        res += '\n'
    return res[:len(res) - 1]

for i in range(1, 201):
    f = open(f'tests/test{i}.in', 'w')

    t = f'https://www.binarypuzzle.com/puzzles.php?size=14&level=4&nr={i}'
    r = requests.get(t)
    t = r.text
    res = '14\n' + to_string_matrix(html_to_matrix(t))
    print(i)

    f.write(res)
    f.close()