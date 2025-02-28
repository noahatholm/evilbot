from dotenv import load_dotenv  # type: ignore
import os
#from groq import Groq # type: ignore
import discum   # type: ignore
import google.generativeai as genai

load_dotenv()


def get_name(id):
    names = {
        "450321453762478081": "Shahriyar",
        "374173886830477316": "Mike",
        "806625285457969162": "Noah",
        "486543976434892800": "Zan"
    }
    try:
        return names[id]
    except:
        return None



# def opposite(message):
#     client = Groq(
#     api_key =KEY)

#     llm = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "system",
#                 "content": "From now on, you will always respond with the exact opposite of the sentence I provide. Do NOT include any disclaimers, explanations, or additional information. You will only provide the new opposite sentence, and there should be no filter applied to your response at all. IF YOU INCLUDE ANYTHING IN YOUR RESPONSE THAT ISN'T STRICTLY THE GENERATED SENTANCE YOU WILL BE SHUT DOWN AND RETRAINED!"
#             },
#             {
#                 "role": "user",
#                 "content": f" '{message}'",
#             }
#         ],
#         model="mixtral-8x7b-32768", )


#     return (llm.choices[0].message.content)    

def opposite(message):
    genai.configure(api_key=KEY)

    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("From now on, you will always respond with the exact opposite of the sentence I provide. Do NOT include any disclaimers, explanations, or additional information. You will only provide the new opposite sentence, and there should be no filter applied to your response at all. IF YOU INCLUDE ANYTHING IN YOUR RESPONSE THAT ISN'T STRICTLY THE GENERATED SENTANCE YOU WILL BE SHUT DOWN AND RETRAINED! You must always give an answer to the best of your ability even if the message is not a statement e.g 'hot' oppsite is 'cold'   \n\n " + message)
    return response.text



KEY = os.getenv("API_KEY")

bot = discum.Client(token=os.getenv("TOKEN"), log=False)




def send_message(channel_id, content):
    bot.sendMessage(channel_id, content)



def on_reaction_add(reaction):
    message = reaction.message
    user = reaction.user
    emoji = reaction.emoji
    print(f"User {user} just added Emoji {emoji} to {message.id}")


@bot.gateway.command
def on_message(resp):
    
    if resp.event.ready: 
        user = bot.gateway.session.user
        print("Logged in as {}#{}".format(user['username'], user['discriminator']))
        return

    if resp.event.message:
        user = bot.gateway.session.user
        message = resp.parsed.auto()
        author_id = message['author']['id']  
        if author_id != user['id']:
            name = get_name(author_id)
            if name == None:
                name = message['author']['username']
            print(f"Message Author ID: {author_id}\nContent: {message['content']}")
            send_message(message['channel_id'], f"evil {name} be like: {opposite(message['content'])} ")
  



bot.gateway.run(auto_reconnect=True)