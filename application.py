import base64
import smtplib
import threading
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_socketio import SocketIO,emit,disconnect
from flask import Flask,render_template,request,jsonify,Response,redirect,url_for,session,copy_current_request_context
import os

from werkzeug.utils import secure_filename

import PasswordGeneration
import TokenController
import blogDataSource
import datasource
from threading import Lock

import encryption
import gdrive

TEMPLATE_DIR = os.path.abspath('./templates')
STATIC_DIR = os.path.abspath('./assets')
application = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

async_mode = None
application.config['SECRET_KEY'] = 'secret!'
socket_ = SocketIO(application, async_mode=async_mode, always_connect=True, engineio_logger=True)
thread_lock = Lock()
alllistfiles = []
listfiles = os.listdir("./templates/pythonBlogs")
for name in listfiles:
    alllistfiles.append(name)
listfiles = os.listdir("./templates/cryptoBlogs")
for name in listfiles:
    alllistfiles.append(name)
listfiles = os.listdir("./templates/generalBlogs")
for name in listfiles:
    alllistfiles.append(name)

fileTypes ={'.csv':'text/csv',
            'doc':'application/msword','docx':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'html':'text/html',
            'htm':'text/html',
            'jar':'application/java-archive',
            'jpeg':'image/jpeg',
            'jpg':'image/jpeg',
            'pdf':'application/pdf',
            'txt':'text/plain',
            'zip':'application/zip'}

@application.route('/')
def home():
    return render_template('home.html' , email = "no" , user = '' , status = 'l' , reset = '0')

@application.route('/return')
def projectreturn():
    return render_template('home.html' , email = "no" , user = '' , status = 'l' , reset = '4')

@application.route('/<email>/courses')
def courses(email):
    return render_template('courses.html' , email = email)



@application.route('/<email>/websites')
def websites(email):
    return render_template('websitesBuilding.html' , email = email)


@application.route('/<email>')
def home_return(email):
    if email == 'no':
        return render_template('home.html', email=email, user='', status='l', reset="0")
    try:
        return render_template('home.html' , email = email , user = session[email] , status = 'y' , reset = "0")
    except:
        return render_template('home.html', email='no', user='', status='l', reset="0")

@application.route('/blogs/searching/<email>' , methods = ["POST" , "GET"])
def SearchEngine(email):
    if request.method == "POST":
        searchkey = request.form['searchquery']
    return redirect(url_for('gotoblog' , msg = searchkey+"-"+email))


@application.route('/blogs/<email>/<searchkey>')
def blogs(searchkey , email):
    return redirect(url_for('gotoblog' , msg = searchkey+"-"+email))
    #render_template("blogs.html" , search = searchkey)

@application.route("/blog/<msg>")
def gotoblog(msg):
    try:
        return render_template("blogs.html" , search = msg.split("-")[0] , email = msg.split("-")[1])
    except:
        return render_template('home.html', email='no', user='', status='l', reset="0")

# @application.route('/pythonsleep')
# def newblogs():
#     return render_template("generalBlogs/generalBlogs.highsalaryItcompanies.html")

@application.route('/login-validate' , methods = ["POST" , "GET"])
def login_validate():
    if request.method == "POST":
        email = request.form['email']
        passd = request.form['pass']
        passd = encryption.encryptMessage(passd)
        res,user = datasource.checkLoginUser(email, passd)

        if res:
            session[email] = user
            return redirect(url_for('home_return', email = email))

    return render_template('home.html' , email = 'no' , user = '' , status = 'n' , reset = '6')


def sendTempPass(email,passd,name):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('solutionsforeverything3@gmail.com', 'halosfe00201')
        msg = 'Password for sfe : '+passd
        message = MIMEMultipart('alternative')
        message['Subject'] = "Password for successful sign-in"
        message['From'] = "Solutions For Everything"
        message['To'] = name

        link = "soltionsforeverything.com"

        build_msg = buildpassmail(name,msg,link)
        part = MIMEText(build_msg, 'html')
        message.attach(part)
        server.sendmail('solutionsforeverything3@gmail.com', email, message.as_string())
        server.quit()
        print('Successful!!!')
    except Exception as e:
        print(e)
        print('Failed')






def buildpassmail(name,msg,link) :
    return "<div style=\"font-family:Helvetica,Arial,sans-serif;font-size:16px;margin:0;color:#0b0c0c\">\n" +                "\n" +                "<span style=\"display:none;font-size:1px;color:#fff;max-height:0\"></span>\n" + "\n" +"  <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;min-width:100%;width:100%!important\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n" +     "    <tbody><tr>\n" +                "      <td width=\"100%\" height=\"53\" bgcolor=\"#0b0c0c\">\n" +"        \n" +                "        <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;max-width:580px\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" align=\"center\">\n" +                "          <tbody><tr>\n" +                "            <td width=\"70\" bgcolor=\"#0b0c0c\" valign=\"middle\">\n" +                "                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +                "                  <tbody><tr>\n" +                "                    <td style=\"padding-left:10px\">\n" +                "                  \n" +                "                    </td>\n" +            "                    <td style=\"font-size:28px;line-height:1.315789474;Margin-top:4px;padding-left:10px\">\n" +                "                      <span style=\"font-family:Helvetica,Arial,sans-serif;font-weight:700;color:#ffffff;text-decoration:none;vertical-align:top;display:inline-block\">Message Received</span>\n" +                "                    </td>\n" +                "                  </tr>\n" +               "                </tbody></table>\n" +                "              </a>\n" +                "            </td>\n" +                "          </tr>\n" +                "        </tbody></table>\n" +                "        \n" +                "      </td>\n" +                "    </tr>\n" +                "  </tbody></table>\n" +                "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +                "    <tbody><tr>\n" +                "      <td width=\"10\" height=\"10\" valign=\"middle\"></td>\n" +            "      <td>\n" +                "        \n" +                "                <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +                "                  <tbody><tr>\n" +                "                    <td bgcolor=\"#1D70B8\" width=\"100%\" height=\"10\"></td>\n" +                "                  </tr>\n" +                "                </tbody></table>\n" +                "        \n" +                "      </td>\n" +                "      <td width=\"10\" valign=\"middle\" height=\"10\"></td>\n" +                "    </tr>\n" +                "  </tbody></table>\n" +                "\n" +                "\n" +                "\n" +                "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +                "    <tbody><tr>\n" +                "      <td height=\"30\"><br></td>\n" +                "    </tr>\n" +               "    <tr>\n" +                "      <td width=\"10\" valign=\"middle\"><br></td>\n" +                "      <td style=\"font-family:Helvetica,Arial,sans-serif;font-size:19px;line-height:1.315789474;max-width:560px\">\n" +                "        \n" +                "            <p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\">Hi " + name + ",</p><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> "+ msg +" </p><blockquote style=\"Margin:0 0 20px 0;border-left:10px solid #b1b4b6;padding:15px 0 0.1px 15px;font-size:19px;line-height:25px\"><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> <a href=\"" +link+ "\">Click here to login</a> </p></blockquote>\n  <p>See you soon</p>" +                "        \n" +                "      </td>\n" +                "      <td width=\"10\" valign=\"middle\"><br></td>\n" +                "    </tr>\n" +                "    <tr>\n" +                "      <td height=\"30\"><br></td>\n" +                "    </tr>\n" +                "  </tbody></table><div class=\"yj6qo\"></div><div class=\"adL\">\n" +"\n" + "</div></div>";




@socket_.on('/google_signin' , namespace='/googlesignin')
def google_signin(message):
    uname = message['uname']
    college = '--'
    email = message['email']
    photo = message['photo']
    res = datasource.checkUser(email)
    passd = PasswordGeneration.generate()

    passe = passd

    passd = encryption.encryptMessage(passd)

    if res == False:
        datasource.addgooglesignin(email,uname,college, photo , passd)
        th = threading.Thread(target=sendTempPass, args=(email, passe,uname))
        th.start()
        session[email] = uname

    # emit('/success' , {"email" : email , "count" : c})


@application.route('/signup_validation' ,  methods = ["POST" , "GET"])
def signup_validate():
    if request.method == "POST":
        uname = request.form['uname']
        email = request.form['email']
        passd = request.form['pass']
        passd = encryption.encryptMessage(passd)
        res = datasource.addUser(uname, email, passd)
        if res:
            return render_template('home.html', email = 'no' , user='', status='l', reset='3')
        session[email] = uname
        return redirect(url_for('home_return', email=email))


def sendMail(name,sub,msg,to):

    datasource.sentUserMsg(name , sub , msg , to)

    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('solutionsforeverything3@gmail.com', 'halosfe00201')
        msg = 'Thank you for your response , our maintainance will respond you as soon as we can...'
        message = MIMEMultipart('alternative')
        message['Subject'] = "Message recieved"
        message['From'] = "Solutions For Everything"
        message['To'] = name
        build_msg = buildmail(name,msg)
        part = MIMEText(build_msg, 'html')
        message.attach(part)
        server.sendmail('solutionsforeverything3@gmail.com', to, message.as_string())
        server.quit()
        print('Successful!!!')
    except Exception as e:
        print(e)
        print('Failed')


def buildmail(name,msg,link = 'https://www.youtube.com/channel/UCgTQBk8L_aQz6p9kj9rutqQ') :
    return "<div style=\"font-family:Helvetica,Arial,sans-serif;font-size:16px;margin:0;color:#0b0c0c\">\n" +                "\n" +                "<span style=\"display:none;font-size:1px;color:#fff;max-height:0\"></span>\n" + "\n" +"  <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;min-width:100%;width:100%!important\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n" +     "    <tbody><tr>\n" +                "      <td width=\"100%\" height=\"53\" bgcolor=\"#0b0c0c\">\n" +"        \n" +                "        <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;max-width:580px\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" align=\"center\">\n" +                "          <tbody><tr>\n" +                "            <td width=\"70\" bgcolor=\"#0b0c0c\" valign=\"middle\">\n" +                "                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +                "                  <tbody><tr>\n" +                "                    <td style=\"padding-left:10px\">\n" +                "                  \n" +                "                    </td>\n" +            "                    <td style=\"font-size:28px;line-height:1.315789474;Margin-top:4px;padding-left:10px\">\n" +                "                      <span style=\"font-family:Helvetica,Arial,sans-serif;font-weight:700;color:#ffffff;text-decoration:none;vertical-align:top;display:inline-block\">Message Received</span>\n" +                "                    </td>\n" +                "                  </tr>\n" +               "                </tbody></table>\n" +                "              </a>\n" +                "            </td>\n" +                "          </tr>\n" +                "        </tbody></table>\n" +                "        \n" +                "      </td>\n" +                "    </tr>\n" +                "  </tbody></table>\n" +                "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +                "    <tbody><tr>\n" +                "      <td width=\"10\" height=\"10\" valign=\"middle\"></td>\n" +            "      <td>\n" +                "        \n" +                "                <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +                "                  <tbody><tr>\n" +                "                    <td bgcolor=\"#1D70B8\" width=\"100%\" height=\"10\"></td>\n" +                "                  </tr>\n" +                "                </tbody></table>\n" +                "        \n" +                "      </td>\n" +                "      <td width=\"10\" valign=\"middle\" height=\"10\"></td>\n" +                "    </tr>\n" +                "  </tbody></table>\n" +                "\n" +                "\n" +                "\n" +                "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +                "    <tbody><tr>\n" +                "      <td height=\"30\"><br></td>\n" +                "    </tr>\n" +               "    <tr>\n" +                "      <td width=\"10\" valign=\"middle\"><br></td>\n" +                "      <td style=\"font-family:Helvetica,Arial,sans-serif;font-size:19px;line-height:1.315789474;max-width:560px\">\n" +                "        \n" +                "            <p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\">Hi " + name + ",</p><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> "+ msg +" </p><blockquote style=\"Margin:0 0 20px 0;border-left:10px solid #b1b4b6;padding:15px 0 0.1px 15px;font-size:19px;line-height:25px\"><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> <a href=\"" +link+ "\">Subscribe</a> </p></blockquote>\n  <p>See you soon</p>" +                "        \n" +                "      </td>\n" +                "      <td width=\"10\" valign=\"middle\"><br></td>\n" +                "    </tr>\n" +                "    <tr>\n" +                "      <td height=\"30\"><br></td>\n" +                "    </tr>\n" +                "  </tbody></table><div class=\"yj6qo\"></div><div class=\"adL\">\n" +"\n" + "</div></div>";





@application.route('/contact' , methods = ["POST","GET"])
def contact():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        sub = request.form['subject']
        msg = request.form['message']


        th = threading.Thread(target=sendMail, args=(name,sub,msg, email))
        th.start()

    return "OK"


def sendForgotMail(email,token):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('solutionsforeverything3@gmail.com', 'halosfe00201')
        message = MIMEMultipart('alternative')
        message['Subject'] = "Reset Password"
        message['From'] = "Solutions For Everything"
        message['To'] = email
        link = "https://www.solutionsforeverything/reset_password?token=" + token
        build_msg = build_reset_mail(link,email)
        part = MIMEText(build_msg, 'html')
        message.attach(part)
        server.sendmail('solutionsforeverything3@gmail.com', email, message.as_string())
        server.quit()
        print('Successful!!!')
    except Exception as e:
        print(e)
        print('Failed')


def build_reset_mail(link,email):
    return "<div style=\"font-family:Helvetica,Arial,sans-serif;font-size:16px;margin:0;color:#0b0c0c\">\n" +                "\n" +                "<span style=\"display:none;font-size:1px;color:#fff;max-height:0\"></span>\n" +               "\n" +                "  <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;min-width:100%;width:100%!important\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n" +                "    <tbody><tr>\n" +                "      <td width=\"100%\" height=\"53\" bgcolor=\"#0b0c0c\">\n" +                "        \n" +                "        <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;max-width:580px\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" align=\"center\">\n" +                "          <tbody><tr>\n" +                "            <td width=\"70\" bgcolor=\"#0b0c0c\" valign=\"middle\">\n" +                "                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +                "                  <tbody><tr>\n" +                "                    <td style=\"padding-left:10px\">\n" +                "                  \n" +                "                    </td>\n" +                "                    <td style=\"font-size:28px;line-height:1.315789474;Margin-top:4px;padding-left:10px\">\n" +                "                      <span style=\"font-family:Helvetica,Arial,sans-serif;font-weight:700;color:#ffffff;text-decoration:none;vertical-align:top;display:inline-block\">Confirm your email</span>\n" +                "                    </td>\n" +                "                  </tr>\n" +                "                </tbody></table>\n" +                "              </a>\n" +                "            </td>\n" +                "          </tr>\n" +                "        </tbody></table>\n" +                "        \n" +                "      </td>\n" +            "    </tr>\n" +             "  </tbody></table>\n" +            "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +            "    <tbody><tr>\n" +             "      <td width=\"10\" height=\"10\" valign=\"middle\"></td>\n" +            "      <td>\n" +           "        \n" +             "                <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +            "                  <tbody><tr>\n" +             "                    <td bgcolor=\"#1D70B8\" width=\"100%\" height=\"10\"></td>\n" +            "                  </tr>\n" +            "                </tbody></table>\n" +            "        \n" +             "      </td>\n" +            "      <td width=\"10\" valign=\"middle\" height=\"10\"></td>\n" +            "    </tr>\n" +             "  </tbody></table>\n" +             "\n" +         "\n" +       "\n" +         "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +             "    <tbody><tr>\n" +           "      <td height=\"30\"><br></td>\n" +          "    </tr>\n" +          "    <tr>\n" +           "      <td width=\"10\" valign=\"middle\"><br></td>\n" +              "      <td style=\"font-family:Helvetica,Arial,sans-serif;font-size:19px;line-height:1.315789474;max-width:560px\">\n" +                "        \n" +                "            <p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\">Hi " + email + ",</p><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> You are trying to reset you password. Please click on the below link to reset your password: </p><blockquote style=\"Margin:0 0 20px 0;border-left:10px solid #b1b4b6;padding:15px 0 0.1px 15px;font-size:19px;line-height:25px\"><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> <a href=\"" + link + "\">Reset Now</a> </p></blockquote>\n Link will expire in 30 minutes. <p>See you soon</p>" +                "        \n" +                "      </td>\n" +        "      <td width=\"10\" valign=\"middle\"><br></td>\n" +                "    </tr>\n" +                "    <tr>\n" +                "      <td height=\"30\"><br></td>\n" +               "    </tr>\n" +                "  </tbody></table><div class=\"yj6qo\"></div><div class=\"adL\">\n" +               "\n" +                "</div></div>";


@application.route('/reset_password' , methods = ["POST","GET"])
def reset_password():
    token = request.args.get('token')
    email = TokenController.verifyToken(token)
    if email == None :
        return "token invalid or expierd"
    else:
        return render_template('reset.html', user= email)



@application.route('/update_resetting_password' , methods = ["POST","GET"])
def change_pass():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        password = encryption.encryptMessage(password)

        datasource.updatePassword(email,password)
    return render_template('home.html', email = 'no' ,  user = '' , status = 'l' , reset = "2")




@application.route('/forgot_validation' , methods = ["POST","GET"])
def reset_mail():
    if request.method == "POST":

        email = request.form['email']
        email_exist = datasource.checkUser(email)
        if email_exist == False:
            return "Email does not exist"
        new_token = TokenController.genarateToken(email)
        th = threading.Thread(target=sendForgotMail, args=(email,new_token,))
        th.start()
        return render_template('home.html' , email = "no" ,  user = "", status = 'l' , reset = '1')

@application.route('/profile/<email>')
def profile(email):
    uname , college ,gender , photo= datasource.getProfileDetails(email)


    return render_template("profile.html" , email = email , user = uname ,college = college , gender = gender ,photo = photo)

@socket_.on('/update_user' , namespace='/update')
def update_profile(message):
    print('success socket')
    uname = message['name']
    college = message['college']
    email = message['email']
    gender = message['gender']
    datasource.updateProfile(email , uname ,college , gender)




@application.route('/profile/<email>/update_pic' , methods = ["GET", "POST"])
def upload_file(email):
    if request.method == 'POST':
        f = request.files['file']

        f.save(secure_filename(f.filename))

        time.sleep(3)

        with open(f.filename, "rb") as img_file:
            my_string = base64.b64encode(img_file.read())



        os.remove("./"+f.filename)
        res = "data:"+str(f.content_type)+";base64,"+ str(my_string)
        datasource.updatePhoto(email, res)



    return redirect(url_for('profile' , email = email))




@socket_.on('/check' , namespace='/update')
def ckeckUserProfile(message):
    email = message['email']
    try :
        if session[email] :
            emit('res_check' , {'status' : "ok"})
    except :
        emit('res_check', {'status' : "notok"})

@socket_.on('/return_home' , namespace='/returnhome')
def returnHome(message):
    email = message['email']
    render_template('home.html', email=email, user=session[email], status='y', reset="0")


@application.route('/proj/searchingproject/<email>' , methods = ["POST" , "GET"])
def Searchproj(email):
    if request.method == "POST":
        key = request.form['searchquery']
    return redirect(url_for('projects',email = email , key = key))

@application.route('/projects/<email>/<key>')
def projects(email , key):
    try :
        if session[email] :
            pass
    except :
        return redirect(url_for('projectreturn'))
    return redirect(url_for('projects2',key = key+"-"+email))

@application.route('/proj/<key>')
def projects2(key):
    email = key.split("-")[1]
    key = key.split("-")[0]
    try:
        return render_template("projects.html", search=key, email=email, user=session[email])
    except:
        return render_template('home.html', email='no', user='', status='l', reset="0")


@socket_.on('/getList' , namespace='/get_list')
def send_blogs(message):
    searchkey = message['search']
    if searchkey == "total":
        listfiles = os.listdir("./templates/pythonBlogs")
        for name in listfiles:
            imagelink, desc = blogDataSource.getdetails(name)
            emit('/res_check', {"fname": name, "imglink": imagelink, "desc": desc})
        listfiles = os.listdir("./templates/cryptoBlogs")
        for name in listfiles:
            imagelink, desc = blogDataSource.getdetails(name)
            emit('/res_check', {"fname": name, "imglink": imagelink, "desc": desc})
        listfiles = os.listdir("./templates/generalBlogs")
        for name in listfiles:
            imagelink, desc = blogDataSource.getdetails(name)
            emit('/res_check', {"fname": name, "imglink": imagelink, "desc": desc})
    else :
        keys =  searchkey.split(" ")
        matchedfiles = set()
        for k in keys:
            for name in alllistfiles:
                if checkmatch(name.lower(),k.lower()):
                    matchedfiles.add(name)
        for name in matchedfiles:
            imagelink, desc = blogDataSource.getdetails(name)
            emit('/res_check', {"fname": name, "imglink": imagelink, "desc": desc})



def checkmatch(name,searchkey):
    d = 256
    q = 101


    M = len(searchkey)
    N = len(name)
    i = 0
    j = 0
    t = 0
    p = 0
    h = 1


    for i in range(M - 1):
        h = (h * d) % q

    for i in range(M):
        p = (d * p + ord(searchkey[i])) % q
        t = (d * t + ord(name[i])) % q

    for i in range(N - M + 1):

        if p == t:
            # Check for characters one by one
            for j in range(M):
                if name[i + j] != searchkey[j]:
                    break
                else:
                    j += 1
            if j == M:
                return True


        if i < N - M:
            t = (d * (t - ord(name[i]) * h) + ord(name[i + M])) % q

            if t < 0:
                t = t + q
    return False


@application.route("/profile/<email>/logout")
def logout(email):
    session.pop(email)
    return redirect(url_for('home'))


@application.route("/addblog" , methods = ["GET" , "POST"])
def addBlog():
    if request.method == "POST":
        bname = request.form['bname']
        bimage = request.form['bimage']
        bdesc = request.form['bdes']
        blogDataSource.add(bname , bimage , bdesc)

    return render_template("admin.html")


@socket_.on('/getProjectList' , namespace= "/get_projectlist")
def getProjectList(msg):
    search = msg["search"].lower()
    temp = []

    temp = blogDataSource.search(search)

    for row in temp:
        emit('/res_check1' , {"name" : row["name"] , "image" : row["image"] , "desc" : row["desc"] , "url" : row["url"]})

@application.route("/addproject" , methods = ["GET" , "POST"])
def addProject():
    if request.method == "POST":
        pname = request.form['pname']
        pimage = request.form['pimage']
        pdesc = request.form['pdes']
        purl = request.form['purl']
        blogDataSource.addProject(pname , pimage , pdesc , purl)

    return render_template("admin.html")



@application.route("/open_blog/<email>/<name>" )
def openBlog(email , name):
    return render_template(name.split(".")[0]+"/"+name , email = email )


@application.route("/profile/<email>/projupload" , methods = ["POST"])
def projupload(email):
    pname = request.form['pname']
    pdesc = request.form['pdesc']
    purl = request.form['purl']
    blogDataSource.adduserprojects(email , pname , pdesc , purl)
    sendProjMail(email)
    return redirect(url_for("profile" , email = email))

def sendProjMail(email):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('solutionsforeverything3@gmail.com', 'halosfe00201')
        message = MIMEMultipart('alternative')
        message['Subject'] = "Thanks for uploaded the your Project"
        message['From'] = "Solutions For Everything"
        message['To'] = email
        link = "soltionsforeverything.com"
        build_msg = build_proj_mail(link,email)
        part = MIMEText(build_msg, 'html')
        message.attach(part)
        server.sendmail('solutionsforeverything3@gmail.com', email, message.as_string())
        server.quit()
        print('Successful!!!')
    except Exception as e:
        print(e)
        print('Failed')


def build_proj_mail(link,email):
    return "<div style=\"font-family:Helvetica,Arial,sans-serif;font-size:16px;margin:0;color:#0b0c0c\">\n" +                "\n" +                "<span style=\"display:none;font-size:1px;color:#fff;max-height:0\"></span>\n" +               "\n" +                "  <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;min-width:100%;width:100%!important\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n" +                "    <tbody><tr>\n" +                "      <td width=\"100%\" height=\"53\" bgcolor=\"#0b0c0c\">\n" +                "        \n" +                "        <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;max-width:580px\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" align=\"center\">\n" +                "          <tbody><tr>\n" +                "            <td width=\"70\" bgcolor=\"#0b0c0c\" valign=\"middle\">\n" +                "                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +                "                  <tbody><tr>\n" +                "                    <td style=\"padding-left:10px\">\n" +                "                  \n" +                "                    </td>\n" +                "                    <td style=\"font-size:28px;line-height:1.315789474;Margin-top:4px;padding-left:10px\">\n" +                "                      <span style=\"font-family:Helvetica,Arial,sans-serif;font-weight:700;color:#ffffff;text-decoration:none;vertical-align:top;display:inline-block\">Thanks for uploaded</span>\n" +                "                    </td>\n" +                "                  </tr>\n" +                "                </tbody></table>\n" +                "              </a>\n" +                "            </td>\n" +                "          </tr>\n" +                "        </tbody></table>\n" +                "        \n" +                "      </td>\n" +            "    </tr>\n" +             "  </tbody></table>\n" +            "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +            "    <tbody><tr>\n" +             "      <td width=\"10\" height=\"10\" valign=\"middle\"></td>\n" +            "      <td>\n" +           "        \n" +             "                <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +            "                  <tbody><tr>\n" +             "                    <td bgcolor=\"#1D70B8\" width=\"100%\" height=\"10\"></td>\n" +            "                  </tr>\n" +            "                </tbody></table>\n" +            "        \n" +             "      </td>\n" +            "      <td width=\"10\" valign=\"middle\" height=\"10\"></td>\n" +            "    </tr>\n" +             "  </tbody></table>\n" +             "\n" +         "\n" +       "\n" +         "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +             "    <tbody><tr>\n" +           "      <td height=\"30\"><br></td>\n" +          "    </tr>\n" +          "    <tr>\n" +           "      <td width=\"10\" valign=\"middle\"><br></td>\n" +              "      <td style=\"font-family:Helvetica,Arial,sans-serif;font-size:19px;line-height:1.315789474;max-width:560px\">\n" +                "        \n" +                "            <p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\">Hi " + email + ",</p><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> You are Project was uploaded.Thank you for uploaded.we will publish your Project soon. once we published that will add on your profile page. Please click on the below link to go home page : </p><blockquote style=\"Margin:0 0 20px 0;border-left:10px solid #b1b4b6;padding:15px 0 0.1px 15px;font-size:19px;line-height:25px\"><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> <a href=\"" + link + "\">Goto home Page</a> </p></blockquote>\n <p>See you soon</p>" +                "        \n" +                "      </td>\n" +        "      <td width=\"10\" valign=\"middle\"><br></td>\n" +                "    </tr>\n" +                "    <tr>\n" +                "      <td height=\"30\"><br></td>\n" +               "    </tr>\n" +                "  </tbody></table><div class=\"yj6qo\"></div><div class=\"adL\">\n" +               "\n" +                "</div></div>";



@application.route("/profile/<email>/blogupload" , methods = ["POST"])
def blogupload(email):
    bname = request.form['bname']
    bdesc = request.form['bdesc']

    f = request.files['bfile']

    if not secure_filename(f.filename) == "":
        fname = f.filename.replace(" ", "")
        f.save("./gfolder/"+secure_filename(fname))
        typee = f.filename.split('.')


        orgtypee = typee[-1]
        time.sleep(3)

        gdrive.addblogs(fname,fileTypes[orgtypee])
        time.sleep(3)

        os.remove("./gfolder/" + fname)
        sendBlogMail(email)

        blogDataSource.addBlogList(bname , bdesc , email)

    return redirect(url_for("profile" , email = email))

def sendBlogMail(email):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login('solutionsforeverything3@gmail.com', 'halosfe00201')
        message = MIMEMultipart('alternative')
        message['Subject'] = "Thanks for uploaded the blog"
        message['From'] = "Solutions For Everything"
        message['To'] = email
        link = "soltionsforeverything.com"
        build_msg = build_blog_mail(link,email)
        part = MIMEText(build_msg, 'html')
        message.attach(part)
        server.sendmail('solutionsforeverything3@gmail.com', email, message.as_string())
        server.quit()
        print('Successful!!!')
    except Exception as e:
        print(e)
        print('Failed')


def build_blog_mail(link,email):
    return "<div style=\"font-family:Helvetica,Arial,sans-serif;font-size:16px;margin:0;color:#0b0c0c\">\n" +                "\n" +                "<span style=\"display:none;font-size:1px;color:#fff;max-height:0\"></span>\n" +               "\n" +                "  <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;min-width:100%;width:100%!important\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\">\n" +                "    <tbody><tr>\n" +                "      <td width=\"100%\" height=\"53\" bgcolor=\"#0b0c0c\">\n" +                "        \n" +                "        <table role=\"presentation\" width=\"100%\" style=\"border-collapse:collapse;max-width:580px\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" align=\"center\">\n" +                "          <tbody><tr>\n" +                "            <td width=\"70\" bgcolor=\"#0b0c0c\" valign=\"middle\">\n" +                "                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +                "                  <tbody><tr>\n" +                "                    <td style=\"padding-left:10px\">\n" +                "                  \n" +                "                    </td>\n" +                "                    <td style=\"font-size:28px;line-height:1.315789474;Margin-top:4px;padding-left:10px\">\n" +                "                      <span style=\"font-family:Helvetica,Arial,sans-serif;font-weight:700;color:#ffffff;text-decoration:none;vertical-align:top;display:inline-block\">Thanks for uploaded</span>\n" +                "                    </td>\n" +                "                  </tr>\n" +                "                </tbody></table>\n" +                "              </a>\n" +                "            </td>\n" +                "          </tr>\n" +                "        </tbody></table>\n" +                "        \n" +                "      </td>\n" +            "    </tr>\n" +             "  </tbody></table>\n" +            "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +            "    <tbody><tr>\n" +             "      <td width=\"10\" height=\"10\" valign=\"middle\"></td>\n" +            "      <td>\n" +           "        \n" +             "                <table role=\"presentation\" width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse\">\n" +            "                  <tbody><tr>\n" +             "                    <td bgcolor=\"#1D70B8\" width=\"100%\" height=\"10\"></td>\n" +            "                  </tr>\n" +            "                </tbody></table>\n" +            "        \n" +             "      </td>\n" +            "      <td width=\"10\" valign=\"middle\" height=\"10\"></td>\n" +            "    </tr>\n" +             "  </tbody></table>\n" +             "\n" +         "\n" +       "\n" +         "  <table role=\"presentation\" class=\"m_-6186904992287805515content\" align=\"center\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" style=\"border-collapse:collapse;max-width:580px;width:100%!important\" width=\"100%\">\n" +             "    <tbody><tr>\n" +           "      <td height=\"30\"><br></td>\n" +          "    </tr>\n" +          "    <tr>\n" +           "      <td width=\"10\" valign=\"middle\"><br></td>\n" +              "      <td style=\"font-family:Helvetica,Arial,sans-serif;font-size:19px;line-height:1.315789474;max-width:560px\">\n" +                "        \n" +                "            <p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\">Hi " + email + ",</p><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> You are blog was uploaded.Thank you for uploaded.we will publish your blog soon. once we published that will add on your profile page. Please click on the below link to go home page : </p><blockquote style=\"Margin:0 0 20px 0;border-left:10px solid #b1b4b6;padding:15px 0 0.1px 15px;font-size:19px;line-height:25px\"><p style=\"Margin:0 0 20px 0;font-size:19px;line-height:25px;color:#0b0c0c\"> <a href=\"" + link + "\">Goto Home Page</a> </p></blockquote>\n <p>See you soon</p>" +                "        \n" +                "      </td>\n" +        "      <td width=\"10\" valign=\"middle\"><br></td>\n" +                "    </tr>\n" +                "    <tr>\n" +                "      <td height=\"30\"><br></td>\n" +               "    </tr>\n" +                "  </tbody></table><div class=\"yj6qo\"></div><div class=\"adL\">\n" +               "\n" +                "</div></div>";


@application.errorhandler(404)
def error_404():
    return render_template("404.html"),404

@application.errorhandler(403)
def error_403():
    return render_template("403.html"),403

@application.errorhandler(410)
def error_410():
    return render_template("410.html"),410

@application.errorhandler(500)
def error_500():
    return render_template("500.html"),500


if __name__ == "__main__":
    socket_.run(application,debug=True)


