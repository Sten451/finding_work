import time
import random
import requests
from flask import render_template, Blueprint, request, url_for, redirect
from flask import current_app
from finding_work.finding_work.main.api_hh import receive_all_id
from finding_work.finding_work.models import Post, db
from finding_work.finding_work.forms import NoteForm, StatusForm

main = Blueprint('main', __name__)


@main.route("/")
def home():
    statistics = {}
    if request.args.get('sort') == 'filter_exp':
        all = Post.query.filter(
            Post.status != 'CLOSED').order_by(Post.experience)
    elif request.args.get('sort') == 'filter_status':
        all = Post.query.filter(
            Post.status != 'CLOSED').order_by(Post.status)
    else:
        all = Post.query.filter(Post.status != 'CLOSED')
    statistics['all'] = Post.query.filter(Post.status != 'CLOSED').count()
    statistics['answer'] = Post.query.filter(Post.status == 'ANSWER').count()
    statistics['reject'] = Post.query.filter(Post.status == 'REJECT').count()
    return render_template('index.html', content=all, count=statistics)


@main.route("/detail/<int:post_id>", methods=['GET', 'POST'])
def detail(post_id):
    form = NoteForm()
    form2 = StatusForm()
    all = Post.query.filter(Post.status != 'CLOSED')
    post = Post.query.filter(Post.id == post_id).one()
    statistics = {}
    if request.method == 'GET':
        if post.note:
            form.note.data = post.note
        form2.status.data = post.status.name
    elif request.method == 'POST':
        if form.note.data and form.note.data != post.note:
            if form.validate_on_submit():
                post.note = form.note.data
                form2.status.data = post.status.name
                db.session.commit()
        if form2.validate_on_submit():
            post.status = form2.status.data
            db.session.commit()
            current_app.logger.warning(
                f'У вакансии с ID {post.id} - {post.author} был изменён статус.')
    statistics['all'] = Post.query.filter(Post.status != 'CLOSED').count()
    statistics['answer'] = Post.query.filter(Post.status == 'ANSWER').count()
    statistics['reject'] = Post.query.filter(Post.status == 'REJECT').count()
    return render_template('detail.html', content=all, count=statistics, post=post, form=form, form2=form2)


@main.route("/receive_data", methods=['GET', 'POST'])
def receive_data():
    if receive_all_id():
        current_app.logger.warning(
            f'База данных успешно обновлена.')
    else:
        current_app.logger.error(
            f'В процессе обновления произошли ошибки.')
    return redirect(url_for('main.home'))
