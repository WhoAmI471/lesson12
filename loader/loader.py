import logging
import os
from flask import Blueprint, request, render_template, current_app
from functions import load_posts, uploads_posts


logging.basicConfig(encoding='utf-8', level=logging.INFO)


loader_blueprint = Blueprint('loader', __name__, url_prefix='/post', static_folder='static', template_folder='templates')


@loader_blueprint.route('/form/')
def form():
    return render_template('post_form.html')


@loader_blueprint.route("/upload/", methods=["POST"])
def upload():
    try:
        file = request.files['picture']
        filename = file.filename
        content = request.values['content']
        posts = load_posts()
        posts.append({
            'pic': os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
            'content': content
        })
        uploads_posts(posts)
        file.save(f'weather_bot/venv/lesson12_project_source_v3-master/uploads/images/{filename}')
        if filename.split('.')[-1] not in ['png', 'jpg', 'jpeg']:
            logging.info('Файл не изображение')
    except FileNotFoundError:
        logging.error('Ошибка при загрузке файла')
        return '<h1> Файл не найден! </h1>'
    else:
        return render_template('post_uploaded.html', pic=os.path.join(current_app.config['UPLOAD_FOLDER'], filename), content=content)

