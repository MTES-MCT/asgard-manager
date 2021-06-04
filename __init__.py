# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

def classFactory(iface):
  from .asgard import MainPlugin
  return MainPlugin(iface)