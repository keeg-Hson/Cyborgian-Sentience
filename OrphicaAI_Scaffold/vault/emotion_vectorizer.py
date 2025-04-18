# Emotion Vectorizer

#The ultimate purpose of this file is to access text based inputs and to return a dictionary. 
#this stored dcitionary willserve as a subset that scans the overall 'emotional tone' associated with each given user entry

#Output:
##will append dict classification, with an associated score (0-1) for each emotional category (closer to 1; higher user importance)
###example: {contentment: 0.8, distress: 0.2, etc...}

#USE: for: emotionla tagging in EchoVault, Determining memnory salience, future introspective processing

######-----STEPS-----#######
#1. Import necessary libraries
##kinda goes without saying lel
import re #regex processing 
from collections import defaultdict
from nltk.corpus import wordnet #for expanded keyword matching

#deals with keyword matching via nltk
def expand_keywords(base_keywords):
    """
    Expands the base keywords using WordNet synonyms.
    """
    expanded = set()
    for word in base_keywords:
        expanded.add(word)
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                expanded.add(lemma.name().replace("_" , " ").lower())
    return list(expanded)


#2. define emotional categories: 
##to form basis of 'emotional vector' space
##categories to be pre defined here
###append values as necessary

EMOTION_CATEGORIES = [ #temporary placeholder for emotional categories
    "contentment",
    "distress",
    "anger",
    "fear",
    "sadness",
    "joy",
    "grief",
    "anticipation",
    "surprise",
    "disgust", 
]

#BASE EMOTION KEYWORDS
BASE_EMOTION_KEYWORDS = {
    "joy": ["joy", "happy", "delight"],
    "sadness": ["sad", "unhappy", "gloom"],
    "fear": ["fear", "scared", "terrified"],
    "anger": ["angry", "mad", "furious"],
    "grief": ["loss", "cry", "mourning"],
    "anticipation": ["excited", "hopeful", "eager"],
    "surprise": ["shocked", "amazed", "astonished"],
    "disgust": ["disgusted", "repulsed", "nauseated"],
    "contentment": ["satisfied", "calm", "peaceful"],
    "distress": ["anxious", "nervous", "troubled"]
}

#3. placeholder emotional keyword dict

###------------to be replaced with actual ML logic later on!--------###
##for prototyping purposes, we will define a preset array of keywords associated with each emotional category
EMOTION_KEYWORDS={ #"EMOTION_LABEL": ["WORD1", "WORD2", "WORD3", ...]
    
    emotion: expand_keywords(keywords)
    for emotion, keywords in BASE_EMOTION_KEYWORDS.items()

}

#4. processing logic
def preprocess(text:str)->str:
    """
    to serve purpose of cleaning up text inputs. 
    deals with normalization, lowercasing, and preparing text entires for further processing
    """
    text=text.lower()
    text=re.sub(r'[^\w\s]', '', text) #removes punctuation
    return text #lowercase normalization #to be defined later on: will effectively be  our final cleared up outputs


#5. emotional processing logic
def classify_emotions(text:str) -> dict:
    """
    to serve purpose of classifying emotional tone of user input. to return a dictionaly of detected user emotions along with their associated weight scores
    ex: {contentment: 0.8, distress: 0.2, etc...} 
    #all summate to 1.0, or at least should in theory.
    """

    text = preprocess(text) #preprocess to be defined here
    scores={emotion:0.0 for emotion in EMOTION_CATEGORIES} #initializes or dictionary for results
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for word in keywords:
            if word in text:
                scores[emotion] += 1 #incrementiong emotional scoring upon detected match

    
    total=sum(scores.values()) #sums all emotional scores
    if total > 0:
        for k in scores:
            scores[k]=round(scores[k]/total,3) #normalizes our emotioal vector to sumamte to 1.0
    else:
        scores['neutral']=1.0 #if no matches, neutral score of 1.0 is assigned by default

    #stripping of 0s for cleaner output
    emotion_vector={k: v for k, v in scores.items() if v > 0}
    return emotion_vector #returns dictionary of emotional scores, as per the user input


#Step 6: intensity estimation:
def estimate_intensity(text:str) -> float:
    text=preprocess(text) #preprocess to be defined here
    match_count=0 #initializes match count
    for keywords in EMOTION_KEYWORDS.values():
        for word in keywords:
            if word in text:
                match_count+=1 #incrementing upon detected match

    intensity_score = min(match_count/5.0,1.0) #crude normalizatoin
    return round(intensity_score,3)
    """ 
    placeholder function for future use: poses as an estimator for how emotionally 'intense' a a given entry is.
    #to be used fro adjusting memory salience factor

    #IDEAS#
    -concerning user input, classification factors could be based off of 
    exclamations, repetition, strong word densities as far as idea importance/reinforcement patterns are concerned, 
    even word capitalization (etc etc etc.).... 
    """

    #return intensity_score #returns valuation between 0.0 and 1.0 (TO BE DEFINED!)

#---for debugging purposes!---!
if __name__ == "__main__":
    sample = "Not everything you lost was meant to stay. Some things left to make space for your real self to return."
    print("Emotion Vector:", classify_emotions(sample))
    print("Intensity Score:", estimate_intensity(sample))


    