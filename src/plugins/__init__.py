"""
Sistema de Plugins para APIs de Tradução
Permite adicionar novas APIs de tradução sem modificar o código principal
"""

from .api_plugin_base import APIPluginBase, PluginManager

__all__ = ['APIPluginBase', 'PluginManager']
