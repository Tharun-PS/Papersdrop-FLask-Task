from mongoengine import connect, errors
from odm.Book import Book
from flask import Flask, render_template, request, redirect, url_for
import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# environment variables
db_username = os.getenv("db_username")
db_password = os.getenv("db_password")
dbname = os.getenv("dbname")
print(db_username, db_password, dbname)

connect(
    host=f"mongodb+srv://{db_username}:{db_password}@cluster0.iiowz.mongodb.net/{dbname}?retryWrites=true&w=majority"
    # host="mongodb+srv://tharun:tharun123@cluster0.iiowz.mongodb.net/Book?retryWrites=true&w=majority"
)


@app.route("/")
def main_page():
    return redirect(url_for('book'))


@app.route("/books")
def book():
    lst = Book.objects().to_json()
    print(lst)
    return render_template("base.html", AllBooks=(Book.objects().to_json()))


@app.route("/edit", methods=['GET'])
def edit_page():
    return render_template("main.html")


@app.route("/add", methods=["GET", "POST"])
def add():
    try:
        book = Book(bid=request.form['id'], name=request.form['name'], author=request.form['author'],
                    published=request.form['date'])
        book.save()
        return render_template("main.html")
    except errors.NotUniqueError as e:
        print("Book id already exist")
        return render_template("main.html")


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
    return books.to_json()


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
        query['published'] = request.form['date']
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


if __name__ == '__main__':
    app.run(debug=True)
