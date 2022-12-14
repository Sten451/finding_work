from flask import render_template, Blueprint, request, url_for, redirect
from flask import current_app
from flask_login import login_required, current_user
from finding_work.main.api_hh import receive_all_id
from finding_work.models import Post, db
from finding_work.main.forms import NoteForm, StatusForm

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
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if current_user.user_status == 'GUEST':
        cur_user = 1
    else:
        cur_user = current_user.id
    form = NoteForm()
    form2 = StatusForm()
    all = Post.query.filter(Post.status != 'CLOSED',
                            Post.user_id == cur_user)
    post = Post.query.filter(
        Post.id == post_id, Post.user_id == cur_user).one()
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
                f'?? ???????????????? ?? ID {post.id} - {post.author} ?????? ?????????????? ????????????.')
    statistics['all'] = Post.query.filter(
        Post.status != 'CLOSED', Post.user_id == cur_user).count()
    statistics['answer'] = Post.query.filter(
        Post.status == 'ANSWER', Post.user_id == cur_user).count()
    statistics['reject'] = Post.query.filter(
        Post.status == 'REJECT', Post.user_id == cur_user).count()
    return render_template('detail.html', content=all, count=statistics, post=post, form=form, form2=form2)


@main.route("/receive_data", methods=['GET', 'POST'])
def receive_data():
    if receive_all_id():
        current_app.logger.warning(
            f'???????? ???????????? ?????????????? ??????????????????.')
    else:
        current_app.logger.error(
            f'?? ???????????????? ???????????????????? ?????????????????? ????????????.')
    return redirect(url_for('main.home'))
