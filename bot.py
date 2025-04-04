import discord
from discord.ext import commands
import asyncio
import os
import time
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")

@bot.command(name='ct')
async def conceder_cargo(ctx, role_id: int):
    inicio = time.time()

    role = ctx.guild.get_role(role_id)
    if not role:
        await ctx.send("❌ Cargo não encontrado.")
        return

    await ctx.send(f"🧠 Iniciando atribuição turbo. Cargo `{role.name}` será atribuído em lotes de 20...")

    await ctx.guild.chunk()
    membros = [m for m in ctx.guild.members if not m.bot and role not in m.roles]
    total = len(membros)
    setados, falhas = 0, 0

    def dividir_lotes(lista, tamanho):
        for i in range(0, len(lista), tamanho):
            yield lista[i:i + tamanho]

    for i, lote in enumerate(dividir_lotes(membros, 20)):
        tarefas = [member.add_roles(role, reason="Comando !ct turbo") for member in lote]
        resultados = await asyncio.gather(*tarefas, return_exceptions=True)

        for resultado in resultados:
            if isinstance(resultado, Exception):
                falhas += 1
            else:
                setados += 1

        if setados % 1000 == 0:
            await ctx.send(f"🚀 Já setamos {setados} membros com o cargo `{role.name}`.")

        await asyncio.sleep(5)  # delay reduzido

    duracao = time.time() - inicio

    await ctx.send(
        f"✅ Finalizado!\n"
        f"🎯 Cargo `{role.name}` setado em {setados} membros.\n"
        f"❌ Falhou em {falhas} membros.\n"
        f"⏱️ Tempo total: {round(duracao, 2)} segundos (~{round(duracao / 60, 2)} minutos)."
    )

bot.run(os.getenv("TOKEN_DISCORD"))
