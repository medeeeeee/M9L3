import discord
import requests
import pyttsx3
from deep_translator import GoogleTranslator
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

def hablar(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate',150) 
    engine.setProperty('volume',1.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(texto)
    engine.runAndWait()

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

def translate_to_spanish(text):
    return GoogleTranslator(source='auto', target='es').translate(text)

def obtener_clima(ciudad):
    base_url= f"https://wttr.in/{ciudad}?format=%C+%t"
    response = requests.get(base_url)
    if response.status_code == 200:
        clima_info = response.text.strip()
        clima_info = translate_to_spanish(clima_info)
        return clima_info
    else:
        return "error"

def obtener_dato():
    base_url= f"https://uselessfacts.jsph.pl/random.json?language=en"
    response = requests.get(base_url)
    if response.status_code == 200:
        data= response.json()
        data['text'] = translate_to_spanish(data.get('text', 'No se encontró el dato.'))
        return data.get('text', 'No se encontró el dato.')
    else:
        return "error"
    
@bot.command()
async def dato(ctx):
    info= obtener_dato()
    await ctx.send(f"Dato curioso: {info}")
    hablar(f"Dato curioso: {info}")


@bot.command()
async def clima(ctx, *, ciudad):
    info= obtener_clima(ciudad)
    await ctx.send(f"El clima en {ciudad} es: {info}")
    hablar(f"El clima en {ciudad} es: {info}")



bot.run('token')
