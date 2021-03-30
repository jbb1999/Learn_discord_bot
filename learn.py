import discord
from discord.ext import commands
import random
import config
import mysql.connector

NULL = "temp"

bot = commands.Bot(command_prefix = config.prefix)

mydb = mysql.connector.connect( #specifiys info on how to connect to the server
  host="localhost",
  user="root",
  password="",
  database = "learn"
)

mycursor = mydb.cursor()
mycursor2 = mydb.cursor()



#this prints Bot online into the console when the bot has started succesfully
@bot.event
async def on_ready():
    print('Bot online')

@bot.event
async def on_member_join(member):
    mycursor.execute("INSERT INTO users (ID, username, score) VALUES (%s, %s, %d)", (NULL, str(member),0))
    mydb.commit()


# learn
@bot.command()
async def learn(ctx):
    trueFalseQuestions = {
        "1": ["To make a animal thats extinc be alive its called resurrection biology [true/false].", "true"],
        "2": ["Germ cells can not be edited directly [true/false].", "false"],
        "3": ["Could dangers come from de extinction [true/false].", "true"],
        "4": ["Could dinasours be revived [true/false].", "false"],
        "5": ["De extinction has been around for hundreds of years [true/false].", "false"],
        "6": ["De extinction might help us to revive some extinct species that human has wipe out  [true/false].", "true"],
    }
    userID = ctx.message.author.id
    num = random.randint(1, 6)
    userDiscrim = str(ctx.author)
    response = 1
    print(userDiscrim + " has triggered the !learn command")
    await ctx.author.send(file=discord.File(r'C:\Users\****\OneDrive\Projects\bots\Disocrd\learn\info\num' + str(num) + '.txt'))
    sentQuestion = await ctx.author.send(trueFalseQuestions[str(num)][0])
    print(type(response))

    def check(msg):
        return msg.content.lower() in ["true", "false"] and msg.channel == sentQuestion.channel

    response = await bot.wait_for('message', check=check)
    print(response == trueFalseQuestions[str(num)][1])

    if response.content == trueFalseQuestions[str(num)][1]:
        print(userDiscrim + " has answered correct")
        mycursor2.execute(f"UPDATE users set score=score+1 where username='%s'" % (str(userDiscrim)))
        mydb.commit()


bot.run(config.token)
