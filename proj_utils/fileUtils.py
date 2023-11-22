import base64


def converter_arquivo_base64(caminho_arquivo):
    with open(caminho_arquivo, 'rb') as arquivo:
        conteudo = arquivo.read()

    base64_data = base64.b64encode(conteudo)
    base64_string = base64_data.decode('utf-8')

    return base64_string
