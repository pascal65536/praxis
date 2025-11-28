from flask import Flask, render_template, request, flash, redirect, url_for
from extensions import db
from datetime import datetime
from models import City, GeneratedImage
import os
import sys
from flask_debugtoolbar import DebugToolbarExtension

# import logging
# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///temperature.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["UPLOAD_FOLDER"] = "static/generated_images"
app.config["FONT_FOLDER"] = "static/fonts"



db.init_app(app)

# Создаем папки если их нет
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["FONT_FOLDER"], exist_ok=True)

from utils import populate_sample_data, get_or_create_image
from queries import calc_city_optimized, calc_city_unoptimized, calc_citysemioptimized


@app.route("/")
def index():
    recent_images = (
        GeneratedImage.query.order_by(GeneratedImage.created_at.desc()).limit(8).all()
    )
    return render_template("index.html", recent_images=recent_images)


@app.route("/pictures")
@app.route("/pictures/<int:page>")
def pictures(page=1):
    per_page = 8
    images_pagination = GeneratedImage.query.order_by(
        GeneratedImage.created_at.desc()
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        "pictures.html", 
        pagination=images_pagination,
        images=images_pagination.items
    )


@app.route("/gena", methods=["GET", "POST"])
def gena():
    color_hex = request.args.get("color", "#3498db")
    if request.method == "POST":
        color_hex = request.form.get("color", "#3498db")
        check_existing = "check_existing" in request.form
        filename, is_existing = get_or_create_image(color_hex, check_existing)
        if filename:
            flash(
                f"Изображение создано! Цвет: {color_hex.upper()} {'(из кэша)' if is_existing else '(новое)'}",
                "success",
            )
            return redirect(url_for("gena", color=color_hex))
        else:
            flash("Не удалось создать изображение", "error")
    recent_images = (
        GeneratedImage.query.order_by(GeneratedImage.created_at.desc()).limit(4).all()
    )
    return render_template(
        "gena.html", recent_images=recent_images, color_hex=color_hex
    )


@app.route("/api/clear_images", methods=["POST"])
def clear_images():
    for image in GeneratedImage.query.all():
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], image.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    GeneratedImage.query.delete()
    db.session.commit()
    return redirect(url_for("pictures"))


@app.route("/weather1")
def weather1():
    """Оптимизированная версия - одно SQL-запрос с GROUP BY"""
    results = calc_city_optimized()
    results.sort(key=lambda x: x['city'])
    return render_template("query_results.html", data=results)


@app.route("/weather3")
def weather3():
    """Неоптимизированная версия - отдельный запрос для каждого города"""
    results = calc_city_unoptimized()
    results.sort(key=lambda x: x['city'])
    return render_template("query_results.html", data=results)


@app.route("/weather2")
def weather2():
    """Полуоптимизированная версия - отдельные агрегатные запросы для каждого города"""
    results = calc_citysemioptimized()
    results.sort(key=lambda x: x['city'])
    return render_template("query_results.html", data=results)


if __name__ == "__main__":
    # Устанавливаем debug режим из аргументов командной строки
    debug_mode = True
    app.debug = debug_mode
    app.config["DEBUG"] = debug_mode

    if debug_mode:
        # Отключаем профайлер
        app.config["DEBUG_TB_PROFILER_ENABLED"] = False
        app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
        app.config["SQLALCHEMY_RECORD_QUERIES"] = True

    if debug_mode:
        # Инициализируем DebugToolbar ПОСЛЕ установки debug режима
        toolbar = DebugToolbarExtension(app)


    with app.app_context():
        db.create_all()
        if db.session.query(City).count() == 0:
            print("Генерация тестовых данных...")
            populate_sample_data()
        else:
            print(f"В базе уже есть {db.session.query(City).count()} записей")

    print(f"Starting Flask application...")
    print(f"Debug mode: {'ENABLED' if app.debug else 'DISABLED'}")
    print(f"DebugToolbar: {'VISIBLE' if app.debug else 'HIDDEN'}")

    # app.run(debug=app.debug)
    app.run(debug=debug_mode, use_reloader=False)