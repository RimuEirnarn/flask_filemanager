"""Application"""
from os.path import exists, isdir
from os.path import join as path_join
from socket import gethostname

from flask import Flask, abort, flash, redirect, render_template, request, send_file
from flask_login import login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename

from server.loginutil import LoginForm, get_user, login_manager
from server.utils import FileStat, filter_crumb, listdir, loadtomlfile, ROOT
from server.api import api

app = Flask(__name__)
app.config.update(loadtomlfile('config.toml'))
app.register_blueprint(api)
login_manager.init_app(app)

DUMMY_PATH = [FileStat("file.py"), FileStat("file.html")]


app.add_template_global(enumerate)


@app.template_global()
def make_crumb(crumb: str, crumbs: list[str]):
    if len(crumbs) == 1:
        return ''
    index = crumbs.index(crumb)
    current_crumbs = crumbs[:index+1]
    return '/'.join(current_crumbs)


@app.template_global()
def make_path(cwd, file):
    if cwd == "/":
        return file
    return path_join(cwd, file)


@app.route("/")
@login_required
def root():
    return redirect("/files")


@app.route("/files")
@app.route("/files/")
@login_required
def files():
    return render_template("index.html", cwd="/", crumbs=[''], files=listdir('/'))


@app.get("/files/<path:filepath>")
@login_required
def index_get(name="", filepath=""):
    _path = name + filepath
    path = ROOT / _path
    upload = request.args.get("upload", type=bool, default=False)
    files = listdir("/"+_path)
    if not exists(path):
        return render_template('error.html', name="Not Found", code=404, description=f"Huh, it seems like '{str(path.absolute())}' does not exists."), 404
    if isdir(path):
        if upload:
            return render_template("upload.html", cwd=_path)
        return render_template("index.html", cwd=_path, crumbs=filter_crumb(_path), files=files)
    return send_file(path, as_attachment=True)
    # return path
    # return render_template("index.html", cwd=path, crumbs=filter_crumb(path), files=files)


@app.post("/files/<path:filepath>")
@login_required
def index_post(name="", filepath=""):
    _path = name + filepath
    path = ROOT / _path
    print(request.files)
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if not file.filename:
        flash('No selected file', 'error')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        file.save(path / filename)
        flash("File uploaded!", 'success')
        return redirect(request.url)
    return redirect(request.url)


@app.errorhandler(HTTPException)
def http_error(exc: HTTPException):
    return render_template("error.html", name=exc.name, code=exc.code, description=exc.description)


if app.config.get('debug', False) is False:
    @app.errorhandler(Exception)
    def main_error(_: Exception):
        name = "Internal Server Error"
        code = 500
        description = "Server crashed with its own bug! We will be back later."
        return render_template("error.html", name=name, code=code, description=description)


@app.get("/login")
def login_get():
    form = LoginForm()
    return render_template("login.html", systemname=gethostname(), form=form)


@app.post("/login")
def login_post():
    form = LoginForm()
    if not form.validate_on_submit():
        flash("Cannot login, validation error!", 'error')
        return render_template("login.html", systemname=gethostname(), form=form)
    user = get_user(form.username.data)
    if not user:
        flash("Cannot login, user does not exists", 'error')
        return render_template("login.html", systemname=gethostname(), form=form)
    if not check_password_hash(user.password, form.password.data):  # type: ignore
        flash("Cannot login, password is invalid", 'error')
        return render_template("login.html", systemname=gethostname(), form=form)
    login_user(user, True)
    return redirect("/")


@app.post("/logout")
@login_required
def logout_post():
    logout_user()
    return redirect('/')


@app.route('/crash')
@login_required
def raiser():
    raise Exception("Server crashed!")


@app.route('/error/<int:code>')
@login_required
def aborter(code: int):
    return abort(code)


if __name__ == '__main__':
    app.config['debug'] = True
    app.run(debug=True, threaded=True)
