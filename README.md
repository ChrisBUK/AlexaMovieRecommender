# AlexaMovieRecommender
Some configuration and code for a simple Alexa based movie recommendation service.

## alexa_skill
This is the main part of the configuration that powers the skill in the amazon developer console.

The intents file represents all of the different individual functions the app can do when the user interacts with it.  Some of the intents have slots, which are variables provided by the user as part of a query.  For example, asking for a movie with a certain actor or from a specific genre.

The utterances file represents what the user can actually say to Alexa; each group might have a few slightly different ways of saying the same thing - this is to make the app more conversational and natural. When Alexa recognises one of these utterances, it is abstracted into a JSON payload representing the intent and any of the recognised slots, and sent to the parser.

Deployment: Copy/Paste into the relevant areas of the Alexa Skill setup; each file belongs in a different area.

## alexa_parser

Our alexa parser is written in Python 2.7 and runs on AWS as a lambda function. It's purpose is simply to receive JSON payloads from an interaction with Alexa - and return a payload back so that Alexa can converse with the user.

Each of the intents we specified in the skill (and any custom slot variables) corresponds to a function here, so that we can tell Alexa what to say in response to queries we expect to receive.

Deployment: Copy/Paste into the AWS Lamda function :-o

## movies_api

In order to present actual movies from the database when responding to requests; a quick n dirty movies API has been created using PHP and runs on an AWS elastic beanstalk instance (whatever that is!).

When Alexa needs to respond to an intent with real information; the parser will fetch data from this API in order to present it back.

Deployment: zip the contents of movies_api and upload to the elastic beanstalk instance.

## The User Journey

User speaks to Alexa -> Alexa determines user intent and sends to alexa_parser -> alexa_parser determines response (using movies_api if needed) -> Alexa speaks to user

