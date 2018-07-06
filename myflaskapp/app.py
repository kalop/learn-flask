from flask import Flask, render_template, request
from data import Articles

app = Flask(__name__)
#Reload the server every time something is changed
app.debug=True

Articles = Articles()
dic = {"key1":"Yes", "key2":"No"}

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)

@app.route('/playWithForms')
def playWithForms():

    return render_template('forms.html', data=dic)

@app.route('/changeValue', methods=['POST', 'GET'])
def changeValue():
    clau = request.form['valor']

    if dic[clau] == "Yes":
        dic[clau] = "No"
        return dic[clau]
    else:
        dic[clau] = "Yes"
        return dic[clau]


@app.route('/changePermission', methods=['POST', 'GET'])
def changePermission():
    permission = request.form['permission']
    print "get: " + permission
    if permission == 'Yes':
        bpermission = 'No'
    else:
        bpermission = 'Yes'
    print "return: " + bpermission
    return bpermission



if __name__ == '__main__':
    app.run()
