from middleware import check_extension,generate_token,get_metadata
from flask import Flask,render_template,url_for,request,flash,make_response,send_file
import os,hashlib
import datetime
import jwt
from jwt import ExpiredSignatureError
from jwt import InvalidSignatureError,DecodeError
from customexception import ApiLimitExceed

apiuser={'b068931cc450442b63f5b3d276ea4297':0}

app=Flask(__name__,static_folder='./public',template_folder='./templates')
app.secret_key="abcdefghi"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/gallery')
def gallery():
    images=sorted(os.listdir('./public/images'),reverse=True) #sorting images on their upload time
    return render_template('gallery.html',images=images) #display all images in gallery.html tenplate

@app.route('/upload',methods=['POST'])
def upload():
    if request.method=='POST':
        f=request.files['image']
        if f.filename == '':
            flash('No selected file','error')
            return render_template('home.html')
            
        if check_extension(f.filename): #check extension method call of file only image are allow
            name=str(int(datetime.datetime.timestamp(datetime.datetime.now())))+os.path.splitext(f.filename)[-1].lower() #image name according to timestamp
            f.save(os.path.join('./public/images',name))
            flash('Success','success') 
            return render_template('home.html') 
        else:
            flash('Choose .jpg,.png,.jpeg file','error')
            return render_template('home.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/generatekey',methods=["POST"])
def generate_key():
    # Generate key on basis of name of user
    key=hashlib.md5(request.form.get('name').encode()).hexdigest()
    # if already present in apiuser dictionary then just return key
    if key not in apiuser:
        # Generate JWt token with initial count to 0 and expiration of 1 minute and store in apiuser dict
        apiuser[key]=generate_token(key,0,datetime.datetime.timestamp(datetime.datetime.now()+datetime.timedelta(seconds=60)))
    return key

@app.route('/imageapi',methods=["GET","POST"])
def imageapi():
    # parse key and image from url
    key=request.args.get('key')
    image=request.args.get('image')
    if key in apiuser:
        token=apiuser[key]
        try:
            # decode token
            data=jwt.decode(token,'apirate',algorithms='HS256')
            # if count is less or equal to 5 then proceed otherwise raise limit exceed exception
            if data['count']<6:
                count=data['count']+1
                token1=generate_token(key,count,data['exp']) #set expiration to previous expiration value till 1 minute complete
                apiuser[key]=token1
                return get_metadata(f'./public/images/{image}')
            else:
                raise ApiLimitExceed()
        except ExpiredSignatureError as sign:
            # after 1 minute token expired and raised expire signature error so generate token with count 1 and return specified image
            token1=generate_token(key,1,datetime.datetime.timestamp(datetime.datetime.now()+datetime.timedelta(seconds=60)))
            apiuser[key]=token1
            return get_metadata(f'./public/images/{image}')
        except InvalidSignatureError as sign:
            token1=generate_token(key,1,datetime.datetime.timestamp(datetime.datetime.now()+datetime.timedelta(seconds=60)))
            apiuser[key]=token1
            return get_metadata(f'./public/images/{image}')
        except DecodeError as sign:
            token1=generate_token(key,1,datetime.datetime.timestamp(datetime.datetime.now()+datetime.timedelta(seconds=60)))
            apiuser[key]=token1
            return get_metadata(f'./public/images/{image}')
            
        except ApiLimitExceed as ALE:
            # return Limit exceed message
            return ALE.message

if __name__=="__main__":
    app.run(debug=True)
    
