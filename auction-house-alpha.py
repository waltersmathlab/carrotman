import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import os
import math
import datetime
from datetime import datetime
from collections import Counter

#market for cyklerbot; made by 677333268345126973

from utils import data, save_data, insert_data, get_data, rcolor, delete_data, list_all_keys, list_keys_with_prefix, developer_check, loadinv, createinv, additem, profile_intialization_check
save_data(data)
class AHLBButtons(discord.ui.View):
    def __init__(self,client,page_num,m, *, timeout=60):
        super().__init__(timeout=timeout)
        self.items_per_page = 5
        self.client = client
        self.page_num = 1
        self.m = m
        self.max_page = (len(sorted(m.items(), key=lambda item: item[1], reverse=True)) + self.items_per_page - 1) // self.items_per_page
    
    def create_leaderboard_embed(self, page_num, m,sort):
        sorted_items = sorted(m.items(), key=lambda item: item[sort])
        items_per_page = self.items_per_page
        start_index = (page_num - 1) * items_per_page
        end_index = min(start_index + items_per_page, len(sorted_items))
        page_items = sorted_items[start_index:end_index]
        embed = discord.Embed(title="Auction House", color=random.choice(rcolor))
        field_value = "\n".join(f"**{item} x {amt}**     Ends in <t:{endtime}:R>"+"\n"+f"   Cost: ${cost} Seller: {user}" for i, (user,tuser,item,amt,cost,endtime) in enumerate(page_items))
        embed.add_field(name=f"Page {page_num}/{(len(sorted_items) + items_per_page - 1) // items_per_page}", value=field_value, inline=True)
        return embed
    
    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple,disabled=True)
    async def left_button(self,interaction,button):
        self.page_num -= 1
        if self.page_num <= 1:
            button.disabled = True
        if self.page_num < self.max_page:
            for discord.ui.button in self.children:
                if discord.ui.button.label == ">":
                    discord.ui.button.disabled = False
        embed = self.create_leaderboard_embed(self.page_num,self.m)
        await interaction.response.edit_message(embed=embed,view=self)
    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple)
    async def right_button(self,interaction,button):
        self.page_num += 1
        if self.page_num == self.max_page:
            button.disabled = True
        if self.page_num > 1:
            for discord.ui.button in self.children:
                if discord.ui.button.label == "<":
                    discord.ui.button.disabled = False
        embed = self.create_leaderboard_embed(self.page_num,self.m)
        await interaction.response.edit_message(embed=embed,view=self)


class AHDevCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    group = app_commands.Group(name="auction", description="A group of auction commands.")   
    
    @group.command(name="house", description="Shows the auction house.")
    async def marketshow(self, interaction: discord.Interaction,sort:int | None):
        if sort is None:
            sort=1
        await interaction.response.defer()
        page_num = 1
        items_per_page=4
        guild_id = interaction.guild_id
        try:
            ahlist = data[f"ah{guild_id}"]
        except:
            data[f"ah{guild_id}"] = {}
            ahlist = {}
        current_time = round(datetime.timestamp(datetime.now()))
        ahlist = {k: v for k, v in ahlist.items() if v[5] > current_time}
        if len(ahlist) < 1:
            return await interaction.followup.send(f"There are currently no items on the auction house.")
        embed = self.create_leaderboard_embed(page_num,ahlist,sort)
        if (len(sorted(ahlist.items(), key=lambda item: item[sort])) + items_per_page - 1) // items_per_page <= 1:
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(embed=embed,view=AHLBButtons(self.client,page_num,ahlist))

    @group.command(name="update", description="Updates AH.")
    async def marketupd(self, interaction: discord.Interaction):
        await interaction.response.defer()
        guild_id = interaction.guild_id
        try:
            ahexlist = data[f"ah{guild_id}"]
        except:
            data[f"ah{guild_id}"] = {}
            ahexlist = {}
        current_time = round(datetime.timestamp(datetime.now()))
        ahexlist = {k: v for k, v in ahexlist.items() if v[5] < current_time}
        if len(ahexlist)<1:
            return await interaction.followup.send("All expired auctions have been claimed.")
        for i in ahexlist:
            embed = discord.Embed(colour=discord.Colour.random())
            if data[f"ah{guild_id}"][i][0]==data[f"ah{guild_id}"][i][1]:
                additem('inv' + str(guild_id) + data[f"ah{guild_id}"][i][1],data[f"ah{guild_id}"][i][2],data[f"ah{guild_id}"][i][3])
                embed.add_field(name=f'Auction ID {i}', value=f'{data[f"ah{guild_id}"][i][1]}s auction has no bids and {data[f"ah{guild_id}"][i][2]} x {data[f"ah{guild_id}"][i][3]} has been returned.', inline=True)
            else:
                embed.add_field(name=f'Auction ID {i}', value=f'The top bidder is {data[f"ah{guild_id}"][i][1]} and he got {data[f"ah{guild_id}"][i][2]} x {data[f"ah{guild_id}"][i][3]}.'+"\n", inline=True)
                await interaction.followup.send
                additem('inv' + str(guild_id) + data[f"ah{guild_id}"][i][1],data[f"ah{guild_id}"][i][2],data[f"ah{guild_id}"][i][3])
                for key,value in data[f"esc{guild_id}"][i].items():
                    if key!=data[f"ah{guild_id}"][i][1]:
                        data[f'm{guild_id}{key}']+=value
                        embed.add_field(value=f"escrow returns ${value} to {key}")
                data[f'm{guild_id}{data[f"ah{guild_id}"][i][0]}']+=data[f"ah{guild_id}"][i][4]
            await interaction.followup.send(embed=embed)
            del data[f"ah{guild_id}"][i]
            del data[f"esc{guild_id}"][i]


    @group.command(name="bid", description = "Bid on an item in the auction house.")
    @app_commands.describe(id = 'ID of item you are bidding on.')
    @app_commands.describe(cost = 'How much you are bidding for.')
    async def auctionbid(self, interaction: discord.Interaction, id: int, cost: int):
        await interaction.response.defer()
        id=str(id)
        guild_id = interaction.guild_id
        buser=f'<@{interaction.user.id}>'
        try:
            user=data[f"ah{guild_id}"][id][0]
            item=data[f"ah{guild_id}"][id][2]
            amt=data[f"ah{guild_id}"][id][3]
            xcost=data[f"ah{guild_id}"][id][4]
        except:
            return await interaction.followup.send(f'Item not found.', ephemeral=True)
        if xcost>=cost:
            return await interaction.followup.send(f'You cannot bid lower than the current bid.', ephemeral=True)
        if math.floor(xcost*1.05)>=cost:
            return await interaction.followup.send(f'You have to bid at least ${math.floor(xcost*1.05)}, or 5% more than the current bid.', ephemeral=True)
        if buser==data[f"ah{guild_id}"][id][1]:
            return await interaction.followup.send(f'You are already the top bidder on this auction.', ephemeral=True)
        if user!=buser:
            try:
                dcost=data[f'esc{guild_id}'][id][buser]
            except:
                dcost=0
                try:
                    data[f'esc{guild_id}'][id][buser]=0
                except:
                    try:
                        data[f'esc{guild_id}'][id]={}
                        data[f'esc{guild_id}'][id][buser]=0
                    except:
                        data[f'esc{guild_id}']={}
                        data[f'esc{guild_id}'][id]={}
                        data[f'esc{guild_id}'][id][buser]=0

            try:
                temp=data[f'm{guild_id}{buser}']
            except:
                data[f'm{guild_id}{buser}']=0
            if data[f'm{guild_id}{buser}']>=cost-dcost:
                    data[f'm{guild_id}{buser}']+=-(cost-dcost)
                    data[f'ah{guild_id}'][id][1]=buser
                    data[f'ah{guild_id}'][id][4]=cost
                    try:
                        data[f'esc{guild_id}'][id][buser]=cost
                    except:
                        try:
                            data[f'esc{guild_id}'][id]={}
                        except:
                            data[f'esc{guild_id}']={}
                            data[f'esc{guild_id}'][id]={}
                            data[f'esc{guild_id}'][id][buser]=cost
                    save_data(data)
                    await interaction.followup.send(f'You bid on {item} x {amt} for ${cost} from {user}.')
            else:
                    await interaction.followup.send(f'Not enough money.', ephemeral=True)
        else:
            await interaction.followup.send(f'You cannot bid on your own items or delist them. ', ephemeral=True)
    
    @group.command(name="list", description = "List an item on the ah.")
    @app_commands.describe(item = 'Item to list.')
    @app_commands.describe(amt = 'Amount of item to list.')
    @app_commands.describe(cost = 'Cost of item on listing (for all items).')
    @app_commands.describe(hours = 'Amount of hours the item will be sellable.')
    async def marketlist(self, interaction: discord.Interaction, item: str, amt: int, cost:int,hours:float):
        await interaction.response.defer()
        guild_id = interaction.guild_id
        user=f'<@{interaction.user.id}>'
        try:
            ahid=data[f"ahid{guild_id}"]
        except:
            data[f"ahid{guild_id}"]=0
            ahid=0
        endtime=round(datetime.timestamp(datetime.now())+3600*hours)
        if amt<1 or cost<1 or hours<=0:
            return await interaction.followup.send(f'Please enter positive integers.', ephemeral=True)
        if hours>168:
            return await interaction.followup.send(f'Cannot list auctions for longer than 1 week.', ephemeral=True)
        try:
            count=data[f"inv{guild_id}{user}"][item]
        except:
            count=0
        if count>=amt:
            try:
                data[f"ah{guild_id}"][ahid]=([f"<@{interaction.user.id}>",user,item,amt,cost,endtime])
            except:
                data[f"ah{guild_id}"]={}
                data[f"ah{guild_id}"][ahid]=([f"<@{interaction.user.id}>",user,item,amt,cost,endtime])
            additem('inv' + str(guild_id) + str(user),item,-amt)
            data[f"ahid{guild_id}"]+=1
            save_data(data)
            await interaction.followup.send(f'You listed {item} x {amt} onto the market for ${cost} with auction id {ahid}. Item expires <t:{endtime}:R>')
        else:
            await interaction.followup.send(f'not enough of {item}.', ephemeral=True)
            
#lb test

    def create_leaderboard_embed(self, page_num, m,sort):
        sorted_items = sorted(m.items(), key=lambda item: item[1][sort-1])
        items_per_page = 4
        start_index = (page_num - 1) * items_per_page
        end_index = min(start_index + items_per_page, len(sorted_items))
        page_items = sorted_items[start_index:end_index]
        embed = discord.Embed(title="Auction House", color=random.choice(rcolor))
        field_value = "\n".join(f"**{item} x {amt}**     Ends <t:{endtime}:R>"+"\n"+f"   Current Bid: ${cost} by {tuser}"+"\n"+f"Item ID: {key} | Auction sold by {user}" for i, (key,(user,tuser,item,amt,cost,endtime)) in enumerate(page_items))
        embed.add_field(name=f"Page {page_num}/{(len(sorted_items) + items_per_page - 1) // items_per_page}", value=field_value, inline=True)
        return embed
    
    
async def setup(client):
    await client.add_cog(AHDevCog(client))