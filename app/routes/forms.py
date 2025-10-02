from flask import Blueprint, render_template, redirect, request, flash
from flask_login import  current_user
from ..extensions import db
from ..models.forms import Form
forms = Blueprint('forms',__name__)

@forms.route('/all-forms')
def all_forms():
    if current_user.is_authenticated:
        forms = Form.query.all()
        return render_template('forms/all-forms.html',is_auth = current_user.name, forms = forms)
    else: return render_template('forms/all-forms.html')

@forms.route('/add-form', methods = ['POST', 'GET'])
def add_form():
    if current_user.is_authenticated:
        if request.method == 'POST':
            try:
                return render_template('forms/add-form-1.html',is_auth = current_user.name, num = int(request.form.get('num')))
            except: 
                i = 0
                names = ''
                answers = ''
                while True:
                    try:
                        names = names + request.form.get(f'name{i}')+';'
                        ans = request.form.get(f'ans{i}')
                        if ans: answers = answers + ans + ';'
                        else: answers = answers + '~;'
                        i+=1
                    except: break
                form = Form(name = request.form.get('name'), creator = current_user.name, creator_login = current_user.login, description = request.form.get('desc'), time = request.form.get('time'), questions = names, answers_to_questions = answers)
                db.session.add(form)
                db.session.commit()
                flash('Вы успешно создали форму!', 'succes')
                return redirect('/all-forms')
        else:
            return render_template('forms/add-form-1.html',is_auth = current_user.name)
    else: 
        flash("Зарегистрируйтесь чтобы создавать формы", 'alert')
        return redirect('/signup')

@forms.route('/form/<int:id>/task', methods = ['POST', 'GET'])
def form(id):
    if current_user.is_authenticated:
        if request.method == 'POST':
            score = 0
            form = Form.query.get(id)
            answers_to_questions = form.answers_to_questions.split(';')
            lenght = len(answers_to_questions)-1
            for i in range(lenght):
                if answers_to_questions[i]!='~' and request.form.get(f'que{i}')==answers_to_questions[i]:
                    score +=1
            if form.dids: 
                dids = list(form.dids)
                dids+=[current_user.name]
                form.dids = dids
                scores = list(form.scores)
                scores+=[str(score)]
                form.scores = scores
            else: 
                form.dids = [current_user.name]
                form.scores = [str(score)]
            db.session.commit()
            flash(f'Количество правильных ответов {score}/{lenght}', "succes")
            return render_template("forms/complete-form.html")
        else:
            form = Form.query.get(id)
            name = form.name
            questions = form.questions.split(';')
            answers_to_questions = form.answers_to_questions.split(';')
            num = len(list(form.questions.split(';')))-1
            if form: 
                return render_template('forms/select-form.html', name = name, questions = questions, answers_to_questions = answers_to_questions , num = num, is_auth=current_user.name)
            else: return 'Ошибка блин((('
    else: return abort(403)

@forms.route('/my-forms')
def my_forms():
    try:
        forms = Form.query.filter_by(creator_login=current_user.login).all()
        form_data = []
        for form in forms:
            results = []
            if form.dids and form.scores:
                lenght = len(form.dids)
                for i in range(lenght):
                    results.append({
                        'user': form.dids[i],
                        'score': form.scores[i]
                    })
            form_data.append({
                'form': form,
                'results': results
            })
        
        return render_template("forms/my-forms.html", form_data = form_data, length = lenght, is_auth = current_user.name)
    except: 
        flash('У вас ещё нет форм', 'alert')
        return redirect('/all-forms')