#!/usr/bin/python
# -*- coding: utf8 -*-

import sys,json
supernodes= [ "kaah","supernode","euer","pa_sharepoint","oxberg" ]
""" TODO: Refactoring needed to pull the edges out of the node structures again,
it should be easier to handle both structures"""
DUMP_FILE = "/krebs/db/availability"
def write_digraph(nodes):
  """
  writes the complete digraph in dot format
  """
  print ('digraph retiolum {')
  #print ('  graph [center rankdir=LR packMode="clust"]')
  print ('  graph [center packMode="clust"]')
  print ('  node[shape=box,style=filled,fillcolor=grey]')
  print ('  overlap=false')
  generate_stats(nodes)
  merge_edges(nodes)
  write_stat_node(nodes)
  for k,v in nodes.iteritems():
    write_node(k,v)
  print ('}')
def dump_graph(nodes):
  from time import time
  graph = {}
  graph['nodes'] = nodes
  graph['timestamp'] = time()
  f = open(DUMP_FILE,'a')
  json.dump(graph,f)
  f.write('\n')
  f.close()
def write_stat_node(nodes):
  ''' Write a `stats` node in the corner
      This node contains infos about the current number of active nodes and connections inside the network
  '''
  num_conns = 0
  num_nodes = len(nodes)
  for k,v in nodes.iteritems():
    num_conns+= len(v['to'])
  node_text = "  stats_node [label=\"Statistics\\l"
  node_text += "Active Nodes: %s\\l" % num_nodes
  node_text += "Connections : %s\\l" % num_conns
  node_text += "\""
  node_text += ",fillcolor=green"
  node_text += "]"
  print(node_text)

def generate_stats(nodes):
  """ Generates some statistics of the network and nodes
  """
  try:
    f = open(DUMP_FILE,'r')
    f.close()
  except Exception,e:
    f = []
  jlines = []
  for line in f:
    jlines.append(json.loads(line))
  for k,v in nodes.iteritems():
    conns = v.get('to',[])
    v['num_conns'] = len(conns)
    v['avg_weight'] = get_node_avg_weight(conns)
    v['availability'] = get_node_availability(k,jlines)
    sys.stderr.write( "%s -> %f\n" %(k ,v['availability']))
def get_node_avg_weight(conns):
  """ calculates the average weight for the given connections """
  if not conns:
    sys.syderr.write("get_node_avg_weight: connection parameter empty")
    return 9001
  else:
    return sum([float(c['weight']) for c in conns])/len(conns)
def get_node_availability(name,jlines):
  """ calculates the node availability by reading the generated dump file
  adding together the uptime of the node and returning the time
	parms:
          name - node name
          jlines - list of already parsed dictionaries node archive
  """
  begin = last = current = 0
  uptime = 0
  #sys.stderr.write ( "Getting Node availability of %s\n" % name)
  for stat in jlines:
    ts = stat['timestamp']
    if not begin:
      begin = last = ts
    current = ts
    if stat['nodes'].get(name,{}).get('to',[]):
      uptime += current - last
    else:
      pass
      #sys.stderr.write("%s offline at timestamp %f\n" %(name,current))
    last = ts
  all_the_time = last - begin
  try:
    return uptime/ all_the_time
  except:
    return 1

def delete_unused_nodes(nodes):
  new_nodes = {}
  for k,v in nodes.iteritems():
    if v['external-ip'] == "(null)":
      continue
    if v.get('to',[]):
      new_nodes[k] = v
  for k,v in new_nodes.iteritems():
    if not [ i for i in v['to'] if i['name'] in new_nodes]:
      #del(new_nodes[k])
      del(k)
  return new_nodes
def merge_edges(nodes):
  """ merge back and forth edges into one
  DESTRUCTS the current structure by deleting "connections" in the nodes
  """
  for k,v in nodes.iteritems():
    for con in v.get('to',[]):
      for i,secon in enumerate(nodes.get(con['name'],{}).get('to',[])):
        if k == secon['name']:
          del (nodes[con['name']]['to'][i])
          con['bidirectional'] = True


def write_node(k,v):
  """ writes a single node and its edges 
      edges are weightet with the informations inside the nodes provided by
      tinc
  """

  node = "  "+k+"[label=\""
  node += k+"\\l"
  node += "availability: %f\\l" % v['availability'] 
  node += "avg weight: %.2f\\l" % v['avg_weight'] 
  if v.has_key('num_conns'):
    node += "Num Connects:"+str(v['num_conns'])+"\\l"
  node += "external:"+v['external-ip']+":"+v['external-port']+"\\l"
  for addr in v.get('internal-ip',['¯\\\\(°_o)/¯']):
    node += "internal:"+addr+"\\l"
  node +="\""
  if k in supernodes:
    node += ",fillcolor=steelblue1"
  #node +=",group=\""+v['external-ip'].replace(".","")+"\""
  node += "]"
  print node

  for con in v.get('to',[]):
    label  = con['weight']
    w = int(con['weight'])
    weight = str(1000 - (((w - 150) * (1000 - 0)) / (1000 -150 )) + 0)

    length = str(float(w)/1500)
    #weight = "1000" #str(300/float(con['weight']))
    #weight = str((100/float(con['weight'])))
    #weight = str(-1 * (200-100000/int(con['weight'])))
    if float(weight) < 0 :
      weight= "1"

    #sys.stderr.write(weight + ":"+ length +" %s -> " %k + str(con) + "\n")
    edge = "  "+k+ " -> " +con['name'] + "[label="+label + " weight="+weight #+ " minlen="+length
    if con.get('bidirectional',False):
      edge += ",dir=both"
    edge += "]"
    print edge

def decode_input(FILE):
  return json.load(FILE)
nodes = decode_input(sys.stdin)
nodes = delete_unused_nodes(nodes)
try:
  dump_graph(nodes)
except Exception,e:
  sys.stderr.write("Cannot dump graph: %s" % str(e))
write_digraph(nodes)