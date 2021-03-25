import math
import random
import numpy as np
from copy import copy

# ------Dekode Kromosom------

def CreateKromosom(lenKromosom): 
    # for i in range(0, lenKromosom):
    # Array_CreateKromosom.append(np.random.randint(0, 2))
    return [random.randint(0, 1) for x in range(0, lenKromosom)]


def Populasi(nPopulasi, lenKromosom):
    Array_Populasi = []
    for x in range(nPopulasi):
        Array_Populasi.append(CreateKromosom(lenKromosom))
    return Array_Populasi


def dekodeKromosom(CreateKromosom):
    dekodeKromosom = []
    rmin1, rmax1 = -1, 2
    rmin2, rmax2 = -1, 1
    kali1, bagi1 = 0, 0
    kali2, bagi2 = 0, 0
    Individux1 = CreateKromosom[0:len(CreateKromosom)//2]
    Individux2 = CreateKromosom[len(CreateKromosom)//2:]

    for i in range(len(Individux1)):
        kali1 = kali1 + (Individux1[i]*(2**(-(i+1))))
        bagi1 = bagi1 + 2**-(i+1)

    for i in range(len(Individux2)):
        kali2 = kali2 + (Individux2[i]*(2**(-(i+1))))
        bagi2 = bagi2 + 2**(-(i+1))

    hasil_x1 = rmin1 + (rmax1 - rmin1) * kali1 / bagi1
    hasil_x2 = rmin2 + (rmax2 - rmin2) * kali2 / bagi2

    dekodeKromosom.append(hasil_x1)
    dekodeKromosom.append(hasil_x2)

    return dekodeKromosom

# -----Perhitungan Fitness-----

def rumus(hasil_x1, hasil_x2):
    return math.cos(hasil_x1**2) * math.sin(hasil_x2**2) + (hasil_x1 + hasil_x2) #rumus


def fungsi_fitness(h):
    f = h #Nilai Maksimum f=h
    return f


def Hitung_Fitness(Populasi):
    Pfitness = []
    hasilRumus = []
    hasil_x = []
    for i in range(len(Populasi)):
        individu = Populasi[i]
        hasil_x1, hasil_x2 = dekodeKromosom(individu)
        hasil = rumus(hasil_x1, hasil_x2)
        hasil_fitness = fungsi_fitness(hasil)
        Pfitness.append(hasil_fitness)
        hasilRumus.append(hasil)
        hasil_x.append([hasil_x1, hasil_x2])

    return Pfitness, hasilRumus, hasil_x

# -----Pemilihan Orang Tua-----

def Tournament_Parent(pop, k, fitness):
    # k :berapa banyak melakukan tournament
    best = 0
    individu = ((random.randint(0, len(pop[0])-1)) for i in range(k))
    # individu = (random.randint(0, len(pop[0])-1))
    # for i in range(k):
    if best == 0 or (fitness[individu] > fitness(best)):
        best == individu
    return pop[best]

# -----Crossover-----

def Crossover(induk1, induk2, peluang):
    r = random.uniform(0, 1)
    induk1 = copy(induk1)
    induk2 = copy(induk2)
    anakInduk1 = copy(induk1)
    anakInduk2 = copy(induk2)

    if (r <= peluang):
        T1 = random.randint(0, len(induk1)//2)
        T2 = random.randint(len(induk1)//2, len(induk1)-1)
        anakInduk1 = induk1[0:T1]+induk2[T1:]
        anakInduk2 = induk2[0:T1]+induk1[T1:]
    return anakInduk1, anakInduk2

# -----Mutasi-----

def Mutasi(anakInduk1, anakInduk2, peluang):
    r = random.uniform(0, 1)
    for i in range(len(anakInduk1)):
        if (r <= peluang):
            if(anakInduk1[i] == 0):
                anakInduk1[i] = 1
            else:
                anakInduk1[i] = 0
        if (r <= peluang):
            if(anakInduk2[i] == 0):
                anakInduk2[i] = 1
            else:
                anakInduk2[i] = 0

    return anakInduk1, anakInduk2

# -----------------------------

def sort_generasi(Populasi, fitnes, hasilRumus, populasi_x1x2):
    zipping = zip(fitnes, Populasi,  hasilRumus, populasi_x1x2)
    sorting = sorted(zipping)
    fitnes, Populasi, hasilRumus, populasi_x1x2 = zip(*sorting)
    listPop = list(Populasi)
    listFit = list(fitnes)
    listHx = list(hasilRumus)
    listPop_x1x2 = list(populasi_x1x2)

    return listPop, listFit, listHx, listPop_x1x2

# -----Pergantian Generasi-----

Kromosom = CreateKromosom(7) #Panjang Kromosom = 7
x1, x2 = dekodeKromosom(Kromosom)
result = rumus(x1, x2)
P = Populasi(10, 7) #Panjang Populasi 10 dan Panjang Kromosom 7
Pf, hx, x = Hitung_Fitness(P)
i = 1
while i < 9: #Batas Berhenti
    P, Pf, hx, x = sort_generasi(P, Pf, hx, x)
    induk1 = Tournament_Parent(P, 15, Pf)
    induk2 = Tournament_Parent(P, 15, Pf)
    anakInduk1, anakInduk2 = Crossover(induk1, induk2, 0.7) #Pc = 0.7
    anakInduk1, anakInduk2 = Mutasi(anakInduk2, anakInduk2, 0.1) #Pm = 0.1
    P[0] = anakInduk1
    P[1] = anakInduk2
    i = i+1
    if i == 9:
        P, Pf, hx, x = sort_generasi(P, Pf, hx, x)

# -----Main Program-----

print("================== Generasi terbaik ========================")
print("Kromosom terbaik : ", P[9])
print("Fitness          : ", Pf[9])
print("x dan y          : ", x[9])
print("============================================================")