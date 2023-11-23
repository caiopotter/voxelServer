import subprocess
import json
from flask import Flask
from proj_utils.fileUtils import converter_arquivo_base64
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/criar-voxel')
def cria_voxel():
    script_path = 'scripts/voxel.py'
    try:
        resultado = subprocess.check_output(["python", script_path])
        obj_base64 = converter_arquivo_base64('.\\results\\teste.obj')
        mtl_base64 = converter_arquivo_base64('.\\results\\teste.mtl')

        resposta = {
            "tempo": resultado.decode('utf-8'),
            "arquivo_obj": obj_base64,
            "arquivo_mtl": mtl_base64
        }

        json_data = json.dumps(resposta)

        return json_data
    except Exception as e:
        return 'Erro ao executar o script: ' + str(e)


if __name__ == '__main__':
    app.run()
