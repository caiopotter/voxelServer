import sys
import png
import time


def loadFile():
    try:
        arquivoFonte = sys.argv[1]
    except IndexError:
        arquivoFonte = '.\scripts\\png_exemplos\\dado.png'
    reader = png.Reader(filename=arquivoFonte)
    global listapixel, metadata, imagem_width, imagem_height, indice_rgbs
    imagem_width, imagem_height, pixels, metadata = reader.read_flat()
    listapixel = pixels.tolist()
    indice_rgbs = criar_indice_texturas()


def criar_indice_texturas():
    cont = 0
    pixels_rgb = []
    for z in range(0, imagem_height*2, 2):
        for i in range(0, imagem_width*2, 2):
            cor = pegarPixelAtual(cont)
            pixels_rgb.append('%s %s %s' % (str(cor[0]), str(cor[1]), str(cor[2])))
            cont = cont + 1
    lista_rgb = list(set(pixels_rgb))
    return {v: i for i, v in enumerate(lista_rgb)}


def pegarPixelAtual(index):
    if metadata['alpha']:
        rgbCount = 4
    else:
        rgbCount = 3
    return [listapixel[index*rgbCount], listapixel[(index*rgbCount)+1], listapixel[(index*rgbCount)+2]]


def preencherComZeroAEsquerda(cor):
    cor[0] = str(cor[0]).zfill(3)
    cor[1] = str(cor[1]).zfill(3)
    cor[2] = str(cor[2]).zfill(3)

    return cor


def DrawScene():
    cont = 0
    obj_file = open(".\\results\\teste.obj", "w+")
    obj_file.write('mtllib teste.mtl\n\n')
    mtl_file = open(".\\results\\teste.mtl", "w+")
    preencher_mtl_baseado_em_index(mtl_file)
    for z in range(0, imagem_height*2, 2):
        for i in range(0, imagem_width*2, 2):
            cor = pegarPixelAtual(cont)
            numero_textura = pegar_numero_textura(cor)
            cor = preencherComZeroAEsquerda(cor)
            y = int(str(cor[0]) + str(cor[1]) + str(cor[2])) / 10000000.0

            draw_in_file(obj_file, i, y, z, cont, numero_textura)

            cont = cont + 1

    mtl_file.close()
    obj_file.close()


def preencher_mtl_baseado_em_index(mtl_file):
    for rgb, i in iter(indice_rgbs.items()):
        mtl_file.write('newmtl texture%s\n' % (str(i)))
        array_rgb = rgb.split()
        mtl_file.write('Ka %s %s %s\n' % (str(float(array_rgb[0])/255.0), str(float(array_rgb[1])/255.0),
                                          str(float(array_rgb[2])/255.0)))
        mtl_file.write('Kd %s %s %s\n' % (str(float(array_rgb[0])/255.0), str(float(array_rgb[1])/255.0),
                                          str(float(array_rgb[2])/255.0)))
        mtl_file.write('illum 1\n\n')


def fill_mtl(m, cont, r, g, b):
    m.write('newmtl texture%s\n' % (str(cont)))
    m.write('Ka %s %s %s\n' % (str(r), str(g), str(b)))
    m.write('Kd %s %s %s\n' % (str(r), str(g), str(b)))
    m.write('illum 1\n\n')
    return [r, g, b, cont]


def draw_in_file(obj_file, x, y, z, i, numero_textura):

    obj_file.write('v %s 0.0 %s\n' % (str(x - 1), str(z + 1)))
    obj_file.write('v %s 0.0 %s\n' % (str(x + 1), str(z + 1)))
    obj_file.write('v %s %s %s\n' % (str(x + 1), str(y + 1), str(z + 1)))
    obj_file.write('v %s %s %s\n' % (str(x - 1), str(y + 1), str(z + 1)))

    obj_file.write('v %s 0.0 %s\n' % (str(x - 1), str(z - 1)))
    obj_file.write('v %s %s %s\n' % (str(x - 1), str(y + 1), str(z - 1)))
    obj_file.write('v %s %s %s\n' % (str(x + 1), str(y + 1), str(z - 1)))
    obj_file.write('v %s 0.0 %s\n\n' % (str(x + 1), str(z - 1)))

    obj_file.write('g face%s\n' % (str(i)))

    obj_file.write('usemtl texture%s\n' % (str(numero_textura)))
    obj_file.write('f %s// %s// %s// %s//\n' % (str(1 + (8 * i)), str(2 + (8 * i)), str(3 + (8 * i)), str(4 + (8 * i))))
    obj_file.write('f %s// %s// %s// %s//\n' % (str(5 + (8 * i)), str(6 + (8 * i)), str(7 + (8 * i)), str(8 + (8 * i))))
    obj_file.write('f %s// %s// %s// %s//\n' % (str(1 + (8 * i)), str(2 + (8 * i)), str(8 + (8 * i)), str(5 + (8 * i))))
    obj_file.write('f %s// %s// %s// %s//\n' % (str(2 + (8 * i)), str(8 + (8 * i)), str(7 + (8 * i)), str(3 + (8 * i))))
    obj_file.write('f %s// %s// %s// %s//\n' % (str(3 + (8 * i)), str(7 + (8 * i)), str(6 + (8 * i)), str(4 + (8 * i))))
    obj_file.write('f %s// %s// %s// %s//\n' % (str(1 + (8 * i)), str(5 + (8 * i)), str(6 + (8 * i)), str(4 + (8 * i))))


def pegar_numero_textura(rgb_atual):
    return indice_rgbs.get(' '.join(map(str, rgb_atual)))


def main():
    start = time.time()
    loadFile()
    DrawScene()
    end = time.time()
    print('tempo de execucao: %s' % (str(end - start)))
    sys.exit()


if __name__ == "__main__":
    main()