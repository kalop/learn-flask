from flask import Flask, render_template, request
from data import Articles
from flask_ldapconn import LDAPConn
from ldap3 import SUBTREE, MODIFY_REPLACE
from pprint import pprint
from flask_wtf import Form
from wtforms.fields.html5 import DateField

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
app.config['SECRET_KEY'] = 'secret'

ldap = LDAPConn(app)

Articles = Articles()
dic = {"key1":"Yes", "key2":"No"}

@app.route('/')
def index():

    #testLDAPmodify()
    #testLDAPcreate()

    return render_template('home.html')

def testLDAPcreate():
    attributes=  dict(
        uid= 'test5.user',
        givenName= 'Test5',
        sn= 'User',
        #cn= 'Test4 User',
        mail= 'test.user@ilimit.net'
    )

    ldapc = ldap.connection
    base ='cn=Test5 user,ou=people,dc=planetexpress,dc=com'
    filter = [ 'inetOrgPerson', 'person', 'top', 'organizationalPerson']

    #print ldapc.add(dn=base, object_class=filter, attributes=attributes, controls=None)

    #add passw
    user_dn = 'cn=Test4 user,ou=people,dc=planetexpress,dc=com'
    ldapc.extend.microsoft.unlock_account(user=user_dn)
    #ldapc.modify(user_dn, {'lockoutTime': [(MODIFY_REPLACE, ['0'])]}, controls=None)
    print ldapc.extend.microsoft.modify_password(user=user_dn, new_password='testpass', old_password=None)
    enable_account = {"userAccountControl": (MODIFY_REPLACE, [512])}
    print c.modify(user_dn=user_dn, changes=enable_account)


def testLDAPmodify():
    print "#################"
    #docker run --privileged -d -p 389:389 rroemhild/test-openldap

    ldapc = ldap.connection
    search_filter = '(cn=admin_staff)'

    attributes = ['cn','member']
    base ='ou=people,dc=planetexpress,dc=com'
    ldapc.search( base, search_filter, SUBTREE, attributes=attributes)
    pprint(ldapc.response)#print users

    #modificar membre
    newlist =  {'member': [(MODIFY_REPLACE,['cn=Albert Cabrerizo,ou=people,dc=planetexpress,dc=com','cn=Hermes Conrad,ou=people,dc=planetexpress,dc=com'])]}
    print ldapc.modify('cn=admin_staff,ou=people,dc=planetexpress,dc=com', newlist)

    ldapc.search( base, search_filter, SUBTREE, attributes=attributes)
    pprint(ldapc.response)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/articles')
def articles():
    return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
    return render_template('article.html', id = id)


class ExampleForm(Form):
    dt = DateField('DatePicker', format='%Y-%m-%d')

@app.route('/playWithForms', methods=['POST','GET'])
def playWithForms():
    form = ExampleForm()
    if form.validate_on_submit():
        print 'DATE:'
        print form.dt.data.strftime('%Y-%m-%d')
    return render_template('forms.html', data=dic,form=form)

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
