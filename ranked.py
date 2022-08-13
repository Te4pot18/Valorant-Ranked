from discord.ext import commands
import json, time
import discord
import asyncio
from random import *
from discord.utils import get

token = ''
bot = commands.Bot(command_prefix='.', description="Valorant")
bot.remove_command("help")
image = "PDP DU BOT POUR LES EMBEDS"
owner = ["ID1", "ID2", "ID3", "ETC..."]

class JsonDatabase:
    def __init__( self, database ): # database => (str)
        self.db = database
        pass

    def getContent( self ):
        return json.loads(open(self.db, "r").read())
        pass

    def insertContent( self, data ): # this => (json)
        with open(self.db, "w") as database:
            database.write(json.dumps(data))
            pass
        pass

    def updateUser( self, data ): # user => (str), key => (str), value => (str, bool, int)
        content = self.getContent()
        content[data['user']][data['key']] = data['value']

        self.insertContent(content)
        pass

    def userExist( self, data ): # user => (str)
        content = self.getContent()
        
        if data['user'] in content.keys():
            return True
        else:
            return False
        pass

    def getKeyContent( self, data ): # user => (str), key => (str)
        content = self.getContent()
        if data['user'] in content.keys():
            return content[data['user']][data['key']]
        else:
            return False
        pass

    def insertUser( self, data ):
        content = self.getContent()
        content[data['user']] = {
            'win': 0,
            'loose': 0,
            'elo': 0,
            'staff': False,
            'equipe': False,
            'host': False,
            'channel': False,
            'pick': 0,
            'draft': False,
            'capitaine': False
        }

        self.insertContent(content)
        pass

database = JsonDatabase('database.json')

@bot.event
async def on_ready():
    print('Bot ON')
    await bot.change_presence(activity=discord.Streaming(name=f'.help - Valorant Ranked', url='https://www.twitch.tv/tt'))
    
@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel != None:
        if after.channel.id == 991632088535150602:
            for guild in bot.guilds:
                maincategory = discord.utils.get(
                    guild.categories, id=991631792345985058)
                secondcategory = discord.utils.get(
                    guild.categories, id=991632429968277537)
                channel2 = await guild.create_voice_channel(name=f'Ranked ({member.display_name})', category=maincategory, user_limit=8)
                channel3 = await guild.create_voice_channel(name=f'Equipe#1 ({member.display_name})', category=secondcategory, user_limit=4)
                channel4 = await guild.create_voice_channel(name=f'Equipe#2 ({member.display_name})', category=secondcategory, user_limit=4)
                await channel4.set_permissions(guild.default_role, connect=False)
                await channel3.set_permissions(guild.default_role, connect=False)
                await member.move_to(channel2)
                tkt = member.display_name

                def check(x, y, z):
                    return len(channel2.members) == 8
                await bot.wait_for('voice_state_update', check=check)
                await channel2.set_permission(guild.default_role, connect=False)
                a = 1
                for i in range(1):
                    for member in channel2.members[0:a]:
                        await member.move_to(channel3)
                        id = member.id
                        if database.userExist({'user': str(id)}):
                            database.updateUser({
                                'user': str(id),
                                'key': 'capitaine',
                                'value': True
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'host',
                                'value': f'{tkt}'
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'channel',
                                'value': 1
                            })
                        else:
                            database.insertUser({'user': str(id)})
                            time.sleep(1)
                            database.updateUser({
                                'user': str(id),
                                'key': 'capitaine',
                                'value': True
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'host',
                                'value': f'{tkt}'
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'channel',
                                'value': 1
                            })
                for i in range(1):
                    for member in channel2.members[0:a]:
                        time.sleep(1)
                        await member.move_to(channel4)
                        id = member.id
                        if database.userExist({'user': str(id)}):
                            database.updateUser({
                                'user': str(id),
                                'key': 'capitaine',
                                'value': True
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'host',
                                'value': f'{tkt}'
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'channel',
                                'value': 2
                            })
                        else:
                            database.insertUser({'user': str(id)})
                            time.sleep(1)
                            database.updateUser({
                                'user': str(id),
                                'key': 'capitaine',
                                'value': True
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'host',
                                'value': f'{tkt}'
                            })
                            database.updateUser({
                                'user': str(id),
                                'key': 'channel',
                                'value': 2
                            })
                            a+=1
                time.sleep(1)
                b = 6
                for i in range(6):
                    for member in channel2.members[0:b]:
                        id = member.id
                        if database.userExist({'user': str(id)}):
                            database.updateUser({
                                'user': str(id),
                                'key': 'host',
                                'value': f'{tkt}'
                            })
                        else:
                            database.insertUser({'user': str(id)})
                            time.sleep(1)
                            database.updateUser({
                                'user': str(id),
                                'key': 'host',
                                'value': f'{tkt}'
                            })
                            b+=6





@bot.event
async def on_message(message):
    if database.userExist({'user': str(message.author.id)}):
        database.insertUser({'user': str(message.author.id)})

    if '.help' in message.content:
        if database.getKeyContent({'user':str(message.author.id),'key':'staff'}) == True:
            embed = discord. Embed(title="Valorant ~ Help", description=f"Voila toute les commandes", color=0xffffff)
            embed. add_field(name="`.profile`", value='Voir vos wins/looses\n\n`.update`\nUpdate son compte pour avoir ces rôles\n\n`.top`\nVoir le LeaderBoard (5 joueurs)\n\n`.pick`\nChoisir ces mates (seulement les capitaines)\n\n`.map`\nVoir la map pour le MDT (RinaOrc)\n\n`.win`\nMettre une win a un utilisateur\n\n`.delwin`\nRetiré une win a un utilisateur\n\n`.loose`\nMettre une loose a un utilisateur\n\n`.delloose`\nRetiré une loose a un utilisateur')
            embed. set_thumbnail(url=f'{image}')
            embed. set_footer(text="Valorant ~ profile")
            await message.channel.send(embed=embed)
        else:
            embed = discord. Embed(title="Valorant ~ Help", description=f"Voila toute les commandes", color=0xffffff)
            embed. add_field(name="`.profile`", value='Voir vos wins/looses\n\n`.update`\nUpdate son compte pour avoir ces rôles\n\n`.top`\nVoir le LeaderBoard (5 joueurs)\n\n`.pick`\nChoisir ces mates (seulement les capitaines)\n\n`.map`\nVoir la map pour le MDT (RinaOrc)')
            embed. set_thumbnail(url=f'{image}')
            embed. set_footer(text="Valorant ~ profile")
            await message.channel.send(embed=embed)

    if '.update' in message.content:
        member = message.author
        elo = database.getKeyContent({'user':str(message.author.id), 'key':'elo'})
        if database.userExist({'user': str(message.author.id)}):
            bronze = discord.utils.get(message.guild.roles, name="Bronze")
            argent = discord.utils.get(message.guild.roles, name="Argent")
            gold = discord.utils.get(message.guild.roles, name="Gold")
            platine = discord.utils.get(message.guild.roles, name="Platine")
            diamand = discord.utils.get(message.guild.roles, name="Diamand")
            if 0 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 99:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Bronze")
                await member.add_roles(role)
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(diamand)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")

            elif 100 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 199:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Argent")
                await member.add_roles(role)
                await member.remove_roles(bronze)
                await member.remove_roles(gold)
                await member.remove_roles(diamand)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")

            elif 200 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 299:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Gold")
                await member.add_roles(role)
                await message.reply("Ton compte a bien été update !")
                await member.remove_roles(argent)
                await member.remove_roles(diamand)
                await member.remove_roles(bronze)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo}) - {message.author.name}')

            elif 300 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 399:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Platine")
                await member.add_roles(role)
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(bronze)
                await member.remove_roles(diamand)
                await message.reply("Ton compte a bien été update !")

            elif 400 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}):
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Diamand")
                await member.add_roles(role)
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(platine)
                await member.remove_roles(bronze)
                await member.edit(nick=f'({elo}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")
            else:
                member = message.author
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(diamand)
                await member.remove_roles(bronze)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")
        else:
            database.insertUser({'user': str(message.author.id)})
            time.sleep(1)
            elo2 = database.getKeyContent({'user':str(message.author.id), 'key':'elo'})
            bronze = discord.utils.get(message.guild.roles, name="Bronze")
            argent = discord.utils.get(message.guild.roles, name="Argent")
            gold = discord.utils.get(message.guild.roles, name="Gold")
            platine = discord.utils.get(message.guild.roles, name="Platine")
            diamand = discord.utils.get(message.guild.roles, name="Diamand")
            await member.edit(nick=f'({elo2}) - {message.author.name}')
            if 0 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 99:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Bronze")
                await member.add_roles(role)
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(diamand)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo2}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")

            elif 100 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 199:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Argent")
                await member.add_roles(role)
                await member.remove_roles(bronze)
                await member.remove_roles(gold)
                await member.remove_roles(diamand)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo2}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")

            elif 200 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 299:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Gold")
                await member.add_roles(role)
                await message.reply("Ton compte a bien été update !")
                await member.remove_roles(argent)
                await member.remove_roles(diamand)
                await member.remove_roles(bronze)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo2}) - {message.author.name}')

            elif 300 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}) <= 399:
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Platine")
                await member.add_roles(role)
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(bronze)
                await member.remove_roles(diamand)
                await member.edit(nick=f'({elo2}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")

            elif 400 <= database.getKeyContent({'user':str(message.author.id), 'key':'elo'}):
                member = message.author
                role = discord.utils.get(message.guild.roles, name="Diamand")
                await member.add_roles(role)
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(platine)
                await member.remove_roles(bronze)
                await member.edit(nick=f'({elo2}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")
            else:
                member = message.author
                await member.remove_roles(argent)
                await member.remove_roles(gold)
                await member.remove_roles(diamand)
                await member.remove_roles(bronze)
                await member.remove_roles(platine)
                await member.edit(nick=f'({elo2}) - {message.author.name}')
                await message.reply("Ton compte a bien été update !")

    if '.staff' in message.content:
        if str(message.author.id) in owner:
            if database.getKeyContent({'user':str(message.author.id),'key':'staff'}) != True:
                database.updateUser({
                    'user': str(message.mentions[0].id),
                    'key': 'staff',
                    'value': True
                })
                await message.reply(f"<@{message.mentions[0].id}> est staff maintenant")
            else:
                database.updateUser({
                    'user': str(message.mentions[0].id),
                    'key': 'staff',
                    'value': False
                })
                await message.reply(f"<@{message.mentions[0].id}> n'est plus staff")

    if '.pick' in message.content:
        if database.getKeyContent({'user':str(message.author.id),'key':'capitaine'}) == True:
            if database.getKeyContent({'user':str(message.author.id),'key':'pick'}) == 3:
                await message.channel.send("Tu as déjà pick tout t'es coéquipiers !")
            else:
                if database.getKeyContent({'user':str(message.mentions[0].id),'key':'host'}) == database.getKeyContent({'user':str(message.author.id),'key':'host'}):
                    if database.getKeyContent({'user':str(message.mentions[0].id),'key':'equipe'}) == False:
                        host = database.getKeyContent({'user':str(message.author.id),'key':'host'})
                        zdazda = database.getKeyContent({'user':str(message.author.id),'key':'channel'})
                        channel2 = discord.utils.get(bot.get_all_channels(), name=f'Equipe#{zdazda} ({host})')
                        id = message.author.id
                        database.updateUser({
                            'user': str(id),
                            'key': 'pick',
                            'value': database.getKeyContent({'user': str(id), 'key': 'pick'}) + 1
                        })
                        if database.userExist({'user': str(message.mentions[0].id)}):
                            database.updateUser({
                                'user': str(message.mentions[0].id),
                                'key': 'equipe',
                                'value': True
                            })
                        else:
                            database.insertUser({'user': str(message.mentions[0].id)})
                            time.sleep(1)
                            database.updateUser({
                                'user': str(message.mentions[0].id),
                                'key': 'equipe',
                                'value': True
                            })
                        member = message.mentions[0]
                        member1 = message.author
                        tt = database.getKeyContent({'user':str(message.author.id),'key':'host'})
                        tet = database.getKeyContent({'user':str(message.author.id),'key':'channel'})
                        channel = discord.utils.get(bot.get_all_channels(), name=f'Equipe#{tet} ({tt})')
                        await channel2.set_permissions(member, connect=True)
                        await channel2.set_permissions(member1, connect=True)
                        await member.move_to(channel)
                        await message.channel.send(f"<@{message.mentions[0].id}> est maintenant dans l'équippe de <@{message.author.id}>")
                    else:
                        await message.channel.send(f"<@{message.mentions[0].id}> est déjà dans une autre équippe")
                else:
                    await message.channel.send(f"<@{message.mentions[0].id}> n'est pas dans la draft !")
        else:
            await message.channel.send("Tu n'es pas Capitaine !")

    if ".map" in message.content:
        liste = ['pearl', 'fracture', 'breeze', 'icebox', 'bind', 'heaven', 'split', 'ascent']
        await message.reply('La map est: ' + liste[randint(0, 8)])

    if ".profile" in message.content:
        id = message.author.id
        if database.userExist({'user': str(id)}) == False:
            database.insertUser({'user': str(id)})
            await message.channel.send("Tu n'as pas encore fait de game !")
        else:
            if "@" in message.content:
                embed = discord. Embed(title="Valorant ~ profile", description=f"""
**Pseudo : {message.mentions[0].name}
ID : {message.mentions[0].id}**

**Elo <:blue:991898476092866610> **{database.getKeyContent({'user':str(message.mentions[0].id),'key':'elo'})}
**wins <:green:991898516018438175> **{database.getKeyContent({'user':str(message.mentions[0].id),'key':'win'})}
**Looses <:red:991898552802496542> **{database.getKeyContent({'user':str(message.mentions[0].id),'key':'loose'})}

                """, color=0xffffff)
                embed. set_footer(text="Valorant ~ profile")
                embed. set_thumbnail(url=f'{image}')
                await message.channel.send(embed=embed)
            else:
                embed = discord. Embed(title="Valorant ~ profile", description=f"""
**Pseudo : {message.author.name}
ID : {message.author.id}**

**Elo <:blue:991898476092866610> **{database.getKeyContent({'user':str(message.author.id),'key':'elo'})}
**wins <:green:991898516018438175> **{database.getKeyContent({'user':str(message.author.id),'key':'win'})}
**Looses <:red:991898552802496542> **{database.getKeyContent({'user':str(message.author.id),'key':'loose'})}
                
                """, color=0xffffff)
                embed. set_thumbnail(url=f'{image}')
                embed. set_footer(text="Valorant ~ profile")
                await message.channel.send(embed=embed)

    if '.top' in message.content:
        content, final_lines = json.load(open("database.json", "r")), []
        members = ""

        for i in content:
            final_lines.append(str(i) + ":" + str(content[i]["elo"]))

            final_lines.sort(key=lambda x:float(x.split(":")[1] + ".0"), reverse=True)
        for i in range(5):
            members+=(f'\n<@{final_lines[i].split(":")[0]}> ID : ``{final_lines[i].split(":")[0]}``  | Elo : **{final_lines[i].split(":")[1]}**')

        embed = discord.Embed(title="__:trophy: **Leaderboard :**__", description=f'{members}', color=0xffffff)
        embed. set_footer(text="Valorant ~ LeaderBoard")
        await message.channel.send(embed = embed)

# ============================================== STAFF =====================================================

    if '.win' in message.content:
        if database.getKeyContent({'user':str(message.author.id),'key':'staff'}) == True:
            id = message.mentions[0].id
            if database.userExist({'user': str(id)}):
                database.updateUser({
                    'user': str(id),
                    'key': 'win',
                    'value': database.getKeyContent({'user': str(id), 'key': 'win'}) + 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'elo'}) + 30
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'capitaine',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'pick',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'channel',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'host',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'equipe',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'draft',
                    'value': False
                })
            else:
                database.insertUser({'user': str(id)})
                time.sleep(1)
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'win'}) + 30
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'win',
                    'value': database.getKeyContent({'user': str(id), 'key': 'win'}) + 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'capitaine',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'pick',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'channel',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'host',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'equipe',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'draft',
                    'value': False
                })
                
            await message.reply(f'La win de <@{message.mentions[0].id}> a bien été mise !')
        else:
            await message.channel.send("Tu n'as pas accès à cette commande !")
    
    if '.delwin' in message.content:
        if database.getKeyContent({'user':str(message.author.id),'key':'staff'}) == True:
            id = message.mentions[0].id
            if database.userExist({'user': str(id)}):
                database.updateUser({
                    'user': str(id),
                    'key': 'win',
                    'value': database.getKeyContent({'user': str(id), 'key': 'win'}) - 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'elo'}) - 30
                })
            else:
                database.insertUser({'user': str(id)})
                time.sleep(1)
                database.updateUser({
                    'user': str(id),
                    'key': 'win',
                    'value': database.getKeyContent({'user': str(id), 'key': 'win'}) - 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'elo'}) - 30
                })
            await message.reply(f'La win de <@{message.mentions[0].id}> a bien été retiré !')
        else:
            await message.channel.send("Tu n'as pas accès à cette commande !")

    if '.loose' in message.content:
        if database.getKeyContent({'user':str(message.author.id),'key':'staff'}) == True:
            id = message.mentions[0].id
            if database.userExist({'user': str(id)}):
                database.updateUser({
                    'user': str(id),
                    'key': 'loose',
                    'value': database.getKeyContent({'user': str(id), 'key': 'loose'}) + 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'elo'}) - 10
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'capitaine',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'pick',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'channel',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'host',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'equipe',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'draft',
                    'value': False
                })
            else:
                database.insertUser({'user': str(id)})
                time.sleep(1)
                database.updateUser({
                    'user': str(id),
                    'key': 'loose',
                    'value': database.getKeyContent({'user': str(id), 'key': 'loose'}) + 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'elo'}) - 10
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'capitaine',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'pick',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'channel',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'host',
                    'value': 0
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'equipe',
                    'value': False
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'draft',
                    'value': False
                })
            await message.reply(f'La loose de <@{message.mentions[0].id}> a bien été mise !')
        else:
            await message.channel.send("Tu n'as pas accès à cette commande !")

    if '.delloose' in message.content:
        if database.getKeyContent({'user':str(message.author.id),'key':'staff'}) == True:
            id = message.mentions[0].id
            if database.userExist({'user': str(id)}):
                database.updateUser({
                    'user': str(id),
                    'key': 'loose',
                    'value': database.getKeyContent({'user': str(id), 'key': 'loose'}) - 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'elo'}) + 10
                })
            else:
                database.insertUser({'user': str(id)})
                time.sleep(1)
                database.updateUser({
                    'user': str(id),
                    'key': 'loose',
                    'value': database.getKeyContent({'user': str(id), 'key': 'loose'}) - 1
                })
                database.updateUser({
                    'user': str(id),
                    'key': 'elo',
                    'value': database.getKeyContent({'user': str(id), 'key': 'elo'}) + 10
                })
            await message.reply(f'La loose de <@{message.mentions[0].id}> a bien été retiré !')
        else:
            await message.channel.send("Tu n'as pas accès à cette commande !")


bot.run(token)