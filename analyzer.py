import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as sia
from nrclex import NRCLex

#####1- word categories #######
EMOTIONAL_WORDS = {
    # Anger / outrage
    "furious", "outraged", "infuriated", "enraged", "livid",
    "angry", "seething", "incensed", "irate",

    # Fear / threat
    "terrified", "horrified", "petrified", "alarmed", "panicked",
    "afraid", "fearful", "dread", "menacing", "threatening",

    # Disgust / contempt
    "disgusted", "repulsed", "sickened", "appalled", "revolted",
    "contempt", "despise", "loathe",

    # Moral outrage / condemnation
    "outrage", "scandal", "atrocity", "abomination", "injustice",
    "cruel", "brutal", "ruthless", "merciless", "vicious",

    # Strong negative affect (bias-prone)
    "hate", "hatred", "evil", "wicked", "monstrous",
    "tragic", "devastating", "catastrophic", "nightmare", "destroy", "destroyed", "destroying"
}

SENSATIONAL_WORDS = {
    "shocking", "breaking", "unbelievable", "explosive",
    "bombshell", "outrageous", "incredible", "insane",
    "mind-blowing", "jaw-dropping", "stunning", "astounding",
    "earth-shattering", "game-changing", "historic", "unprecedented",
    "massive", "huge", "gigantic", "colossal",
    "disaster", "catastrophe", "meltdown", "crisis",
    "scandal", "exposé", "revelation", "whistleblower",
    "secret", "hidden"
}

ABSOLUTE_WORDS = {
    "always", "never", "every", "everyone", "everybody",
    "no one", "nobody", "nothing", "nowhere",
    "all", "none", "everything", "anything",
    "completely", "totally", "absolutely", "entirely",
    "utterly", "fully", "wholly",
    "definitely", "certainly", "undoubtedly", "undeniably",
    "impossible", "inevitable", "guaranteed", "without exception"
}

LOADED_WORDS = {
    # Corruption / illegality
    "corrupt", "corruption", "crooked", "criminal", "fraud",
    "scam", "swindle", "embezzlement", "bribery", "kickback",

    # Authoritarian / oppressive framing
    "regime", "dictator", "tyrant", "oppressive", "repressive",
    "authoritarian", "totalitarian", "police state",

    # Extremism / radicalism
    "radical", "extremist", "fanatic", "zealot", "militant",

    # Character attacks
    "traitor", "sellout", "collaborator", "pawn", "puppet",
    "incompetent", "clueless", "pathetic", "useless", "worthless",

    # Greed / selfishness
    "greedy", "selfish", "predatory", "exploitative", "parasitic",

    # Propaganda / manipulation
    "propaganda", "spin", "lies", "deception", "cover-up",
    "smear", "witch hunt", "conspiracy"
}


URGENCY_WORDS = {
    "now", "immediately", "instantly", "right away",
    "hurry", "rush", "urgent", "emergency", "critical",
    "warning", "alert", "danger", "threat",
    "act", "do something", "share", "spread",
    "before it's too late", "last chance", "final warning","bad",
    "don't wait", "time is running out", "quickly"
}


MANIPULATIVE_PHRASES = {
    # Us vs them
    "us vs them", "ordinary people", "the elites",
    "people like us", "those people", "people in power",
    "the people in power", "real citizens", "true patriots",
    "the silent majority", "the corrupt establishment",

    # Conspiracy / secrecy
    "they don't want you to know", "what they're hiding",
    "the truth they don't want you to see",
    "mainstream media won't tell you", "covered up",
    "behind the scenes", "pulling the strings",

    # Moral panic / threat framing
    "under attack", "being destroyed", "our way of life is at risk",
    "this is an existential threat", "if we don't act now"
}

###INITIALIZE VADAR###
vadar=sia()

### basic text processing###
def tokenize(text):
    ##convert text into lowercase word tokens
    return re.findall(r'\b\w+\b',text.lower())

####find word based bias signals###
def find_category_words(words, category):
    ##finds words that belong to a perticular category
    return sorted(set(word for word in words if word in category))

#### CAPITALIZATION ANALYSIS###
def find_capatilized_words(text):
    words=re.findall(r'\b[A-Z]{3,}\b', text)
    return sorted(set(words))

#### EXCLAMATION / QUESTION ANALYSIS

def punctuation_signal(text):
    exclamation_count=text.count("!")
    question_count=text.count("?")
    return{
        "exclamation":exclamation_count,
        "question":question_count
    }
    
##### VADAR SENTIMENT ####
def analyze_sentiment(text):
    scores= vadar.polarity_scores(text)
    return{
        "positive": round(scores["pos"], 3),
        "negative": round(scores["neg"], 3),
        "neutral": round(scores["neu"], 3),
        "compound" :round(scores["compound"], 3)
    }
    
#### NRC EMOTION ANALYSIS###
def analyse_emotions(text):
    
    try:
        emotion=NRCLex(str(text))
        emotion.load_raw_text(str(text))
        scores=emotion.raw_emotion_scores
        #oonly return useful emotion categories
        categories=[
            "anger",
            "fear",
            "anticipation",
            "trust",
            "surprise",
            "sadness",
            "joy",
            "disgust"
        ]
        return{
            category: scores.get(category, 0)
            for category in categories
        }
    except Exception:
        #if nrc fails
        return{
              "anger":0,
              "fear":0,
               "anticipation":0,
               "trust":0,
               "surprise":0,
               "sadness":0,
               "joy":0,
               "disgust":0
        }

###PHASE BASED MANIPULATION DETECTION ##

def find_manupilative_phrases(text):
    lower_text = text.lower()
    found = []
    for phrase in MANIPULATIVE_PHRASES:
        if phrase in lower_text:
            found.append(phrase)
    return found

#### CALLCULATE BIAS SIGNAL SCORE ####

def calculate_bias_score(
    emotional_words,
    sensational_words,
    absolute_words,
    loaded_words,
    urgency_words,
    manipulative_phrases,
    capitalized_words,
    punctuation,
    sentiment
):
    score=0
    
    #word-based signals
    score+=len(emotional_words)*3
    score+=len(sensational_words)*3
    score+=len(absolute_words)*3
    score+=len(loaded_words)*3
    score+=len(urgency_words)*3
    
    #phrase-based manipulation
    score+=len(manipulative_phrases)*5
    
    #excessive capitalization
    score+=min(len(capitalized_words)*2,10)
    
    #excessive exclamation
    if punctuation["exclamation"]>=2:
        score+=5
        
    #very negative/positive
    compound=sentiment["compound"]
    
    if abs(compound)>0.75:
        score+=5
        
    #keeping score in 0-100 range
    score=min(score,100)
    return score

####INTERPPRET ANALYZER####

def interpret_score(score):
    if score<20:
        return "low"
    elif score<40:
        return "moderate"
    elif score<60:
        return "elevated"
    elif score<80:
        return "high"
    else:
        return "very high"
    
####MAIN ANALYZER####

def analyze_text(text):
    if not text or not text.strip():
        return{
            "Error":"please enter some text to analyze"
        }
    
    #basic processing 
    words=tokenize(text)
    
    ##wordcategories##
    emotional_words= find_category_words(words, EMOTIONAL_WORDS)
    sensational_words=find_category_words(words, SENSATIONAL_WORDS)
    absolute_words=find_category_words(words, ABSOLUTE_WORDS)
    loaded_words=find_category_words(words, LOADED_WORDS)
    urgency_words=find_category_words(words, URGENCY_WORDS)
    
    ##OTHER SIGNALS
    capitalized_words= find_capatilized_words(text)
    punction= punctuation_signal(text)
    manipulative_phrases=find_manupilative_phrases(text)
    
    ##sentiment##
    sentiment=analyze_sentiment(text)
    
    ##emotions##
    emotions=analyse_emotions(text)
    
    ##BIAS SCORES
    
    bias_score  = calculate_bias_score(
    emotional_words,
    sensational_words,
    absolute_words,
    loaded_words,
    urgency_words,
    manipulative_phrases,
    capitalized_words,
    punction,
    sentiment
    )  
    
    ##FINAL RESULT
    
    return{
        "bias_score":bias_score,
        "bias_level":interpret_score(bias_score),
        "word_count":len(words),
        "emotional_words":emotional_words,
        "sensational_words": sensational_words,
        "absolute_words":absolute_words,
        "loaded_words":loaded_words,
        "urgency_words":urgency_words,
        "manipulative_words":manipulative_phrases,
        "capitalized_words":capitalized_words,
        "punctuation":punction,
        "Sentiment":sentiment,
        "emotions":emotions
    }   
        
### TESTING ###

if __name__== "__main__":
    test_text="""
    This SHOCKING decision will DESTROY our country!
    The government has ALWAYS ignored ordinary people.
    """
    
    result=analyze_text(test_text)
    for key, value in result.items():
        print(f"\n{key}:")
        print((value))
        