import os
from flask import render_template, url_for, flash, redirect, request, abort, session#, jsonify
from app.webapp import app#,  bcrypt #, db
from app.webapp.forms import MainForm

from app.Modules.SimilarityMeasures import vectorize_pair
from app.Modules.PDFtoTxt import PdfConverter
from app.Modules.SearchnGet import search, get_doc
from app.Modules.Compare import compare, match_proportion
import pickle
import numpy as np
from app.Modules.text_wrapper import TextWrapper, process_input_file
from os.path import getsize


@app.route("/", methods=['GET', 'POST'])
@app.route("/main", methods=['GET', 'POST'])
def main():
    form = MainForm()

    if form.validate_on_submit():
        if form.file.data and form.content.data:
            flash('Both TextField and FileField have content! Please empty one.', 'danger')
        elif form.file.data:
            file_path = save_file(form.file.data, 'file')
            type = os.path.splitext(form.file.data.filename)[1][1:]
            keyword = form.keyword.data
            if form.pdf_only.data:
                keyword += ' filetype:pdf'
            query = keyword
            num = form.num_files.data

            match, proportion = search_and_compare(file_path, type, query, num)
            session['match'] = match
            session['proportion'] = proportion
            return redirect(url_for('result'))

        elif form.content.data:
            file_path = save_file(form.content.data, 'text')
            type = 'txt'
            keyword = form.keyword.data
            if form.pdf_only.data:
                keyword += ' filetype:pdf'
            query = keyword
            num = form.num_files.data

            match, proportion = search_and_compare(file_path, type, query, num)
            session['match'] = match
            session['proportion'] = proportion
            return redirect(url_for('result'))
        else:
            flash('Both TextField and FileField are empty! Please fill in one of those two fields.', 'danger')

    return render_template('main.html', title='main', form = form)


def search_and_compare(file_path, type, query, num):
    text_wrapper1 = process_input_file(file_path, type)
    print(text_wrapper1.sentence_count)

    urls = search(query = query, num = num)

    processed_text_dirs = []
    processed_text_count = 0
    for url in urls:
        if processed_text_count == num:
            break
        try:
            processed_text_dir = get_doc(url, processed_text_count)
            if processed_text_dir is not None:
                processed_text_dirs.append(processed_text_dir)
                processed_text_count +=1
        except Exception:
            pass

    pkl_file = 'app/Models/SVM/svm_paraphrase_identification_model.sav'
    with open(pkl_file, 'rb') as file:
        pkl_model = pickle.load(file)

    match = {}
    for processed_text_dir in processed_text_dirs:
        try:
            match = compare(match, text_wrapper1 , processed_text_dir, pkl_model)
        except Exception as e:
            print(e)
            pass
            
    for processed_text_dir in processed_text_dirs:
        os.remove(processed_text_dir[0])
    print("Finished comparing!")

    proportion = match_proportion(match, text_wrapper1.sentence_count)

    print(proportion)
    os.remove(file_path)

    return match, proportion

def save_file(form_data, mode):

    if mode == 'file':
        _, f_ext = os.path.splitext(form_data.filename)
    else:
        f_ext = 'txt'

    # file_fn = 'uploaded' + f_ext
    # file_path = os.path.join('app/webapp/static/uploaded_files',file_fn)

    file_path = 'uploaded.' + f_ext

    if mode == 'file':
        form_data.save(file_path)
    else:
        with open(file_path,'w') as f:
            f.write(form_data)

    return file_path


@app.route("/result", methods=['GET', 'POST'])
def result():
    try:
        headings = ["Your sentence", "Source sentence", "Source", "Paraphrase probability"]
        proportion = session['proportion']
        match = session['match']
        data = []
        for key in match.keys():
            data.append([key]+match[key])
        return render_template('result.html', title='result', headings=headings, data=data, proportion_data = proportion)
    except Exception as e:
        print(e)
        form = MainForm()
        return redirect(url_for('main'))
