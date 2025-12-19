"""
Módulo de Verificação e Instalação de Sistema
Verifica dependências e instala automaticamente se necessário
Com suporte a cores no terminal usando colorama
"""

import sys
import subprocess
import importlib
import os
from typing import Tuple, List, Optional

# Tenta importar colorama, se não existir, instala
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Fallback para quando colorama não está instalado
    class Fore:
        RED = GREEN = YELLOW = CYAN = WHITE = MAGENTA = BLUE = RESET = ""
    
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""


class VerificadorSistema:
    """Classe para verificar e instalar dependências do sistema"""
    
    # Dependências principais do projeto
    DEPENDENCIAS = {
        'PySide6': 'PySide6>=6.6.0',
        'requests': 'requests>=2.31.0',
        'psutil': 'psutil>=5.9.0',
        'colorama': 'colorama>=0.4.6',
    }
    
    # Dependências opcionais (apenas para build)
    DEPENDENCIAS_BUILD = {
        'PyInstaller': 'pyinstaller'
    }
    
    def __init__(self, verbose: bool = True):
        """
        Inicializa o verificador
        
        Args:
            verbose: Se True, imprime mensagens detalhadas
        """
        self.verbose = verbose
        self.erros = 0
        self.avisos = 0
        self.instalacoes = 0
        
    def print_sucesso(self, mensagem: str):
        """Imprime mensagem de sucesso em verde"""
        if self.verbose:
            print(f"{Fore.GREEN}✓ {mensagem}{Style.RESET_ALL}")
    
    def print_erro(self, mensagem: str):
        """Imprime mensagem de erro em vermelho"""
        if self.verbose:
            print(f"{Fore.RED}✗ {mensagem}{Style.RESET_ALL}")
        self.erros += 1
    
    def print_aviso(self, mensagem: str):
        """Imprime mensagem de aviso em amarelo"""
        if self.verbose:
            print(f"{Fore.YELLOW}⚠ {mensagem}{Style.RESET_ALL}")
        self.avisos += 1
    
    def print_info(self, mensagem: str):
        """Imprime mensagem informativa em ciano"""
        if self.verbose:
            print(f"{Fore.CYAN}ℹ {mensagem}{Style.RESET_ALL}")
    
    def print_titulo(self, mensagem: str):
        """Imprime título em destaque"""
        if self.verbose:
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'='*70}")
            print(f"  {mensagem}")
            print(f"{'='*70}{Style.RESET_ALL}\n")
    
    def print_secao(self, mensagem: str):
        """Imprime título de seção"""
        if self.verbose:
            print(f"\n{Fore.CYAN}{Style.BRIGHT}[{mensagem}]{Style.RESET_ALL}\n")
    
    def verificar_python(self) -> Tuple[bool, str]:
        """
        Verifica se Python está instalado
        
        Returns:
            Tupla (instalado, versão)
        """
        try:
            versao = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            return True, versao
        except:
            return False, ""
    
    def verificar_pip(self) -> bool:
        """
        Verifica se pip está disponível
        
        Returns:
            True se pip está disponível
        """
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "--version"],
                check=True,
                capture_output=True,
                text=True
            )
            return True
        except:
            return False
    
    def verificar_biblioteca(self, nome: str) -> bool:
        """
        Verifica se uma biblioteca está instalada
        
        Args:
            nome: Nome da biblioteca
            
        Returns:
            True se a biblioteca está instalada
        """
        try:
            importlib.import_module(nome)
            return True
        except ImportError:
            return False
    
    def instalar_biblioteca(self, nome: str, pacote: str) -> bool:
        """
        Instala uma biblioteca usando pip
        
        Args:
            nome: Nome da biblioteca para display
            pacote: Nome do pacote pip
            
        Returns:
            True se instalação foi bem-sucedida
        """
        try:
            self.print_info(f"Instalando {nome}...")
            
            resultado = subprocess.run(
                [sys.executable, "-m", "pip", "install", pacote, "--quiet"],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutos de timeout
            )
            
            if resultado.returncode == 0:
                self.print_sucesso(f"{nome} instalado com sucesso!")
                self.instalacoes += 1
                return True
            else:
                self.print_erro(f"Falha ao instalar {nome}: {resultado.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.print_erro(f"Timeout ao instalar {nome}")
            return False
        except Exception as e:
            self.print_erro(f"Erro ao instalar {nome}: {e}")
            return False
    
    def atualizar_pip(self) -> bool:
        """
        Atualiza o pip para a versão mais recente
        
        Returns:
            True se atualização foi bem-sucedida
        """
        try:
            self.print_info("Atualizando pip...")
            
            resultado = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
                capture_output=True,
                text=True,
                timeout=180
            )
            
            if resultado.returncode == 0:
                self.print_sucesso("pip atualizado com sucesso!")
                return True
            else:
                self.print_aviso("Não foi possível atualizar pip (não crítico)")
                return False
                
        except Exception as e:
            self.print_aviso(f"Aviso ao atualizar pip: {e} (não crítico)")
            return False
    
    def verificar_dependencias_principais(self, auto_instalar: bool = False) -> bool:
        """
        Verifica todas as dependências principais
        
        Args:
            auto_instalar: Se True, instala automaticamente dependências faltantes
            
        Returns:
            True se todas as dependências estão instaladas
        """
        self.print_secao("Verificando Dependências Principais")
        
        todas_ok = True
        faltantes = []
        
        for nome, pacote in self.DEPENDENCIAS.items():
            if self.verificar_biblioteca(nome):
                self.print_sucesso(f"{nome}: instalado")
            else:
                self.print_aviso(f"{nome}: NÃO INSTALADO")
                faltantes.append((nome, pacote))
                todas_ok = False
        
        # Se auto_instalar está ativo, instala dependências faltantes
        if auto_instalar and faltantes:
            print(f"\n{Fore.YELLOW}Instalando dependências faltantes...{Style.RESET_ALL}")
            
            for nome, pacote in faltantes:
                self.instalar_biblioteca(nome, pacote)
            
            # Nota: colorama será recarregado na próxima execução do script
        
        return todas_ok or (auto_instalar and len(faltantes) > 0)
    
    def verificar_dependencias_build(self) -> bool:
        """
        Verifica dependências de build (PyInstaller)
        
        Returns:
            True se PyInstaller está instalado
        """
        self.print_secao("Verificando Dependências de Build")
        
        for nome, pacote in self.DEPENDENCIAS_BUILD.items():
            if self.verificar_biblioteca(nome):
                self.print_sucesso(f"{nome}: instalado")
                return True
            else:
                self.print_info(f"{nome}: não instalado (opcional, apenas para criar .exe)")
                return False
        
        return False
    
    def verificar_arquivos_projeto(self) -> bool:
        """
        Verifica se os arquivos principais do projeto existem
        
        Returns:
            True se todos os arquivos essenciais existem
        """
        self.print_secao("Verificando Arquivos do Projeto")
        
        # Descobre o diretório raiz do projeto
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        arquivos_essenciais = [
            'src/main.py',
            'src/gui/main_window.py',
            'src/database.py',
            'requirements.txt'
        ]
        
        todos_ok = True
        
        for arquivo in arquivos_essenciais:
            caminho = os.path.join(base_dir, arquivo)
            if os.path.exists(caminho):
                self.print_sucesso(arquivo)
            else:
                self.print_erro(f"{arquivo} - NÃO ENCONTRADO")
                todos_ok = False
        
        # Verifica executável (opcional)
        exe_path = os.path.join(base_dir, 'dist', 'GameTranslator.exe')
        if os.path.exists(exe_path):
            self.print_sucesso("Executável: criado em dist/GameTranslator.exe")
        else:
            self.print_info("Executável: ainda não criado (use INSTALAR.bat opção 4)")
        
        return todos_ok
    
    def verificar_tudo(self, auto_instalar: bool = False) -> bool:
        """
        Executa verificação completa do sistema
        
        Args:
            auto_instalar: Se True, instala dependências automaticamente
            
        Returns:
            True se sistema está pronto
        """
        self.print_titulo("GAME TRANSLATOR - VERIFICAÇÃO DO SISTEMA")
        
        # 1. Verifica Python
        self.print_secao("Verificando Python")
        python_ok, versao = self.verificar_python()
        
        if python_ok:
            self.print_sucesso(f"Python {versao} encontrado")
        else:
            self.print_erro("Python NÃO ENCONTRADO")
            self.print_info("Baixe em: https://www.python.org/downloads/")
            return False
        
        # 2. Verifica pip
        self.print_secao("Verificando pip")
        if self.verificar_pip():
            self.print_sucesso("pip disponível")
            
            # Atualiza pip se solicitado
            if auto_instalar:
                self.atualizar_pip()
        else:
            self.print_erro("pip NÃO ENCONTRADO")
            return False
        
        # 3. Verifica dependências
        deps_ok = self.verificar_dependencias_principais(auto_instalar)
        
        # 4. Verifica dependências de build (opcional)
        self.verificar_dependencias_build()
        
        # 5. Verifica arquivos
        arquivos_ok = self.verificar_arquivos_projeto()
        
        # Resumo final
        self.print_titulo("RESUMO DA VERIFICAÇÃO")
        
        if self.erros == 0 and self.avisos == 0:
            self.print_sucesso("✓ SISTEMA PRONTO!")
            self.print_info("Execute EXECUTAR.bat ou use o executável em dist/GameTranslator.exe")
            return True
        elif self.erros == 0:
            self.print_aviso(f"⚠ Sistema OK, mas {self.avisos} aviso(s) encontrado(s)")
            if self.instalacoes > 0:
                self.print_sucesso(f"✓ {self.instalacoes} dependência(s) instalada(s) automaticamente")
            return True
        else:
            self.print_erro(f"✗ {self.erros} erro(s) e {self.avisos} aviso(s) encontrado(s)")
            self.print_info("Corrija os erros antes de continuar")
            return False


def main():
    """Função principal para execução standalone"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Verifica e instala dependências do Game Translator'
    )
    parser.add_argument(
        '--auto-instalar',
        action='store_true',
        help='Instala automaticamente dependências faltantes'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Modo silencioso (sem mensagens detalhadas)'
    )
    
    args = parser.parse_args()
    
    verificador = VerificadorSistema(verbose=not args.quiet)
    sucesso = verificador.verificar_tudo(auto_instalar=args.auto_instalar)
    
    if not args.quiet:
        input("\nPressione ENTER para sair...")
    
    return 0 if sucesso else 1


if __name__ == "__main__":
    sys.exit(main())
