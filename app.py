import streamlit as st
import pandas as pd
from googletrans import Translator
translator = Translator()

st.title('Streamlit Lingo Bot')
col1, col2 = st.beta_columns(2)

prompt_text = "#####\n\nYou go inside a big department store which sell almost everything to buy many stuffs. This is a big box store with only 1 floor, and all staffs know everything about all products in the store, so you can ask them anything.\nHere’s an example of conversation between you and a staff.\n\nYou: Good day!  I would love to buy a super-dupler machine. Where is it?\n\nStaff: Hmmm … A super-dupler machine? I am sorry, I am afraid we do not have that product in our store.\n\nYou: In that case, I would like to buy a skateboard, where should I go?\n\nStaff: Ok! Our skateboard section is on your far left, you should walk pass food and bicycle sections, and then you should find a lot of skateboards there. I could walk along with you if you would love to.\n\nYou: Yes, please!! That would be great! I already put lots of food to my cart, but I could not really find the skateboard section.\n\nStaff: Ok I will guide you, please follow me.\n\nYou: Thanks. You are very kind.\n\nStaff: Here’s our skateboard section, you can take a look. By the way, we have many kind of skateboards. Which types do you want to buy today: normal skateboard or longboard or surfskate?\n\nYou: Actually, I do not quite know the differences among them. Could you please explain?\n\nStaff: Sure. First of all, a skateboard is a standard one where everybody buys as her first item. You can do street or park skating with a lot of jumping tricks. As you can see from the famous Tony Hawk example. \n\nNext, a longboard is somewhat two times longer than a skateboard. It is heavier but more stable, and can be used mainly just to go from one place to another place. There is a longboard cruiser which even more stable than a normal longboard, and there is a longboard dancing which people can practice make a dancing trick in the board. It now becomes popular as much as a classic skate board, especially for a girl.\n\nLastly, a surfskate is one that simulated the feeling of surfing in the real ocean. When you ride on it, you will feel like you are riding on wave, even though you are on ground!\n\nYou: Wow!! That’s a load of information. Thanks so much!!!  What are their price range?\n\nStaff: Normally, a skateboard is around 20-30$. A longboard is around 30$-150$. And a surfskate being the top product is from 100$ to 300$\n\nYou: I would love to try a surfskate, which brands that you would recommend me to try?\n\nStaff: I would recommend Carver if you are new since it’s quite stable compared to other brand. But if you have some surfing experience, Smoothstar is the definite choice.\n\nYou: Do you know Triple-Q surfskate?\n\nStaff: Sorry. I am afraid I have never heard of that brand before.\n\nYou: Okay maybe I will try Carver for now. Thanks so much!!\n\nStaff: My pleasure!!\n\n#####\n\nAnother day, you go again inside the same big department store which sell every existent product and every brand on earth.\nOnly non-existent product are not sold. Here’s another example of conversation between you and a staff.\n\nYou: Hi, I am looking to buy a new mobile phone. I am interested in Huawei or iPhone. Or maybe Xiaomi or Samsung might be ok too. Which brands do you recommend?\n\nStaff: Sure. Huawei is a famous brand in China. It is a Chinese company which is very cheap and have a good quality. You can find many Huawei models on our store.\n\nYou: Which Huawei models do you have? And what are their prices and specs?\n\nStaff: We have the Huawei P10, Huawei P10 Plus, Huawei P20 Pro and Huawei Mate 10 Pro. Their prices are from 200$ to 800$.\n\nYou: Could you please compare specifications between P20 Pro and Mate 10 Pro ?\n\nStaff: Sure. The Huawei Mate 10 Pro is more powerful than the P20 Pro. The Huawei Mate 10 Pro has a 6.39 inch OLED screen, and the Huawei P20 Pro has a 6.1 inch IPS screen.\n\nYou: How about their cameras? How many mega-pixels? And which ones have better quality? And how about CPU and RAM too?\n\nStaff: Both Huawei P20 Pro and Mate 10 Pro have 20 mega-pixels rear camera, but the Huawei P20 Pro has a higher resolution sensor, it can take more detailed images.\n\nYou: How about CPU and RAM of both models? How about price of each model ?\n\nStaff: Both Huawei P20 Pro and Mate 10 Pro have the same CPU, but the Huawei P20 Pro has a higher RAM.\n\nYou: So P20 Pro is better in every aspect. How about their prices ?\n\nStaff: Huawei Mate 10 Pro is in our store for 800$, but Huawei P20 Pro is only for 200$.\n\nYou: Great P20 Pro is a no-brainer then. How about you compare P20 Pro to iPhone ?\n\nStaff: Ok. Huawei Mate 10 Pro is more powerful than iPhone. The Huawei Mate 10 Pro has a 6.39 inch OLED screen, and the iPhone X has a 5.8 inch IPS screen.\n\nYou: But iPhone has much more applications to download, a better eco-system, right?\n\nStaff: Yes, iPhone is more powerful than Huawei Mate 10 Pro. But Huawei Mate 10 Pro has a higher RAM.\n\nYou: Which apps you recommend me to download on Huawei ?\n\nStaff: Huawei has a lot of apps, and most of them are free.\n\nYou: Thanks. I will take Huawei. Bye!!\n\n#####\n\nAnother day, you go again to buy a different stuff inside the same big department store which sell every existent service, product and every brand on earth.\nThe store sometimes also give some discount. All staffs are knowledgable, nice and polite. They are also great at communication.\nOnly non-existent product are not sold. Here’s another example of ordinary conversation between you and a staff. (Nothing exciting or fantasy happen)\n\nYou: Hi, I want to buy a dog. I am deciding whether it would be Labrador, Border Collie or Corgi.\n\nStaff: Sure"
translated_text = translator.translate(prompt_text, dest='th').text

xx = 'hey'
yy = 102
col1.write(prompt_text)
col1.write(xx)
col1.text_input('your input:')

col2.write(translated_text)
col2.write(yy)
col2.text_input('ใส่ข้อความ:')

# text = col1.text_area(
#     "Your text",
#     "I dreamed a dream."
# )
# if not text:
#     text = "Emptiness"
# col1.write(text+"555")

# outputs={



# table_md = f'''
#     |Script/Language|Eng|Lang|
#     |--|--|--|
#     |Conversation|**{xx}**|{yy}|
#     |Bot Latest|{xx}|**{yy}**|
#     |You say|{xx}|{yy}|
#     '''
    
# col2.markdown(table_md)
