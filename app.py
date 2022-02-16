import os

from pymodm import connect

from database import Server
from other import human_date
from flask import *
from api import YandexCloudApi

connect(os.environ.get('MONGODB_COEX_CONNECTION'), alias="coex-cloud")

app = Flask(__name__)

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
app.secret_key = SECRET_KEY

app.jinja_env.filters['human_date'] = human_date
yc_api = YandexCloudApi()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        code = request.form.get('code').upper()
        try:
            server = dict(Server.objects.values().get({'access_code': code}))
        except Exception as e:
            return render_template('index.html', error='сервер не найден')

        if not server:
            return render_template('index.html', error='сервер не найден')
        else:
            instance_id = server.get('yc_id')
            status = yc_api.get_status(instance_id)
            if status == 'RUNNING':
                return render_template('vm.html', IP=server['ip'])
            elif status == 'STARTING':
                return render_template('index.html',
                                       message='Сервер запускается, обычно, это занимает не более 5 минут. '
                                               'Повторите подключение после запуска сервера.')
            else:
                yc_api.start_instance(instance_id)
                return render_template('index.html',
                                       message='Сервер был выключен. Запускаем сервер... '
                                               'Повторите подключение через минуту.')


def main():
    app.run(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    main()
