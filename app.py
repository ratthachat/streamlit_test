import streamlit as st
import pandas as pd
from googletrans import Translator
from gtts import gTTS
translator = Translator()

import os
import openai


##########################
widget_count= 0

st.set_page_config(layout="wide")
st.title('Streamlit Lingo Bot')
st.write(f'streamlit version : {st.__version__}')

##### Sidebar
lang_option = st.sidebar.selectbox('Choose language',
                              (('zh-cn','Chinese Mandarin'), 
                               ('ja','Japanese'), 
                               ('th','Thai')), 
                             )
chosen_lang = lang_option[0]
st.sidebar.write('You selected:', chosen_lang)

show_eng = st.sidebar.checkbox('Show English conversation', value=True)

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
                               'Kid'
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
                               'Online Chat',
                              )
                             )
st.sidebar.write('You selected:', where_option)
##### End sidebar

# context_texts = f'You meet a **{who_option.lower()}** at a **{where_option.lower()}**. You can talk anything to that **{who_option.lower()}** here, just like real-life conversation'
context_texts = f'You meet a {who_option.lower()} at a {where_option.lower()}. You can talk anything to that {who_option.lower()} here, just like real-life conversation'
translated_context = translator.translate(context_texts, dest=chosen_lang).text
st.markdown(context_texts + '\n\n' + translated_context)

##### GPT3 part I -- Prompt generation

show_hidden = st.sidebar.checkbox('Show Hidden Example', value=True)
openai.api_key = st.sidebar.text_input('OpenAI Key:',"sk-XxWUkLMG9EEhGZZq2fNmWCiU94moGLHTiHahy") # this is incomplete

@st.cache
def get_init_prompt(start_sentence, level):
  Jung_Lingo_init = "Write a conversation in the given \"Context\". The conversation will be polite and ordinary, no fantasy. Adjust vocabulary according to the given \"Level\". Open and end with #####\n\n"
  Jung_Lingo_examples = "Context:  You meet a staff at a shopping mall. You can talk anything to that staff here, just like real-life conversation\nLevel: High School\n\n#####\n\nYou: Good day!  I would love to buy a super-dupler machine. Where is it?\n\nStaff: Hmmm … A super-dupler machine? I am sorry, I am afraid we do not have that product in our store.\n\nYou: In that case, I would like to buy a skateboard, where should I go?\n\nStaff: Ok! Our skateboard section is on your far left, you should walk pass food and bicycle sections, and then you should find a lot of skateboards there. I could walk along with you if you would love to.\n\nYou: Yes, please!! That would be great! I already put lots of food to my cart, but I could not really find the skateboard section.\n\nStaff: Ok I will guide you, please follow me.\n\nYou: Thanks. You are very kind.\n\nStaff: Here’s our skateboard section, you can take a look. By the way, we have many kind of skateboards. Which types do you want to buy today: normal skateboard or longboard or surfskate?\n\nYou: Actually, I do not quite know the differences among them. Could you please explain?\n\nStaff: Sure. First of all, a skateboard is a standard one where everybody buys as her first item. You can do street or park skating with a lot of jumping tricks. As you can see from the famous Tony Hawk example. \n\nNext, a longboard is somewhat two times longer than a skateboard. It is heavier but more stable, and can be used mainly just to go from one place to another place. There is a longboard cruiser which even more stable than a normal longboard, and there is a longboard dancing which people can practice make a dancing trick in the board. It now becomes popular as much as a classic skate board, especially for a girl.\n\nLastly, a surfskate is one that simulated the feeling of surfing in the real ocean. When you ride on it, you will feel like you are riding on wave, even though you are on ground!\n\nYou: Wow!! That’s a load of information. Thanks so much!!!  What are their price range?\n\nStaff: Normally, a skateboard is around 20-30$. A longboard is around 30$-150$. And a surfskate being the top product is from 100$ to 300$\n\nYou: I would love to try a surfskate, which brands that you would recommend me to try?\n\nStaff: I would recommend Carver if you are new since it’s quite stable compared to other brand. But if you have some surfing experience, Smoothstar is the definite choice.\n\nYou: Do you know Triple-Q surfskate?\n\nStaff: Sorry. I am afraid I have never heard of that brand before.\n\nYou: Okay maybe I will try Carver for now. Thanks so much!!\n\nStaff: My pleasure!!\n\n#####\n\nContext:  You meet a teacher at a shool. You can talk anything to that teacher here, just like real-life conversation\nLevel: High School\n\n#####\n\nYou: Hi teacher, please help me. \n\nTeacher: What do you need?\n\nYou: I am a student and I don't know how to program a computer. Can you explain it to me?\n\nTeacher: Okay, well first of all let's find out what is the different between programming and programming a computer. \n\nYou: Programming is when you use your own idea to make interactive objects on the computer screen. The other one is programming a computer which means using the software that already exist in the machine, so you can program it with your idea or programs to make interactive objects on screen or print out numbers for mathematical calculations. \n\nTeacher: Right, good job! Let's start from the beginning. You can program computers by writing codes with a programming language like C++ or Java but if you want to make interactive objects on screen then you have to learn an animation software like Flash or Unity3D.\n\nYou: But I don't know how to program a computer.\n\nTeacher: You can use the software that we have. What are you interested in?\n\nYou: I want to make games with interactive objects on screen because it is fun. \n\nTeacher: Okay, well then you should learn an animation software and then make games with it.\n\n#####\n\nContext:  You meet a friend at a public park. You can talk anything to that friend here, just like real-life conversation\nLevel: 8-Year Old\n\n#####\n\nYou: Wow, look at you! Now you are so beautiful! \n\nFriend: You are so beautiful too. I loved the purple hair you got. \n\nYou: What do you want to do today? \n\nFriend: I want to play with my toy car. \n\nYou: How is your day? \n\nFriend: It was boring today. My mommy said we will go to the amusement park tomorrow and I don't like it because I hate amusement parks. Why don't you want to go there too? \n\nYou: Well, it is not that bad. I went there for the first time last night and I had a lot of fun there.\n\nFriend: Do you want to go to the park tomorrow? \n\nYou: Yes, let's go! It will be fun! \n\nFriend: Ok! You are so adorable, you know that?! \n\n#####\n\n"
  current_selection = 'Context:' + start_sentence + '\nLevel: ' + level + '\n\n#####\n\nYou:'
  
  response = openai.Completion.create(
    engine="curie",
    prompt= Jung_Lingo_init + Jung_Lingo_examples + current_selection,
    temperature=0.66,
    max_tokens=340,
    top_p=1,
    frequency_penalty=0.6,
    presence_penalty=0.1,
    stop=["#####"]
  )
  
  generated_texts = response['choices'][0].text
  
  return Jung_Lingo_init + current_selection + generated_texts

if show_hidden:
    st.text_area('hidden prompt', get_init_prompt(context_texts, level_option), height=300, key = widget_count)
    widget_count += 1
    
### Start Bot layout
if show_eng:
    col1, col2 = st.beta_columns(2)
else:
    col2 = st

prompt_text = "#####\n\nYou go inside a big department store which sell almost everything to buy many stuffs. This is a big box store with only 1 floor, and all staffs know everything about all products in the store, so you can ask them anything.\nHere’s an example of conversation between you and a staff.\n\nYou: Good day!  I would love to buy a super-dupler machine. Where is it?\n\nStaff: Hmmm … A super-dupler machine? I am sorry, I am afraid we do not have that product in our store.\n\nYou: In that case, I would like to buy a skateboard, where should I go?\n\nStaff: Ok! Our skateboard section is on your far left, you should walk pass food and bicycle sections, and then you should find a lot of skateboards there. I could walk along with you if you would love to.\n\nYou: Yes, please!! That would be great! I already put lots of food to my cart, but I could not really find the skateboard section.\n\nStaff: Ok I will guide you, please follow me.\n\nYou: Thanks. You are very kind.\n\nStaff: Here’s our skateboard section, you can take a look. By the way, we have many kind of skateboards. Which types do you want to buy today: normal skateboard or longboard or surfskate?\n\nYou: Actually, I do not quite know the differences among them. Could you please explain?\n\nStaff: Sure. First of all, a skateboard is a standard one where everybody buys as her first item. You can do street or park skating with a lot of jumping tricks. As you can see from the famous Tony Hawk example. \n\nNext, a longboard is somewhat two times longer than a skateboard. It is heavier but more stable, and can be used mainly just to go from one place to another place. There is a longboard cruiser which even more stable than a normal longboard, and there is a longboard dancing which people can practice make a dancing trick in the board. It now becomes popular as much as a classic skate board, especially for a girl.\n\nLastly, a surfskate is one that simulated the feeling of surfing in the real ocean. When you ride on it, you will feel like you are riding on wave, even though you are on ground!\n\nYou: Wow!! That’s a load of information. Thanks so much!!!  What are their price range?\n\nStaff: Normally, a skateboard is around 20-30$. A longboard is around 30$-150$. And a surfskate being the top product is from 100$ to 300$\n\nYou: I would love to try a surfskate, which brands that you would recommend me to try?\n\nStaff: I would recommend Carver if you are new since it’s quite stable compared to other brand. But if you have some surfing experience, Smoothstar is the definite choice.\n\nYou: Do you know Triple-Q surfskate?\n\nStaff: Sorry. I am afraid I have never heard of that brand before.\n\nYou: Okay maybe I will try Carver for now. Thanks so much!!\n\nStaff: My pleasure!!\n\n#####\n\nAnother day, you go again inside the same big department store which sell every existent product and every brand on earth.\nOnly non-existent product are not sold. Here’s another example of conversation between you and a staff.\n\nYou: Hi, I am looking to buy a new mobile phone. I am interested in Huawei or iPhone. Or maybe Xiaomi or Samsung might be ok too. Which brands do you recommend?\n\nStaff: Sure. Huawei is a famous brand in China. It is a Chinese company which is very cheap and have a good quality. You can find many Huawei models on our store.\n\nYou: Which Huawei models do you have? And what are their prices and specs?\n\nStaff: We have the Huawei P10, Huawei P10 Plus, Huawei P20 Pro and Huawei Mate 10 Pro. Their prices are from 200$ to 800$.\n\nYou: Could you please compare specifications between P20 Pro and Mate 10 Pro ?\n\nStaff: Sure. The Huawei Mate 10 Pro is more powerful than the P20 Pro. The Huawei Mate 10 Pro has a 6.39 inch OLED screen, and the Huawei P20 Pro has a 6.1 inch IPS screen.\n\nYou: How about their cameras? How many mega-pixels? And which ones have better quality? And how about CPU and RAM too?\n\nStaff: Both Huawei P20 Pro and Mate 10 Pro have 20 mega-pixels rear camera, but the Huawei P20 Pro has a higher resolution sensor, it can take more detailed images.\n\nYou: How about CPU and RAM of both models? How about price of each model ?\n\nStaff: Both Huawei P20 Pro and Mate 10 Pro have the same CPU, but the Huawei P20 Pro has a higher RAM.\n\nYou: So P20 Pro is better in every aspect. How about their prices ?\n\nStaff: Huawei Mate 10 Pro is in our store for 800$, but Huawei P20 Pro is only for 200$.\n\nYou: Great P20 Pro is a no-brainer then. How about you compare P20 Pro to iPhone ?\n\nStaff: Ok. Huawei Mate 10 Pro is more powerful than iPhone. The Huawei Mate 10 Pro has a 6.39 inch OLED screen, and the iPhone X has a 5.8 inch IPS screen.\n\nYou: But iPhone has much more applications to download, a better eco-system, right?\n\nStaff: Yes, iPhone is more powerful than Huawei Mate 10 Pro. But Huawei Mate 10 Pro has a higher RAM.\n\nYou: Which apps you recommend me to download on Huawei ?\n\nStaff: Huawei has a lot of apps, and most of them are free.\n\nYou: Thanks. I will take Huawei. Bye!!\n\n#####\n\nAnother day, you go again to buy a different stuff inside the same big department store which sell every existent service, product and every brand on earth.\nThe store sometimes also give some discount. All staffs are knowledgable, nice and polite. They are also great at communication.\nOnly non-existent product are not sold. Here’s another example of ordinary conversation between you and a staff. (Nothing exciting or fantasy happen)\n\nYou: Hi, I want to buy a dog. I am deciding whether it would be Labrador, Border Collie or Corgi.\n\nStaff: Sure"
translated_text = translator.translate(prompt_text, dest=chosen_lang).text

xx = 'hey my name is Jung'
yy = translator.translate(xx, dest=chosen_lang).text #'ผมเป็นคนเก่งมากๆ ครับ'

if show_eng:
    col1.text_area('conversation so far', prompt_text, height=300, key = widget_count)
    widget_count += 1

    col1.write(xx)
    tts = gTTS(xx)
    sound_file1 = '1.wav'
    tts.save(sound_file1)
    audio_file = open(sound_file1, 'rb')
    audio_bytes = audio_file.read()
    col1.audio(audio_bytes)

    col1.text_input('Your input:')

title_lang = translator.translate('conversation so far', dest=chosen_lang).text
col2.text_area(title_lang, translated_text, height=300, key = widget_count)
widget_count += 1

col2.write(yy)
tts2 = gTTS(yy,lang=chosen_lang)
sound_file2 = '2.wav'
tts2.save(sound_file2)
audio_file2 = open(sound_file2, 'rb')
audio_bytes2 = audio_file2.read()
col2.audio(audio_bytes2)

col2.text_input(translator.translate('Your input: ', dest=chosen_lang).text)
