import urllib2
import json

ENABLE_REPEAT = True
IMAGE_BASE = "https://images.metadata.sky.com/pd-image/"
API_BASE   = "http://default-environment.vmbhrspg8y.us-east-1.elasticbeanstalk.com/"

def lambda_handler(event, context):
    
    #if (event["session"]["application"]["applicationId"] !=
    #        "amzn1.ask.skill.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx"):
    #    raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session): 
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetRandomMovie":
        return get_random_movie(intent, session)
    elif intent_name == "GetRandomMovieByGenre":
        return get_random_movie_by_genre(intent, session)
    elif intent_name == "GetRandomMovieByActor":
        return get_random_movie_by_actor(intent,session)
    elif intent_name == "GetRandomMovieByActorAndGenre":
        return get_random_movie_by_actor_and_genre(intent,session)        
    elif intent_name == "GetLatestMovies":
        return get_latest_movies(intent, session)
    elif intent_name == "GetLatestMoviesByGenre":
        return get_latest_movies_by_genre(intent, session)
    elif intent_name == "GetLatestMoviesByActor":
        return get_latest_movies_by_actor(intent, session)
    elif intent_name == "GetMovieInfo":
        return get_movie_info(intent, session)
    elif intent_name == "AMAZON.RepeatIntent":
        return get_last_response(intent, session)
    elif intent_name == "AMAZON.YesIntent":
        return get_yes_response(intent, session)
    elif intent_name == "AMAZON.NoIntent":
        return get_no_response(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response(session)
    elif intent_name == "EndInteraction" or intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    session_attributes = {}
    initial_speech = "Thank you for using Sky Cinema, remember we offer great new movies every day!"
    reprompt_speech = ""
    card = None
    should_end_session = True

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    return build_response(session_attributes, speechlet)

def get_welcome_response():
    session_attributes = {}
    initial_speech = "Welcome to the Alexa Sky Cinema skill. " \
                    "I'm here to help you to find something to watch. " \
                    "You can ask me to suggest a movie by genre or actor, or I can tell you about the latest titles. " \
                    "If you're feeling lucky, I can choose something at random that you might like."
                    
    reprompt_speech = "Please ask me to recommend a movie."

    card_title = "Get Movies from Sky Cinema"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False
    
    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    return build_response(session_attributes, speechlet)

def get_random_movie(intent, session):
    session_attributes = session.get('attributes', {})

    response = urllib2.urlopen(API_BASE + "?action=randomMovie")
    movie = json.load(response)

    session_attributes = create_attribute_current_movie(movie['movie']['title'], session_attributes)
    session_attributes = create_attribute_current_movie_id(movie['movie']['uuid'], session_attributes)

    initial_speech = "How about " + movie['movie']['title'] + "?"
    reprompt_speech = ""

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    session_attributes = create_attribute_conversation_context('initiateDownload', session_attributes)    
    return build_response(session_attributes, speechlet)

def get_random_movie_by_genre(intent, session):
    session_attributes = session.get('attributes', {})

    response = urllib2.urlopen(API_BASE + "?action=movieByGenre&genre=" + get_intent_genre(intent))
    movie = json.load(response)

    session_attributes = create_attribute_current_movie(movie['movie']['title'], session_attributes)
    session_attributes = create_attribute_current_movie_id(movie['movie']['uuid'], session_attributes)
  
    initial_speech = "Would you like to watch " + movie['movie']['title'] + "?"
    reprompt_speech = ""

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    session_attributes = create_attribute_conversation_context('initiateDownload', session_attributes)    
    return build_response(session_attributes, speechlet)

def get_random_movie_by_actor(intent, session):
    session_attributes = session.get('attributes', {})

    response = urllib2.urlopen(API_BASE + "?action=movieByActor&actor=" + get_intent_actor(intent))
    movie = json.load(response)

    session_attributes = create_attribute_current_movie(movie['movie']['title'], session_attributes)
    session_attributes = create_attribute_current_movie_id(movie['movie']['uuid'], session_attributes)
  
    initial_speech = intent['slots']['MovieActor']['value'] + " is in " + movie['movie']['title'] + ", would you like to watch it?"
    reprompt_speech = ""

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    session_attributes = create_attribute_conversation_context('initiateDownload', session_attributes)    
    return build_response(session_attributes, speechlet)

def get_random_movie_by_actor_and_genre(intent, session):
    session_attributes = session.get('attributes', {})

    response = urllib2.urlopen(API_BASE + "?action=movieByActorAndGenre&actor=" + get_intent_actor(intent) + "&genre=" + get_intent_genre(intent))
    movie = json.load(response)

    session_attributes = create_attribute_current_movie(movie['movie']['title'], session_attributes)
    session_attributes = create_attribute_current_movie_id(movie['movie']['uuid'], session_attributes)
  
    initial_speech = "A " + intent['slots']['MovieGenre']['value'] + " movie with " + intent['slots']['MovieActor']['value'] + ". How about " + movie['movie']['title'] + "?"
    reprompt_speech = ""

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    session_attributes = create_attribute_conversation_context('initiateDownload', session_attributes)    
    return build_response(session_attributes, speechlet)

def get_latest_movies(intent, session):
    session_attributes = session.get('attributes', {})

    initial_speech = "Here are three of the latest releases. " \
                     "Deadpool, an action thriller. " \
                     "Sully: Miracle on the Hudson, a drama based on real events. " \
                     "Finding Dory, an animated kids movie. " \
                     "Would you like to watch any of these?"

    reprompt_speech = ""

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    return build_response(session_attributes, speechlet)

def get_latest_movies_by_genre(intent, session):
    session_attributes = session.get('attributes', {})
    session_attributes = create_attribute_current_movie("Deadpool", session_attributes)

    initial_speech = "Deadpool is a great action movie, would you like to watch that?"
    reprompt_speech = ""

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    return build_response(session_attributes, speechlet)

def get_latest_movies_by_actor(intent, session):
    session_attributes = session.get('attributes', {})
    session_attributes = create_attribute_current_movie("Central Intelligence", session_attributes)
    
    initial_speech = "Dwayne Johnson was recently in Central Intelligence, would you like to watch that?"
    reprompt_speech = ""

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    return build_response(session_attributes, speechlet)

def get_movie_info(intent, session):
    response = urllib2.urlopen(API_BASE + "?action=movieByUuid&uuid="+session['attributes']['currentMovieId'])
    movie = json.load(response)

    session_attributes = session.get('attributes', {})
    session_attributes = create_attribute_current_movie(movie['movie']['title'], session_attributes)
    session_attributes = create_attribute_current_movie_id(movie['movie']['uuid'], session_attributes)
  
    initial_speech = movie['movie']['title'] + ": " + movie['movie']['synopsis'] + "."
    reprompt_speech = "Do you fancy " + movie['movie']['title'] + "?"

    card_title = "Movie Recommendation"
    card_text = initial_speech

    card = build_card("Simple", card_title, card_text)

    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    session_attributes = create_attribute_conversation_context('initiateDownload', session_attributes)
    return build_response(session_attributes, speechlet)

def get_yes_response(intent, session):
    session_attributes = session.get('attributes', {})
    context = session_attributes.get('currentContext', '')

    if context == 'initiateDownload':
        initial_speech = "OK, I'll download " + session_attributes['currentMovie'] + " to your Sky Q box now."
        reprompt_speech = ""
    else:
        initial_speech = "I don't know what you're saying yes to."
        reprompt_speech = "Ask me to suggest a movie."

    should_end_session = False
    card = None

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    session_attributes = create_attribute_conversation_context('None', session_attributes)
    return build_response(session_attributes, speechlet)


def get_no_response(intent, session):
    session_attributes = session.get('attributes', {})
    context = session_attributes.get('currentContext', '')

    if context == 'initiateDownload':
        initial_speech = "OK, I won't download that."
        reprompt_speech = "Ask me to suggest a movie."
    else:
        initial_speech = "I don't know what you're saying no to."
        reprompt_speech = "Ask me to suggest a movie."

    should_end_session = False
    card = None

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    session_attributes = create_attribute_conversation_context('None', session_attributes)
    return build_response(session_attributes, speechlet)

# --- Intent helpers ---

def get_intent_genre(intent):

    if intent['slots']['MovieGenre']['value'] == "science fiction":
        genre = "sci-fi"
    elif intent['slots']['MovieGenre']['value'] == "scary":
        genre = "horror"
    elif intent['slots']['MovieGenre']['value'] == "funny":
        genre = "comedy"
    else:
        genre = intent['slots']['MovieGenre']['value']

    return urllib2.quote(genre)

def get_intent_actor(intent):
    return urllib2.quote(intent['slots']['MovieActor']['value'])

def get_intent_title(intent):
    return urllib2.quote(intent['slots']['MovieTitle']['value'])

# --- Session helpers ---

def create_attribute_current_movie_id(uuid, session_attributes):
    session_attributes['currentMovieId'] = uuid
    return session_attributes

def create_attribute_current_movie(title, session_attributes):
    session_attributes['currentMovie'] = title
    return session_attributes

def create_attribute_current_genre(genre, session_attributes):
    session_attributes['currentGenre'] = genre
    return session_attributes

def create_attribute_current_actor(actor, session_attributes):
    session_attributes['currentActor'] = actor
    return session_attributes

def create_attribute_conversation_context(topic, session_attributes):
    session_attributes['currentContext'] = topic
    return session_attributes

def create_attribute_repeat(response, session_attributes):
    if ENABLE_REPEAT == True:
        session_attributes['lastResponse'] = response
        return session_attributes
    else:        
        return session_attributes

def get_last_response(intent, session):
    session_attributes = session.get('attributes', {})

    if "lastResponse" in session.get('attributes', {}):
        return build_response(session_attributes, session['attributes']['lastResponse'])

    initial_speech = "I didn't say anything." 
    reprompt_speech = ""
    card = None
    should_end_session = False

    speechlet = build_speechlet_response(card, initial_speech, reprompt_speech, should_end_session)
    session_attributes = create_attribute_repeat(speechlet, session_attributes)
    return build_response(session_attributes, speechlet)

# --- Response Payload Helpers ---

def build_speechlet_response(card, speech, reprompt_speech, should_end_session):
    
    if card == None:

        return {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": speech
                },
                "reprompt": {
                    "outputSpeech": {
                        "type": "PlainText",
                        "text": reprompt_speech
                    }
                },
                "shouldEndSession": should_end_session
            }

    else:

        return {
            "outputSpeech": {
                "type": "PlainText",
                "text": speech
            },
            "card": card,
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": reprompt_speech
                }
            },
            "shouldEndSession": should_end_session
        }

def build_card(type,title,text,small_image=None,large_image=None):

    if type == "standard":

        return {
            "type": "Standard",
            "title": title,
            "text": text,
            "image": {
                "smallImageUrl": small_image,
                "largeImageUrl": large_image
            }
        }

    else:

        return {
            "type": "Simple",
            "title": title,
            "content": text
        }
        
        
def build_response(session_attributes, speechlet_response):
    response = {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
        }

    return response
