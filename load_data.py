import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx


def load_data(ver_map, dir='data/', pKeep=1.0, nEdge=9, nKeep=15, opt='train'):

  with open(dir + opt + '.csv', encoding='utf-8') as f:
    lines = f.read().split('\n')

  p = 0
  playerid = {}
  for i in range(len(lines)):
    csv = lines[i].split(',')
    if len(csv) != 10:
      continue  # parse error or blank line
    player0, player1 = csv[1], csv[4]
    if player0 not in playerid:
      playerid[player0] = p
      p += 1
    if player1 not in playerid:
      playerid[player1] = p
      p += 1

  # Sparsifying parameters (discard some training examples):
  # pKeep = 1.0   # fraction of edges to consider (immed. throw out 1-p edges)
  # nEdge = 3     # try to keep nEdge opponents per player (may be more; asymmetric)
  # nKeep = 5     # keep at most nKeep games per opponent pairs (play each other multiple times)

  wins = []
  playerA, playerB = [], []
  raceA, raceB = [], []
  counters = []

  nplayers = len(playerid)
  nplays = np.zeros((nplayers, nplayers))
  race = {'P': 0, 'T': 1, 'Z': 2}
  for i in range(len(lines)):
    csv = lines[i].split(',')
    if len(csv) != 10 or csv[6] == 'R' or csv[7] == 'R':
      continue  # parse error or blank line
    a, b = playerid[csv[1]], playerid[csv[4]]
    aw, bw = csv[2] == '[winner]', csv[5] == '[winner]'

    if (np.random.rand() < pKeep):
      if (nplays[a, b] < nKeep) and (((nplays[a, :] > 0).sum() < nEdge) or ((nplays[:, b] > 0).sum() < nEdge)):
        nplays[a, b] += 1
        nplays[b, a] += 1

        playerA.append(a + 1)
        playerB.append(b + 1)
        wins.append(1 if aw else 0)
        raceA.append(race[csv[6]])
        raceB.append(race[csv[7]])

        counters.append(int(ver_map[csv[8]][race[csv[6]], race[csv[7]]]))

  return playerid, nplayers, playerA, playerB, raceA, raceB, wins, counters


def load_valid_data(playerid, ver_map, dir='data/', pKeep=1.0, nEdge=3, nKeep=5, opt='valid'):
  with open(dir + opt + '.csv', encoding='utf-8') as f:
    lines = f.read().split('\n')
  nplayers = len(playerid)

  games = []
  race = {'P': 0, 'T': 1, 'Z': 2}
  nplays, nwins = np.zeros((nplayers, nplayers)), np.zeros((nplayers, nplayers))
  for i in range(len(lines)):
    csv = lines[i].split(',')
    if len(csv) != 10 or csv[6] == 'R' or csv[7] == 'R':
      continue  # parse error or blank line

    a, b = playerid[csv[1]], playerid[csv[4]]
    aw, bw = csv[2] == '[winner]', csv[5] == '[winner]'

    if (np.random.rand() < pKeep):
      if (nplays[a, b] < nKeep) and (((nplays[a, :] > 0).sum() < nEdge) or ((nplays[:, b] > 0).sum() < nEdge)):
        nplays[a, b] += 1
        nplays[b, a] += 1
        nwins[a, b] += aw
        nwins[b, a] += bw
        counter = int(ver_map[csv[8]][race[csv[6]], race[csv[7]]])
        games.append((a, b, aw, race[csv[6]], race[csv[7]], counter))

  return playerid, nplayers, nplays, nwins, games


def load_counter(dir='data/', opt='train'):
  #  Race: Z - Zerg, P - Protoss, T - Terran
  #  WoL- Wings of Liberty, HotS - Heart of the Swarm, LotV - Legacy of the Void
  with open(dir + opt + '.csv', encoding='utf-8') as f:
    lines = f.read().split('\n')

  WoL = np.zeros((3, 3))
  HotS = np.zeros((3, 3))
  LotV = np.zeros((3, 3))
  race_map = {'P': 0, 'Z': 1, 'T': 2}
  ver_map = {'WoL': np.zeros((3, 3)), 'HotS': np.zeros((3, 3)), 'LotV': np.zeros((3, 3))}
  ver_map_total = {'WoL': np.zeros((3, 3)), 'HotS': np.zeros((3, 3)), 'LotV': np.zeros((3, 3))}
  for line in lines:
    csv = line.split(',')
    if len(csv) != 10 or csv[6] == 'R' or csv[7] == 'R':
      continue  # parse error or blank line
    r1, r2 = race_map[csv[6]], race_map[csv[7]]
    ver_map[csv[8]][r1, r2] += csv[5] == '[winner]'
    ver_map[csv[8]][r2, r1] += csv[5] != '[winner]'
    ver_map_total[csv[8]][r1, r2] += 1
    ver_map_total[csv[8]][r2, r1] += 1

  for k, v in ver_map.items():
    ver_map[k] /= ver_map_total[k]
    ver_map[k] = ver_map[k] > 0.5

  return ver_map

