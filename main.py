from mongoengine import connect, errors
from odm.Book import Book
from flask import Flask, render_template, request, redirect, url_for
import datetime
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)
load_dotenv()

# environment variables
db_username = os.getenv("db_username")
db_password = os.getenv("db_password")
dbname = os.getenv("dbname")

connect(
    host=f"mongodb+srv://{db_username}:{db_password}@cluster0.iiowz.mongodb.net/{dbname}?retryWrites=true&w=majority"
)


@app.route("/")
def main_page():
    return redirect(url_for('book'))


@app.route("/books")
def book():
    lst = json.loads(Book.objects().to_json())
    for i in lst:
        i['published']['$date'] = datetime.datetime.fromtimestamp(int(i['published']['$date']) / 1000)
    return render_template("base.html", AllBooks=lst)


@app.route("/edit", methods=['GET'])
def edit_page():
    return render_template("main.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    try:
        book = Book(bid=request.form['id'], name=request.form['name'], author=request.form['author'],
                    published=request.form['date'])
        book.save()
        return "Added record Successfully"
    except errors.NotUniqueError as e:
        return "Book id already exist\n\n"+str(e)


@app.route('/view', methods=["POST"])
def view():
    query = {}
    if request.form['id'] != "":
        query['bid'] = int(request.form['id'])
    if request.form['name'] != "":
        query['name'] = request.form['name']
    if request.form['author']:
        query['author'] = request.form['author']
    if request.form['date'] != "":
        query['published'] = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d")
    books = Book.objects(__raw__=query)
    lst = json.loads(books.to_json())
    for i in lst:
        i['published']['$date'] = datetime.datetime.fromtimestamp(int(i['published']['$date'])/1000)
    return lst[0]


@app.route('/delete', methods=['GET', 'POST'])
def delete():
    query = {}
    if request.form['id'] != "":
        query['bid'] = int(request.form['id'])
    if request.form['name'] != "":
        query['name'] = request.form['name']
    if request.form['author']:
        query['author'] = request.form['author']
    if request.form['date'] != "":
        query['published'] = datetime.datetime.strptime(request.form['date'], "%Y-%m-%d")
    book = Book.objects(__raw__=query).delete()
    return "No of deleted records : "+str(book)


@app.route('/update', methods=['POST'])
def update():
    f_query = {}
    if request.form['fid'] != "":
        f_query['bid'] = int(request.form['fid'])
    if request.form['fname'] != "":
        f_query['name'] = request.form['fname']
    if request.form['fauthor']:
        f_query['author'] = request.form['fauthor']
    if request.form['fdate'] != "":
        f_query['published'] = datetime.datetime.strptime(request.form['fdate'], "%Y-%m-%d")
    print(f_query)

    r_query = {}
    if request.form['rid'] != "":
        r_query['bid'] = int(request.form['rid'])
    if request.form['rname'] != "":
        r_query['name'] = request.form['rname']
    if request.form['rauthor']:
        r_query['author'] = request.form['rauthor']
    if request.form['rdate'] != "":
        r_query['published'] = datetime.datetime.strptime(request.form['rdate'], "%Y-%m-%d")
    print(r_query)

    book = Book.objects(__raw__=f_query).update(__raw__={"$set": r_query})
    print(book)
    return "No of updated records : " + str(book)


@app.route('/delete_with_id', methods=['POST'])
def delete_with_id():
    b_id = int(request.args['id'])
    Book.objects(bid=b_id).delete()
    return redirect(url_for('book'))


if __name__ == '__main__':
    app.run(debug=True)
