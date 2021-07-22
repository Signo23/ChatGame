# -*- coding: utf-8 -*-
"""
Created on Thu Jul 22 12:40:53 2021

@author: lory4
"""
from random import randint

def random_role():
    return role[randint(1, num_role)]
    
num_question = 15
num_role = 5

question = {1 : "Qual è il vero nome di Gerry Scotti? ", 
            2 : "In che anno è scoppiata la pandemia da Covid19? ",
            3 : "Tutti sanno aprirlo ma nessuno chiuderlo. Cos'è? ",
            4 : "Il gruppo di Bono Vox",
            5 : "Chi ha vinto i Mondiali di calcio nel 2006?",
            6 : "Fabbrica Italiana Automobili Torino",
            7 : "Il numero di Michael Jordan dopo il suo ritorno ",
            8 : "Viene spesso scambiato per un topo ma è molto più docile",
            9 : "Tre uomini e una...",
            10 : "In che anno usc' la prima versione stabile di Minecraft?",
            11 : "Azienda fondata nel 1976 a Cupertino ",
            12 : "La città giapponese dell'incidente nucleare del 2011  ",
            13 : "La prima guerra mondiale è anche chiamata ---- guerra(inserire la parola al posto dei trattini)",
            14 : "Il famoso programma automobilistico della BBC",
            15 : "Il marchio di telefonia considerato incontrastabile prima dell'avvento di Apple"}
answer = {1 : "Virginio",
            2 : "2020" ,
            3 : "Uovo",
            4 : "U2",
            5 : "Italia", 
            6 : "FIAT",
            7 : "45",
            8 : "Criceto",
            9 : "Gamba",
            10 : "2009",
            11 : "Apple",
            12 : "Fukushima",
            13 : "Grande",
            14 : "Top Gear",
            15 : "Nokia"}

role = {1 : "Aldo",
            2 : "Giovanni" ,
            3 : "Giacomo",
            4 : "Server",
            5 : "Client"}