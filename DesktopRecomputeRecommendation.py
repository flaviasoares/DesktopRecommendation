# Como escolher as melhores peças para um computador desktop, dado um certo valor?
# cromossomo = [motherBoard, processor, ramMemory, ssd, gpu]

from collections.abc import Sized
from secrets import SystemRandom
rd = SystemRandom()

# dados a serem usados na geração de cada cromossomo
def data():
  
  global motherboards
  global processors
  global ramMemories
  global ssds
  global gpus

  global motherboardModels
  global processorModels
  global ramMemoryModels
  global ssdModels
  global gpuModels
  
  # valor em reais de cada componente
  motherboards = [462.46, 573.75, 704.00, 978.44, 1167.61, 1643.94, 2004.00]
  processors = [499.06, 799.99, 1069.99, 1440.29, 2035.57, 2347.10, 2618.26]
  ramMemories = [174.50, 209.90, 220.03, 261.25, 616.50, 670.82, 719.00]
  ssds = [129.00, 194.00, 267.00, 474.00, 509.00, 799.00, 1399.00]
  gpus = [650.00, 1399.99, 1431.00, 1859.00, 3200.00, 7811.00, 15749.00]

  # variações de componentes
  motherboardModels = ["ASRock H310CM-HG4", "Gigabyte GA-A320M-S2H", "Asus Prime H510M-E", "Asus TUF Gaming B460M-Plus", 
                       "Gigabyte Z390 M Gaming", "Asus TUF Gaming X570-Plus/BR", "Asus TUF Gaming Z490-Plus"]
  processorModels = ["Intel Core i3-10100f", "AMD Ryzen 5 3600", "Intel Core i5-10400", "Intel Core i5 10600KF", 
                     "AMD Ryzen 5 5600X", "Intel Core i7-11700", "Intel Core i7-10700KF"]
  ramMemoryModels = ["Adata 4 GB DDR4", "DDR4 HyperX Fury 8 GB", "DDR4 PC Yes UDIMM 4 GB", "Corsair Vengeance LPX 8 GB", 
                    "Corsair Vengeance PRO RGB", "Kingston Fury Beast 16 GB", "Kingston 16 GB DDR4"]
  ssdModels = ["Kingston 240gb Sata 3 A400", "Kingston 480gb Sata 3 A400", "Western Digital NVMe 480GB", "Kingston Fury Renegate NVMe 500GB", 
               "Western Digital NVMe 960GB", "Kingston Fury Renegate NVMe 1TB", "Corsair Force MP600 PRO XT NVMe 1TB"]
  gpuModels = ["RandeonRX 550", "Nvidia RTX 3070", "NVIDIA Geforce GTX 1660 Super", "AMD Randeon RX 6600", 
              "Nvidia RTX3060 Ti", "GeForce RTX 2060", "Radeon RX 6900 XT"]

# gera cromossomo
def createChromosome():
  data()
  
  totalValue = 0

  chromosome = {}

  # adiciona valor da placa-mãe
  chromosome["Motherboard"] = [motherboards[rd.randint(0, 6)], motherboardModels[rd.randint(0, 6)]]

  # adiciona valor do processador
  chromosome["Processor"] = [processors[rd.randint(0, 6)], processorModels[rd.randint(0, 6)]]

  # adiciona valor da memória ram
  chromosome["RAM Memory"] = [ramMemories[rd.randint(0, 6)], ramMemoryModels[rd.randint(0, 6)]]

  # adiciona ssd 
  chromosome["SSD"] =[ssds[rd.randint(0, 6)], ssdModels[rd.randint(0, 6)]]

  # adiciona gpu
  chromosome["GPU"] = [gpus[rd.randint(0, 6)], gpuModels[rd.randint(0, 6)]]

  # valor total do computador
  for i in chromosome.values():
    totalValue = totalValue + i[0]
  chromosome["Total Value"] = round(totalValue)

  chromosome["Tempo de Vida"] = 0

  return chromosome

# gera a população
def createPopulation(POPULATION_SIZE):
  population = []

  while len(population) < POPULATION_SIZE:
    c = createChromosome()
    if c["Total Value"] <= budget: # Verifica se o indivíduo não é monstro
      population.append(c)

  return population

# mostra a população
def showPopulation(population):
  for i in range(len(population)):
    print(population[i])

# cria uma lista com valor de adaptabilidade para cada cromossomo
def adaptationRanking(population, budget, component):
  ''' se adapta melhor o cromossomo que tem o componente de maior importância para o usuário - os mais caros e em 
  maior quantidade - e os que são menores ou iguais ao orçamento definido pelo usuário'''
  
  adaptation = []
  difference = []

  # pega os valores totais menos o valor do orçamento e coloca numa lista
  for i in range(len(population)):
    valorDifferent = population[i].get("Total Value") - budget
    difference.append(valorDifferent)

  # print("\n------------- população antes de ser ordenada -------------\n")
  # showPopulation(population)

  # ordena a população de acordo com o valor mais aproximado do orçamento
  for i in range(len(population)):
    for j in range(len(population)):
      if difference[i] > difference[j]:
        aux1 = difference[i]
        difference[i] = difference[j]
        difference[j] = aux1

        aux2 = population[i]
        population[i] = population[j]
        population[j] = aux2

  # print("\n---- população ordenada de acordo com o valor mais próximo do orçamento ----\n")
  # showPopulation(population)

  for i in range(len(population)):
    for key,value in population[i].items():
      #print(key,value)
      if key != "Total Value" and key != 'Tempo de Vida':
        if value[1] == component:
          adaptation.append(1)
        else:
          adaptation.append(0)
  
  if sum(adaptation) > 0:
    for i in range(len(population)):
      for j in range(len(population)):
        if adaptation[i] > adaptation[j]:
          aux1 = difference[i]
          difference[i] = difference[j]
          difference[j] = aux1

          aux2 = population[i]
          population[i] = population[j]
          population[j] = aux2

          aux3 = adaptation[i]
          adaptation[i] = adaptation[j]
          adaptation[j] = aux3

  # showPopulation(population)
  # print("\n---- população ordenada de acordo com o componente da escolha do usuário ----\n")
  
  return adaptation

def showPopWithAdaptation(population, adaptation):
  # print(adaptation)
  for i in range(len(population)):
    print(adaptation[i], " = ", population[i])
  print("\n------------------------------------- end of print fuction - with ranking -------------------------------------\n")

def crossover(population, descendants):
  # Faz a combinação de dois cromossomos e retorna o que tiver melhor valor de adaptação
  new_candidate1 = {}
  new_candidate2 = {}
  for i in range(5):
    for j in range(5):
      x = rd.randint(1, 100)
      corte = rd.randint(0, 4)
      if x > 30 and len(des) < 20:
        limit = 0
        if j != i:
          for key, value in population[i].items():
            if limit <= corte:
              new_candidate1[key] = value
              limit += 1
          
          limit = 0
          for key, value in population[j].items():
            if limit <= corte:
              new_candidate2[key] = value
              limit += 1

          limit = 0
          for key, value in population[i].items():
            if key != "Total Value" and key != 'Tempo de Vida' and limit > corte:
              new_candidate2[key] = value
            limit += 1
          
          limit = 0
          for key, value in population[j].items():
            if key != "Total Value" and key != 'Tempo de Vida' and limit > corte:
              new_candidate1[key] = value
            limit += 1

    totalValue = 0
    for value in new_candidate1.values():
      totalValue += value[0]
    new_candidate1["Total Value"] = round(totalValue, 2)
    new_candidate1["Tempo de Vida"] = 0

    totalValue = 0
    for value in new_candidate2.values():
      totalValue = totalValue + value[0]
    new_candidate2["Total Value"] = round(totalValue, 2)
    new_candidate2["Tempo de Vida"] = 0

    if new_candidate1["Total Value"] < new_candidate2["Total Value"]:
      # print('Cromossomo 1 mais adaptado')
      descendants.append(new_candidate1)

    elif new_candidate1["Total Value"] > new_candidate2["Total Value"]:
      # print('Cromossomo 2 mais adaptado')
      descendants.append(new_candidate2)
    
    elif new_candidate1["Total Value"] == new_candidate2["Total Value"]:
      descendants.append(new_candidate1)
      descendants.append(new_candidate2)
      
    new_candidate1 = {}
    new_candidate2 = {}

def mutation(population):
    new_population = list()
    for crm in population:
        crm_mutation_chance = rd.randint(1, 100)
        if crm_mutation_chance <= 5:
            new_crm = dict()
            for key, value in crm.items():
                new_price, new_model = value
                gene_mutation_chance = rd.randint(1, 100)
                if gene_mutation_chance <= 10:
                    if key == 'Motherboard':
                        new_price = rd.choice(motherboards)
                        new_model = rd.choice(motherboardModels)
                    if key == 'Processor':
                        new_price = rd.choice(processors)
                        new_model = rd.choice(processorModels)
                    if key == 'RAM Memory':
                        new_price = rd.choice(ramMemories)
                        new_model = rd.choice(ramMemoryModels)
                    if key == 'SSD':
                        new_price = rd.choice(ssds)
                        new_model = rd.choice(ssdModels)
                    if key == 'GPU':
                        new_price = rd.choice(gpus)
                        new_model = rd.choice(gpuModels)
                    
                new_crm[key] = [new_price, new_model]
            new_population.append(new_crm)
        else:
            new_population.append(crm)
    
        return new_population

def replacement(population): # Considerando que a população tá ordenada em ordem decrescente
    orig_population = population[:20]
    new_population = createPopulation(10)

    return_population = orig_population[:]
    return_population.extend(new_population)
    
    return return_population

def update_lifespan(population):
  for crm in population:
         crm["Tempo de Vida"] += 1
         if crm["Tempo de Vida"] >= MAX_LIFETIME:
           population.pop(crm)



# valor e component mais importante para o usuário
budget = 3000.00
component = "Intel Core i7-10700KF"

POPULATION_SIZE = 10
SELECT_FOR_CROSSOVER = 5
MAX_LIFETIME = 5 #Tempo de vida máximo em anos

pop = createPopulation(POPULATION_SIZE)
des = []

print("\nPopulação gerada:\n")
showPopulation(pop)

update_lifespan(pop)
adapt = adaptationRanking(pop, budget, component)

print("\nPopulação com valor de adaptação para cada cromossomo:\n")
showPopWithAdaptation(pop, adapt)

# cruza os cinco primeiros cromossomos
crossover(pop, des)
update_lifespan(des)

adaptDes = adaptationRanking(des, budget, component)
print("\nDescendentes da população inicial com valor de adaptação:\n")
showPopWithAdaptation(des, adaptDes)

# print("\nDescendentes da população inicial após mutação:\n")
new_cromossomo = mutation(des)

print("\nNova população com valor de adaptação:\n")
newPop = replacement(pop)
adaptNewPop = adaptationRanking(newPop, budget, component)
showPopWithAdaptation(pop, adapt)
