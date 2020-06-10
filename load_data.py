import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx

# Load training data and reduce (subsample) if desired

# Read thru file to get numeric ids for each player 
with open('train.csv') as f: lines = f.read().split('\n')

p = 0; playerid = {};
for i in range(len(lines)):
  csv = lines[i].split(',');
  if len(csv) != 10: continue;   # parse error or blank line
  player0,player1 = csv[1],csv[4];
  if player0 not in playerid: playerid[player0]=p; p+=1;
  if player1 not in playerid: playerid[player1]=p; p+=1;

nplayers = len(playerid)
playername = ['']*nplayers
for player in playerid: playername[ playerid[player] ]=player;  # id to name lookup


# Sparsifying parameters (discard some training examples):
pKeep = 1.0   # fraction of edges to consider (immed. throw out 1-p edges)
nEdge = 3     # try to keep nEdge opponents per player (may be more; asymmetric)
nKeep = 5     # keep at most nKeep games per opponent pairs (play each other multiple times)

nplays, nwins = np.zeros( (nplayers,nplayers) ), np.zeros( (nplayers,nplayers) );
for i in range(len(lines)):
  csv = lines[i].split(',');
  if len(csv) != 10: continue;   # parse error or blank line
  a,b = playerid[csv[1]],playerid[csv[4]];
  aw,bw = csv[2]=='[winner]',csv[5]=='[winner]';
  if (np.random.rand() < pKeep):
    if (nplays[a,b] < nKeep) and ( ((nplays[a,:]>0).sum() < nEdge) or ((nplays[:,b]>0).sum() < nEdge) ):
      nplays[a,b] += 1; nplays[b,a]+=1; nwins[a,b] += aw; nwins[b,a] += bw;


