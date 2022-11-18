from pytz import timezone 
from zoneinfo import ZoneInfo

import jwt
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
from flask_cors import CORS
from flask_mail import Mail, Message
import pdfkit
import uuid
from functools import wraps
import datetime

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
ma = Marshmallow(app)
cors = CORS(app)
mail = Mail(app)


#<------------------------------------------MODELS------------------------------------------------>

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True) 
    public_id = db.Column(db.String(50), unique=True) 
    email = db.Column(db.String(50),unique=True)
    username = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(80))
    admin= db.Column(db.Boolean)

class Deck(db.Model):
    __tablename__ = 'deck'

    deck_id = db.Column(db.String)
    deck_name = db.Column(db.String(100),primary_key=True )
    creator = db.Column(db.String(100),db.ForeignKey('user.username'), nullable=False)
    score = db.Column(db.Float, nullable=True)
    last_reviewed = db.Column(db.String(50), nullable=True)

    user = db.relationship('User')

class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.String, primary_key=True)
    part_of_deck = db.Column(db.ForeignKey('deck.deck_id'), nullable=False)
    front = db.Column(db.String(100), nullable=False)
    back = db.Column(db.String(100), nullable=False)
    partial = db.Column(db.Integer)

    deck = db.relationship('Deck')


#<-------------------------------------------SCHEMA----------------------------------------------->


class UserSchema(ma.Schema):
    class Meta:
        fields=("public_id","email","username", "password")
        model = User

user_schema= UserSchema()
users_schema= UserSchema(many=True)

class DeckSchema(ma.Schema):
    class Meta:
        fields=("deck_id","deck_name", "creator", "score","last_reviewed")
        model = Deck

deck_schema= DeckSchema()
decks_schema= DeckSchema(many=True)

class CardSchema(ma.Schema):
    class Meta:
        fields=("card_id", "part_of_deck","front","back","partial")
        model = Card

card_schema= CardSchema()
cards_schema= CardSchema(many=True)

#<------------------------------------------Flask-Mail------------------------------------------------>

def send_monthly_email():
    with app.app_context():
        users = User.query.all()
        for user in users:
            decks=Deck.query.filter_by(creator=user.username).all()
            report= render_template("report.html", decks=decks)

            pdf = pdfkit.from_string(report, False )
            msg = Message("Monthly Report by Flashcards App",
                    recipients=[user.email])
            msg.attach("Monthly-Report.pdf","application/pdf",pdf)
            mail.send(msg)
        return "E-mails sent!"

def send_daily_email():
    with app.app_context():
        users = User.query.all()
        for user in users:
            msg = Message("Daily Reminder by Flashcards App",
                    recipients=[user.email])
            msg.body("Hey! How are you doing? \n Hope you're okay. Time to review some cards now!\n \nWith love from Flashcards App")
            mail.send(msg)
        return "E-mails sent!"

#<------------------------------------------Decorator------------------------------------------------>

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Internal server error!'}),401
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message' : 'User not logged in!'}),401

        current_user = User.query.filter_by(public_id=data['public_id']).first()
        return f(current_user, *args, **kwargs)

    return decorated
#<------------------------------------------Auth------------------------------------------------>

@app.route('/login', methods=['POST'])
def login(): # login to account
        username = request.form.get("username")
        password = request.form.get("password")
        user=User.query.filter_by(username=username).first()
        if user==None:
            return jsonify({"message": "User does not exist."}),400
        user=User.query.filter_by(username=username,password=password).first()
        if user:  
            token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=3)}, app.config['SECRET_KEY'])
            return jsonify({'token' : token , 'message':'login successful!'}),200
        else:
            return jsonify({"message": "Password not correct."}),400

@app.route('/register', methods=['POST'])
def register():  #create user
    email=request.form.get('email')
    username=request.form.get('username')
    password=request.form.get('password')
    if username == "" or email == "" or password == "":
        return jsonify({'message':'Username, email or password cannot be empty. Please try again.'}),400
    
    user=User.query.filter_by(username=username).first()
    if user:
        return jsonify({'message':'User already exists.'}),400
    
    user=User.query.filter_by(email=email).first()
    if user:
        return jsonify({'message':'Email already in use.'}),400
    new_user = User(
        public_id=str(uuid.uuid4()),
        email=email,
        username=username,
        password=password,
        admin=False
    )
    db.session.add(new_user)
    db.session.commit()
    
    user=User.query.filter_by(username=username,password=password).first()
    token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=3)}, app.config['SECRET_KEY'])
    return jsonify({'token' : token , 'message':'New User created, login successful!'}),200


#<------------------------------------------User------------------------------------------------>
   
@app.route('/users')
@token_required
def users(current_user): #get all users - for admin
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}),403
    users = User.query.all()
    return jsonify(users_schema.dump(users))

@app.route('/user')
@token_required    
def user(current_user): #get one user - for admin
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}),403
    username = request.form.get('username')
    user=User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({'message':'User does not exist'}),400
    
    return jsonify(user_schema.dump(user))

@app.route('/promotion', methods=['PUT'])    
@token_required
def promotion(current_user): #promotion - for admin
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'}),403
    username=request.form.get('username')
    user=User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message':'User does not exist'}),400
    user.admin=True
    db.session.commit()
    return jsonify({'message':'User has been promoted'}),200

#<------------------------------------------Decks----------------------------------------------->
@app.route('/decks')
@token_required
def decks(current_user): #get all decks of user
    decks = Deck.query.filter_by(creator=current_user.username).all()
    if decks:
        return jsonify(decks_schema.dump(decks))
    return jsonify({"message":"No decks to display. Create a new one."}),400


@app.route('/deck', methods=['POST'])
@token_required
def newdeck(current_user): #create deck
    deck_name=request.form.get('deck_name')
    if deck_name == "":
        return jsonify({'message':'Deck name cannot be empty. Please try again.'}),400

    deck = Deck.query.filter_by(deck_name=deck_name, creator=current_user.username).first()
    if deck:
        return jsonify({'message':'Deck already exists'}),400
    
    new_deck = Deck(
        deck_id=str(uuid.uuid4()),
        deck_name=request.form.get('deck_name'),
        creator=current_user.username,
        score=None,
        last_reviewed=None
    )
    db.session.add(new_deck)
    db.session.commit()
    return_deck = Deck.query.filter_by(deck_name=deck_name, creator=current_user.username).first()

    return jsonify({'deck_id':return_deck.deck_id}),200

@app.route('/deck/<deck_id>', methods=['PUT'])
@token_required
def editdeck(current_user,deck_id): #edit deck
    new_deck_name=request.form.get('new_deck_name')
    
    if new_deck_name == "":
        return jsonify({'message':'Deck cannot be empty. Please try again.'}),400

    deck = Deck.query.filter_by(deck_name=new_deck_name,creator=current_user.username).first()
    if deck:
        return jsonify({'message':'Deck already exists'}),400
    
    Deck.query.filter_by(deck_id=deck_id).update(
    dict(deck_name=new_deck_name))
    db.session.commit()
    return jsonify({'message':'Deck name has been updated'}),200

@app.route('/deck/<deck_id>', methods=['DELETE'])
@token_required
def deldeck(current_user, deck_id): # delete deck
    cards = Card.query.filter_by(part_of_deck=deck_id).all()
    for card in cards:
        db.session.delete(card)
    deck = Deck.query.filter_by(deck_id=deck_id).first()
    db.session.delete(deck)
    db.session.commit()
    return jsonify({'message':'Deck has been deleted'}),200
 
@app.route('/<deck_id>')
@token_required
def return_deck_name(current_user, deck_id):
    deck = Deck.query.filter_by(deck_id=deck_id,creator=current_user.username).first()
    deckname=deck.deck_name
    return jsonify({"deckname": deckname})

#<------------------------------------------Cards------------------------------------------------>


@app.route('/cards/<deck_id>')    
@token_required
def cards(current_user,deck_id): # get all cards 
    cards = Card.query.filter_by(part_of_deck=deck_id).all()
    for card in cards:
        if card:
            return jsonify(cards_schema.dump(cards))
    return jsonify({"message":"No cards in deck. Create a new one."}),400

@app.route('/carde/<card_id>')    
@token_required
def get_card(current_user,card_id): # get all cards 
    card = Card.query.filter_by(card_id=card_id).first()
    return jsonify({"front":card.front, "back": card.back}),200


@app.route('/newcard/<deck_id>', methods=['POST'])
@token_required   
def newcard(current_user,deck_id): # create new card
    front = request.form.get('front')
    back = request.form.get('back')
    
    if front == "" or back == "":
        return jsonify({'message':'Card cannot be empty. Please try again.'}),400
    
    card = Card.query.filter_by(front=front, back=back, part_of_deck=deck_id).first()
    if card:
        return jsonify({'message':'Card already exists in deck.'}),400
    
    new_card = Card(
        card_id=str(uuid.uuid4()),
        part_of_deck=deck_id,
        front=front,
        back=back,
        partial=None
    )
    db.session.add(new_card)
    db.session.commit()
    return jsonify({'message':'Card created'}),200

@app.route('/card/<card_id>', methods=['PUT'])
@token_required    
def editcard(current_user,card_id): #edit card
    card = Card.query.get_or_404(card_id)
    
    front = request.form.get('front')
    back = request.form.get('back')
    if front == "" and back == "":
        return jsonify({'message':'No changes made, card remains same.'}),200

    card = Card.query.filter_by(front=front, back=back, part_of_deck=card.part_of_deck).first()
    if card:
        return jsonify({'message':'Card already exists in deck.'}),400

    card = Card.query.get_or_404(card_id)
    Card.query.filter_by(card_id=card_id,
                     part_of_deck=card.part_of_deck).update(dict(front=front))
    Card.query.filter_by(card_id=card_id,
                     part_of_deck=card.part_of_deck).update(dict(back=back))
    db.session.commit()
    return jsonify({'message':'Card has been updated', 'deck_id':card.part_of_deck}),200

@app.route('/card/<card_id>', methods=['DELETE'])
@token_required
def delcard(current_user,card_id): #delete card
    card = Card.query.get_or_404(card_id)
    db.session.delete(card)
    db.session.commit()
    return jsonify({'message':'Deck has been deleted'}),200


#<------------------------------------------Review and Time Update------------------------------------------------>

@app.route('/begin/<deck_id>')
@token_required
def begin(current_user,deck_id): # update last reviewd
    t = datetime.now()
    deck = Deck.query.filter_by(deck_id=deck_id,creator=current_user.username).first()
    deck.last_reviewed = t
    db.session.commit()
    return jsonify({'message':'Last reviewed updated'}),200

@app.route('/review/<card_id>', methods=["POST"])
@token_required
def review_next(current_user, card_id): #scoring 
    partialscore = request.form.get('partialscore') 
    card = Card.query.filter_by(card_id=card_id).first()
    card.partial = int(partialscore)
    db.session.commit() 
    cards = Card.query.filter_by(part_of_deck=card.part_of_deck).all()
    total = 0
    for cd in cards:
      if cd.partial== None:
        break
      else:
        total = total + cd.partial  
    count = Card.query.filter_by(part_of_deck=card.part_of_deck).count()
    new_score = int(total / count)  
    Deck.query.filter_by(deck_id=card.part_of_deck).update( dict(score=new_score))
    t =  datetime.datetime.now(tz=ZoneInfo('Asia/Kolkata')).strftime("%I:%M %p %d %b, %Y")
    Deck.query.filter_by(deck_id=card.part_of_deck).update( dict(last_reviewed=t))
    db.session.commit() 
    return jsonify({'message':'Partial Score and Deck Score Updated'}),200

#<------------------------------------------------------------------------------------------>

if __name__ == '__main__':
    app.run(debug=True, port= 8080)
