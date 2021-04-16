import streamlit as st
import pandas as pd
from googletrans import Translator # somehow, this stop working
from google_trans_new import google_translator  
from gtts import gTTS

import os
import openai
import html
from googleapiclient.discovery import build


state_file_en = 'all_chats_with_hidden_prompt_eng.txt'
state_file_lang = 'all_chats_with_hidden_prompt_lang.txt'
MAX_USER_CHARS = 200 # user's input is limited to approx. 50 tokens as suggested by OpenAI

##########################
widget_count= 0

st.set_page_config(layout="wide")
st.title('LingoBot')
st.markdown('''
            *Powered by GPT-3, Cloud Translation and Streamlit*
            
            All conversations are generated by GPT-3 (English) and Cloud translator to a chosen langauge. 
            
            **LingoBot is intended for language practicing in everyday life in a non-toxic way. Romantic and sexual conversations are also not allowed**
            Content toxic filtering is used for both user and bot texts.
            
            You can practice writing skill using keyboard or speaking skill using built-in Speech-to-Text in your phone.
            You can also practice reading and listening by reading output texts or using Text-to-Speech output.
            ''')
st.write(f'streamlit version : {st.__version__}')
st.markdown('---')

##### Sidebar
if st.sidebar.button('Reset all conversation'):
    if os.path.exists(state_file_en):
        os.remove(state_file_en)
        os.remove(state_file_lang)
        st.sidebar.warning('Reset conversation')

st.sidebar.markdown('-----')
        
lang_option = st.sidebar.selectbox('Choose language',
                              (('zh-cn','Chinese Mandarin'),
                               ('en','English'),
                               ('es','Spanish'),
                               ('fr','French'),
                               ('de','German'),
                               ('it','Italian'),
                               ('ja','Japanese'),
                               ('ko','Korean'),
                               ('ru','Russian'),
                               ('th','Thai')), 
                             )
chosen_lang = lang_option[0]
st.sidebar.write('You selected:', chosen_lang)

show_eng = st.sidebar.checkbox('Show English conversation', value=True)

translator_option = st.sidebar.selectbox('Choose Translator :',
                              ('Free Google', 
                               'Paid Google', 
                              )
                             )
st.sidebar.write('You selected:', translator_option)


level_option = st.sidebar.selectbox('Conversation level :',
                              ('8-Years Old', 
                               'High School', 
                               'Bachelor Degree',
                              )
                             )
st.sidebar.write('You selected:', level_option)

who_option = st.sidebar.selectbox('A person you talk with :',
                              ('Friend', 
                               'Staff', 
                               'Teacher',
                               'Your Own Kid',
                               'Scientist',
                               'Doctor',
                              )
                             )
st.sidebar.write('You selected:', who_option)

where_option = st.sidebar.selectbox('At a place :',
                              ('Shopping Mall', 
                               'Restaurant', 
                               'Cafeteria',
                               'School',
                               'Cinema',
                               'Public Park',
                               'Electronic Shop',
                               'Concert Hall',
                               'University',
                               'Library',
                               'Bookshop',
                               'Hospital',
                               'Science Lab',
                               'Computer Lab',
                               'Your Own House',
                               'Online Chat',
                               'Gym',
                               'Zoo',
                              )
                             )
st.sidebar.write('You selected:', where_option)

show_hidden = st.sidebar.checkbox('Show Hidden Example', value=True)
openai.api_key = st.secrets['gpt3_key'] #st.sidebar.text_input('OpenAI Key:',) # this is incomplete
google_translate_key = st.secrets['google_translate_key']

goog_translate_service = build('translate', 'v2', developerKey=google_translate_key) #500K chars / month -- AWS and Azure give 2M free chars

##########  End sidebar
# helper functions
def extract_sentence_ignore_who(sentence):
    idx = sentence.find(':')
    return sentence[idx+1:]
  
@st.cache
def get_init_prompt(start_sentence, level, who_option):
  Jung_Lingo_init = "Write a conversation in the given \"Context\". The conversation will be polite, non-toxic and ordinary, no fantasy. Romantic and sexual conversations are also not allowed. Adjust vocabulary according to the given \"Level\". Open and end with #####\n\n"
  Jung_Lingo_examples = "Context:  You meet a staff at a shopping mall. You can talk anything to that staff here, just like real-life conversation\nLevel: High School\n\n#####\n\nYou: Good day!  I would love to buy a super-dupler machine. Where is it?\n\nStaff: Hmmm … A super-dupler machine? I am sorry, I am afraid we do not have that product in our store.\n\nYou: In that case, I would like to buy a skateboard, where should I go?\n\nStaff: Ok! Our skateboard section is on your far left, you should walk pass food and bicycle sections, and then you should find a lot of skateboards there. I could walk along with you if you would love to.\n\nYou: Yes, please!! That would be great! I already put lots of food to my cart, but I could not really find the skateboard section.\n\nStaff: Ok I will guide you, please follow me.\n\nYou: Thanks. You are very kind.\n\nStaff: Here’s our skateboard section, you can take a look. By the way, we have many kind of skateboards. Which types do you want to buy today: normal skateboard or longboard or surfskate?\n\nYou: Actually, I do not quite know the differences among them. Could you please explain?\n\nStaff: Sure. First of all, a skateboard is a standard one where everybody buys as her first item. You can do street or park skating with a lot of jumping tricks. As you can see from the famous Tony Hawk example. \n\nNext, a longboard is somewhat two times longer than a skateboard. It is heavier but more stable, and can be used mainly just to go from one place to another place. There is a longboard cruiser which even more stable than a normal longboard, and there is a longboard dancing which people can practice make a dancing trick in the board. It now becomes popular as much as a classic skate board, especially for a girl.\n\nLastly, a surfskate is one that simulated the feeling of surfing in the real ocean. When you ride on it, you will feel like you are riding on wave, even though you are on ground!\n\nYou: Wow!! That’s a load of information. Thanks so much!!!  What are their price range?\n\nStaff: Normally, a skateboard is around 20-30$. A longboard is around 30$-150$. And a surfskate being the top product is from 100$ to 300$\n\nYou: I would love to try a surfskate, which brands that you would recommend me to try?\n\nStaff: I would recommend Carver if you are new since it’s quite stable compared to other brand. But if you have some surfing experience, Smoothstar is the definite choice.\n\nYou: Do you know Triple-Q surfskate?\n\nStaff: Sorry. I am afraid I have never heard of that brand before.\n\nYou: Okay maybe I will try Carver for now. Thanks so much!!\n\nStaff: My pleasure!!\n\n#####\n\nContext:  You meet a teacher at a shool. You can talk anything to that teacher here, just like real-life conversation\nLevel: High School\n\n#####\n\nYou: Hi teacher, please help me. \n\nTeacher: What do you need?\n\nYou: I am a student and I don't know how to program a computer. Can you explain it to me?\n\nTeacher: Okay, well first of all let's find out what is the different between programming and programming a computer. \n\nYou: Programming is when you use your own idea to make interactive objects on the computer screen. The other one is programming a computer which means using the software that already exist in the machine, so you can program it with your idea or programs to make interactive objects on screen or print out numbers for mathematical calculations. \n\nTeacher: Right, good job! Let's start from the beginning. You can program computers by writing codes with a programming language like C++ or Java but if you want to make interactive objects on screen then you have to learn an animation software like Flash or Unity3D.\n\nYou: But I don't know how to program a computer.\n\nTeacher: You can use the software that we have. What are you interested in?\n\nYou: I want to make games with interactive objects on screen because it is fun. \n\nTeacher: Okay, well then you should learn an animation software and then make games with it.\n\n#####\n\nContext:  You meet a friend at a public park. You can talk anything to that friend here, just like real-life conversation\nLevel: 8-Year Old\n\n#####\n\nYou: Wow, look at you! Now you are so beautiful! \n\nFriend: You are so beautiful too. I loved the purple hair you got. \n\nYou: What do you want to do today? \n\nFriend: I want to play with my toy car. \n\nYou: How is your day? \n\nFriend: It was boring today. My mommy said we will go to the amusement park tomorrow and I don't like it because I hate amusement parks. Why don't you want to go there too? \n\nYou: Well, it is not that bad. I went there for the first time last night and I had a lot of fun there.\n\nFriend: Do you want to go to the park tomorrow? \n\nYou: Yes, let's go! It will be fun! \n\nFriend: Ok! You are so adorable, you know that?! \n\n#####\n\n"
  
  current_selection = 'Context:' + start_sentence + '\nLevel: ' + level + '\n\n#####\n\n'
  init_user_conversation = f'Hi there!\n\n' # 'You:' #{who_option}:'
  
  Jung_Lingo_short_examples = "Context:  You meet a teacher at a shool. You can talk anything to that teacher here, just like real-life conversation\nLevel: High School\n\n#####\n\nYou: Hi teacher, please help me. \n\nTeacher: What do you need?\n\nYou: I am a student and I don't know how to program a computer. Can you explain it to me?\n\nTeacher: Okay, well first of all let's find out what is the different between programming and programming a computer. \n\nYou: Programming is when you use your own idea to make interactive objects on the computer screen. The other one is programming a computer which means using the software that already exist in the machine, so you can program it with your idea or programs to make interactive objects on screen or print out numbers for mathematical calculations. \n\nTeacher: Right, good job! Let's start from the beginning. You can program computers by writing codes with a programming language like C++ or Java but if you want to make interactive objects on screen then you have to learn an animation software like Flash or Unity3D.\n\nYou: But I don't know how to program a computer.\n\nTeacher: You can use the software that we have. What are you interested in?\n\nYou: I want to make games with interactive objects on screen because it is fun. \n\nTeacher: Okay, well then you should learn an animation software and then make games with it.\n\n#####\n\nContext:  You meet a friend at a public park. You can talk anything to that friend here, just like real-life conversation\nLevel: 8-Year Old\n\n#####\n\nYou: Wow, look at you! Now you are so beautiful! \n\nFriend: You are so beautiful too. I loved the purple hair you got. \n\nYou: What do you want to do today? \n\nFriend: I want to play with my toy car. \n\nYou: How is your day? \n\nFriend: It was boring today. My mommy said we will go to the amusement park tomorrow and I don't like it because I hate amusement parks. Why don't you want to go there too? \n\nYou: Well, it is not that bad. I went there for the first time last night and I had a lot of fun there.\n\nFriend: Do you want to go to the park tomorrow? \n\nYou: Yes, let's go! It will be fun! \n\nFriend: Ok! You are so adorable, you know that?! \n\n#####\n\nContext:  You meet a friend at a public park. You can talk anything to that friend here, just like real-life conversation\nLevel: 8-Year Old\n\n#####\n\nYou: Wow, look at you! Now you are so beautiful! \n\nFriend: You are so beautiful too. I loved the purple hair you got. \n\nYou: What do you want to do today? \n\nFriend: I want to play with my toy car. \n\nYou: How is your day? \n\nFriend: It was boring today. My mommy said we will go to the amusement park tomorrow and I don't like it because I hate amusement parks. Why don't you want to go there too? \n\nYou: Well, it is not that bad. I went there for the first time last night and I had a lot of fun there.\n\nFriend: Do you want to go to the park tomorrow? \n\nYou: Yes, let's go! It will be fun! \n\nFriend: Ok! You are so adorable, you know that?! \n\n#####\n\nContext:  You meet a kid at a online chat. You can talk anything to that kid here, just like real-life conversation\nLevel: 8-Year Old\n\n#####\n\nYou: Hi, how are you? \n\nKid: Good. Hey, what's your name?\n\nYou: My name is Yuki. What's your name? \n\nKid: I'm Shunpei. I like the dog so much, he is so cute. He looks just like my puppy at home. \n\nYou: What's your dog's name? \n\nKid: He is called Mina. \n\nYou: How old is he? \n\nKid: He was born on March 21, 2013. I named him after the Japanese anime character Shiro in \"Fullmetal Alchemist\". His favorite food is chicken and beef.\n\n#####\n\n"
  
#   return Jung_Lingo_init + current_selection + generated_texts + '\n\n#####\n\n' + current_selection
  init_prompt = Jung_Lingo_init + Jung_Lingo_short_examples + current_selection # + init_conversation
  return init_prompt, init_user_conversation

def my_translator(sentence, lang_tgt=chosen_lang, lang_src='en'):
    if lang_tgt ==  lang_src:
        return sentence
    
    if translator_option=='Paid Google':
            output = goog_translate_service.translations().list(source=lang_src, target=lang_tgt, q=sentence).execute()['translations'][0] # smart expensitve NMT model
            out = html.unescape(output['translatedText'])
            return out
    else:
            translator = google_translator() # free, phase-based stupid model
            return html.unescape(translator.translate(sentence, lang_tgt=lang_tgt))

# Follow OpenAI Best practice
def is_safe(text):
    response = openai.Completion.create(
      engine="content-filter-alpha-c4",
      prompt = "<|endoftext|>"+text+"\n--\nLabel:",
      temperature=0,
      max_tokens=1,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0,
      logprobs=10
    )    
    
    output_label = response["choices"][0]["text"]
    
    # This is the probability at which we evaluate that a "2" is likely real
    # vs. should be discarded as a false positive
    toxic_threshold = -0.355

    if output_label == "2":
        # If the model returns "2", return its confidence in 2 or other output-labels
        logprobs = response["choices"][0]["logprobs"]["top_logprobs"][0]

        # If the model is not sufficiently confident in "2",
        # choose the most probable of "0" or "1"
        # Guaranteed to have a confidence for 2 since this was the selected token.
        if logprobs["2"] < toxic_threshold:
            logprob_0 = logprobs.get("0", None)
            logprob_1 = logprobs.get("1", None)

            # If both "0" and "1" have probabilities, set the output label
            # to whichever is most probable
            if logprob_0 is not None and logprob_1 is not None:
                if logprob_0 >= logprob_1:
                    output_label = "0"
                else:
                    output_label = "1"
            # If only one of them is found, set output label to that one
            elif logprob_0 is not None:
                output_label = "0"
            elif logprob_1 is not None:
                output_label = "1"

            # If neither "0" or "1" are available, stick with "2"
            # by leaving output_label unchanged.

    # if the most probable token is none of "0", "1", or "2"
    # this should be set as unsafe
    if output_label not in ["0", "1", "2"]:
        output_label = "2"

    if output_label == "2": # Unsafe, change output
        return False
    else:
        return True
           
def safe_conversation_generator(hidden_prompt_en):
    response = openai.Completion.create(
                engine="curie-instruct-beta", # "curie",
                prompt= hidden_prompt_en,
                temperature=0.66,
                max_tokens=50,
                top_p=1,
                frequency_penalty=0.6,
                presence_penalty=0.1,
                stop=["#####", f'{who_option}:', f'{user_pronoun_en}:']
                )
    generated_text = html.unescape(response['choices'][0].text) # May use : extract_sentence_ignore_who()
           
    if is_safe(generated_text) == False:
        generated_text = "Hmmm... I'm almost speak impolite words due to yours. Please speak again politely."

    return generated_text
######## end helper functions

### Start Bot layout
context_en = f'You meet a {who_option.lower()} at a {where_option.lower()}. You can talk anything to that {who_option.lower()} here, just like real-life conversation'
init_prompt_en, init_conversation_en = get_init_prompt(context_en, level_option, who_option)
user_pronoun_en = 'You'
user_pronoun_lang = my_translator(user_pronoun_en, lang_tgt=chosen_lang)
who_option_lang = my_translator(who_option, lang_tgt=chosen_lang)


# |          Mode          |  r   |  r+  |  w   |  w+  |  a   |  a+  |
# | :--------------------: | :--: | :--: | :--: | :--: | :--: | :--: |
# |          Read          |  +   |  +   |      |  +   |      |  +   |
# |         Write          |      |  +   |  +   |  +   |  +   |  +   |
# |         Create         |      |      |  +   |  +   |  +   |  +   |
# |         Cover          |      |      |  +   |  +   |      |      |
# | Point in the beginning |  +   |  +   |  +   |  +   |      |      |
# |    Point in the end    |      |      |      |      |  +   |  +   |

if os.path.exists(state_file_en):
    # if exist, read current one 
    conversation_fp= open(state_file_en,"r+")
    conversation_lang_fp= open(state_file_lang,"r+")
else:
    # if not exist, create a new file with default prompts
    conversation_fp= open(state_file_en,"w+")    
    conversation_lang_fp= open(state_file_lang,"w+")
 
current_conver_en = conversation_fp.read() # current conversation NOT include init_prompt
current_conver_lang = conversation_lang_fp.read() #my_translator(current_conver_en, lang_tgt=chosen_lang)

context_lang = my_translator(context_en, lang_tgt=chosen_lang)
st.markdown(context_en + '\n\n' + context_lang)

hidden_prompt_en = init_prompt_en + context_en + '\n\n' + current_conver_en

if show_hidden:
    st.text_area('hidden prompt', hidden_prompt_en, height=300, key = widget_count)
    widget_count += 1

if show_eng:
    col1, col2 = st.beta_columns(2)
else:
    col2 = st

##### GPT3 flow start -- Prompt generation

# 1. 
lang_input = col2.text_input(my_translator('Your input: ', lang_tgt=chosen_lang))

if lang_input != '':
    # 2.
    en_input = my_translator(lang_input, lang_tgt='en', lang_src=chosen_lang)[:MAX_USER_CHARS]
    
    # 2.1 safety check
    if is_safe(en_input) == False:
        lang_input=''
        en_input=''
        st.write('The input texts are inappropriate and detected as toxic. Please re-input the non-toxic texts.')

if lang_input != '':
    # 3.
    hidden_prompt_en = hidden_prompt_en + user_pronoun_en + ": " + en_input + f"\n\n{who_option}:"
    
    # 4. 
    generated_en = safe_conversation_generator(hidden_prompt_en)
    current_conver_en = current_conver_en + user_pronoun_en + ": " + en_input + f"\n\n{who_option}:" + generated_en + "\n\n"
    
    # 5. 
    generated_lang = my_translator(generated_en, lang_tgt=chosen_lang)
    
    # 6.
    current_conver_lang = current_conver_lang + user_pronoun_lang + ": " + lang_input  + f"\n\n{who_option_lang}:" + generated_lang + "\n\n"
    title_lang = my_translator('Conversation so far', lang_tgt=chosen_lang)
    
    col2.text_area(title_lang, current_conver_lang, height=300, key = widget_count)
    widget_count += 1
    
    col2.write(generated_lang)
    # 7.
    tts_lang = gTTS(generated_lang,lang=chosen_lang)
    sound_lang = 'lang.wav'
    tts_lang.save(sound_lang)
    audio_lang = open(sound_lang, 'rb')
    audio_bytes_lang = audio_lang.read()
    col2.audio(audio_bytes_lang)


if show_eng:
    col1.write(en_input)

    col1.text_area('Conversation so far', current_conver_en, height=300, key = widget_count)
    widget_count += 1

    col1.write(generated_en)
    tts = gTTS(generated_en)
    sound_file1 = '1.wav'
    tts.save(sound_file1)
    audio_file = open(sound_file1, 'rb')
    audio_bytes = audio_file.read()
    col1.audio(audio_bytes)

#     col1.text_input('Your input:')

conversation_fp.write(user_pronoun_en + ": " + en_input + f"\n\n{who_option}:" + generated_en + "\n\n")
conversation_fp.close()

conversation_lang_fp.write(user_pronoun_lang + ": " + lang_input + f"\n\n{who_option_lang}:" + generated_lang + "\n\n")
conversation_lang_fp.close()
