from flask import Flask, render_template, request
from data import Articles
from flask_ldapconn import LDAPConn
from ldap3 import SUBTREE, MODIFY_REPLACE
from pprint import pprint

app = Flask(__name__)
#Reload the server every time something is changed
app.debug=True


##LDAP
LDAP_SERVER = '172.17.0.2'
LDAP_PORT = 389
LDAP_BINDDN = 'cn=admin,dc=planetexpress,dc=com'
LDAP_SECRET = 'GoodNewsEveryone'
LDAP_USE_TLS = False


app.config['LDAP_SERVER'] = LDAP_SERVER
app.config['LDAP_PORT'] = LDAP_PORT
app.config['LDAP_BINDDN'] = LDAP_BINDDN
app.config['LDAP_SECRET'] = LDAP_SECRET
app.config['LDAP_USE_TLS'] = LDAP_USE_TLS

ldap = LDAPConn(app)


###

Articles = Articles()
dic = {"key1":"Yes", "key2":"No"}

@app.route('/')
def index():

    print "#################"
    ldapc = ldap.connection
    search_filter = '(cn=admin_staff)'

    attributes = ['cn','member']
    base ='ou=people,dc=planetexpress,dc=com'
    ldapc.search( base, search_filter, SUBTREE, attributes=attributes)
    pprint(ldapc.response)


    newlist =  [{'attributes': {u'member': [u'cn=Hubert J. Farnsworth,ou=people,dc=planetexpress,dc=com',
        u'cn=Hermes Conrad,ou=people,dc=planetexpress,dc=com'], u'cn': [u'admin_staff']}}]



    newlist =  {'member': [MODIFY_REPLACE,(['cn=Albert Cabre,ou=people,dc=planetexpress,dc=com','cn=Hermes Conrad,ou=people,dc=planetexpress,dc=com'])]}

    print ldapc.modify('cn=admin_staff,ou=people,dc=planetexpress,dc=com', newlist)

    ldapc.search( base, search_filter, SUBTREE, attributes=attributes)
    pprint(ldapc.response)

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
