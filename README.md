# 🎮 Game Translator

Sistema profissional de tradução para arquivos JSON e XML de jogos e mods, com preservação total da estrutura original.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🚀 Instalação Rápida (Windows)

### Método 1: Instalador Automático (Recomendado)

1. **Baixe** ou extraia todos os arquivos do projeto
2. **Execute** `INSTALAR.bat` como administrador
3. **Selecione** a opção `[1] Instalação Completa`
4. **Aguarde** a instalação automática
5. **Pronto!** O executável estará em `dist\GameTranslator.exe`

### Método 2: Execução Direta (Desenvolvimento)

1. Certifique-se de ter Python 3.8+ instalado
2. Execute `EXECUTAR.bat`
3. As dependências serão instaladas automaticamente

### 🔄 Manter Atualizado

Para manter o Game Translator sempre atualizado:

1. **Execute** `ATUALIZAR.bat`
2. **Selecione** a opção `[1] Atualizar Repositório Completo`
3. **Aguarde** a sincronização com a versão mais recente
4. **Pronto!** Todas as melhorias e correções serão aplicadas automaticamente

> 💡 **Dica**: Execute `ATUALIZAR.bat` regularmente para obter novos recursos e correções de bugs!

## 📋 Arquivos do Instalador

| Arquivo | Descrição |
|---------|-----------|
| `INSTALAR.bat` | 🚀 Instalador completo com menu interativo |
| `EXECUTAR.bat` | ▶️ Executa o programa rapidamente |
| `VERIFICAR_SISTEMA.bat` | 🔍 Verifica compatibilidade do sistema com **cores no terminal** |
| `ATUALIZAR.bat` | 🔄 Atualiza o repositório e dependências automaticamente |

> **Novo! 🎨** Os scripts agora utilizam **cores personalizadas no terminal**:
> - ✅ **Verde brilhante** para operações bem-sucedidas
> - ❌ **Vermelho brilhante** para erros
> - ⚠️ **Amarelo brilhante** para avisos
> - ℹ️ **Ciano brilhante** para informações
> - 🔷 **Azul brilhante** para seções
> - 🌟 **Branco brilhante** para destaques
> - 💜 **Magenta brilhante** para títulos

### 🔄 Novo: Sistema de Atualização Automática

O arquivo `ATUALIZAR.bat` oferece:
- **Atualização Completa**: Sincroniza o repositório Git e atualiza todas as dependências
- **Verificação de Atualizações**: Verifica se há novas versões disponíveis
- **Atualização de Dependências**: Atualiza apenas os pacotes Python
- **Verificação de Estado**: Mostra o estado atual do repositório Git
- **Interface Colorida**: Menu interativo com cores personalizadas para melhor visualização

## 🎯 Características Principais

### Tradução Inteligente
- **Preservação Total**: Nunca altera chaves, tags, IDs, variáveis ou formatação
- **Memória de Tradução**: Banco de dados SQLite local e selecionável
- **Padrões Numéricos**: Traduz "Soldier 1" → "Soldado 1" automaticamente aplica a "Soldier 2", "Soldier 3", etc.
- **Reaproveitamento**: Traduções anteriores são aplicadas automaticamente

### Interface Moderna
- **Tema Escuro**: Design profissional e confortável
- **Visualizador de Banco**: Veja e edite todas as traduções salvas
- **Progresso em Tempo Real**: Acompanhe o status das operações
- **Monitor de Recursos**: Visualize uso de RAM e CPU

### Segurança e Estabilidade
- **Limite de Memória**: Máximo 500MB de RAM
- **Limite de CPU**: Máximo 80% de uso
- **Validação de Arquivos**: Verifica tamanho e integridade
- **Backup Automático**: Cria backup antes de salvar
- **Timeout de Operações**: Evita travamentos

### APIs de Tradução
- **DeepL**: API profissional de alta qualidade
- **Google Translate**: Ampla cobertura de idiomas

## 📦 Requisitos do Sistema

| Componente | Mínimo | Recomendado |
|------------|--------|-------------|
| Sistema | Windows 10 | Windows 11 |
| Arquitetura | 64-bit | 64-bit |
| RAM | 4 GB | 8 GB |
| Espaço | 500 MB | 1 GB |
| Python | 3.8 | 3.11+ |

## 📖 Como Usar

### 1. Selecionar Banco de Dados

Ao iniciar, o programa solicita um banco de dados:
- **Criar Novo**: Cria um arquivo `.db` vazio
- **Abrir Existente**: Usa um banco de dados anterior

> 💡 **Dica**: Use bancos diferentes para projetos diferentes!

### 2. Importar Arquivo

1. Clique em **"📁 Importar Arquivo"**
2. Selecione um arquivo `.json` ou `.xml`
3. Escolha o perfil de regex adequado

### 3. Traduzir

| Método | Descrição |
|--------|-----------|
| **Manual** | Duplo clique na célula de tradução |
| **Memória** | Clique em "⚡ Aplicar Memória" |
| **API** | Clique em "🤖 Traduzir Auto" |

### 4. Salvar

- Clique em **"💾 Salvar"**
- Um backup automático será criado

## 🗄️ Visualizador de Banco de Dados

Acesse via **Menu > Banco de Dados > Visualizar** ou botão **"🗄️ Ver Banco"**:

- **Buscar**: Encontre traduções específicas
- **Filtrar**: Por categoria
- **Editar**: Duplo clique para editar
- **Excluir**: Remova traduções incorretas
- **Exportar/Importar**: CSV para backup ou compartilhamento

## 🎮 Perfis Pré-configurados

| Perfil | Jogos/Mods |
|--------|------------|
| JSON Genérico | Qualquer arquivo JSON |
| XML Genérico | Qualquer arquivo XML |
| Bannerlord XML | Mount & Blade II: Bannerlord |
| RimWorld XML | RimWorld e mods |

## ⚙️ Configurações

### APIs de Tradução

1. Acesse **"⚙️ Config"**
2. Cole sua chave de API
3. Selecione a API ativa

**Obter chaves:**
- [DeepL API](https://www.deepl.com/pro-api) (gratuito até 500k caracteres/mês)
- [Google Cloud Translation](https://cloud.google.com/translate)

### Limites de Segurança

| Limite | Valor | Descrição |
|--------|-------|-----------|
| Arquivo máximo | 100 MB | Evita travamentos |
| RAM máxima | 500 MB | Protege o sistema |
| CPU máxima | 80% | Evita aquecimento |
| Entradas máximas | 100.000 | Por arquivo |
| Timeout | 300s | Por operação |

## 📁 Estrutura do Projeto

```
game-translator/
├── 📄 INSTALAR.bat          # Instalador principal
├── 📄 EXECUTAR.bat          # Execução rápida
├── 📄 VERIFICAR_SISTEMA.bat # Verificação de compatibilidade (com cores!)
├── 📄 ATUALIZAR.bat         # Atualizador do repositório (NOVO!)
├── 📄 requirements.txt      # Dependências Python
├── 📄 README.md             # Este arquivo
├── 📁 src/                  # Código-fonte
│   ├── main.py              # Ponto de entrada
│   ├── database.py          # Memória de tradução
│   ├── file_processor.py    # Processamento de arquivos
│   ├── smart_translator.py  # Tradução inteligente
│   ├── translation_api.py   # APIs de tradução
│   ├── regex_profiles.py    # Perfis de regex
│   ├── security.py          # Segurança e otimização
│   ├── logger.py            # Sistema de logs
│   ├── verificar_sistema.py # Verificação do sistema com cores
│   └── gui/
│       └── main_window.py   # Interface gráfica
├── 📁 profiles/             # Perfis de regex salvos
├── 📁 logs/                 # Arquivos de log
└── 📁 dist/                 # Executável gerado
    └── GameTranslator.exe
```

## 🛡️ Segurança

O programa implementa múltiplas camadas de proteção:

1. **Validação de Entrada**
   - Sanitização de textos
   - Prevenção de SQL injection
   - Validação de regex (anti-ReDoS)

2. **Proteção de Recursos**
   - Monitor de RAM/CPU em tempo real
   - Garbage collection automático
   - Processamento em chunks

3. **Proteção de Arquivos**
   - Validação de tamanho
   - Backup automático
   - Verificação de integridade

4. **Estabilidade**
   - Timeout em todas operações
   - Tratamento de exceções
   - Recuperação de erros

## 🐛 Solução de Problemas

### Python não encontrado

```
❌ PYTHON NÃO ENCONTRADO!
```

**Solução:**
1. Baixe Python em [python.org](https://www.python.org/downloads/)
2. Durante instalação, marque **"Add Python to PATH"**
3. Reinicie o instalador

### Erro ao criar executável

```
❌ Erro durante a criação do executável
```

**Solução:**
1. Execute `VERIFICAR_SISTEMA.bat`
2. Instale dependências faltantes
3. Tente novamente

### Programa lento ou travando

**Solução:**
1. Verifique uso de RAM no monitor
2. Feche outros programas
3. Use arquivos menores
4. Aumente memória virtual do Windows

### Traduções não aplicadas

**Solução:**
1. Verifique se o perfil de regex está correto
2. Teste com perfil "Genérico"
3. Crie um perfil personalizado

## 📝 Criar Perfil Personalizado

1. Crie arquivo em `profiles/MeuPerfil.json`:

```json
{
  "name": "Meu Perfil",
  "description": "Perfil para meu jogo",
  "file_type": "xml",
  "capture_patterns": [
    "<text>([^<]+)</text>",
    "label=\"([^\"]+)\""
  ],
  "exclude_patterns": [
    "<id>.*?</id>",
    "<!--.*?-->"
  ]
}
```

2. Reinicie o programa
3. Selecione o novo perfil

## 🔄 Atualizações Futuras

- [ ] Suporte para YAML e INI
- [ ] Editor visual de perfis
- [ ] Modo colaborativo em rede
- [ ] Mais APIs de tradução
- [ ] Corretor ortográfico integrado
- [ ] Exportação para formatos de tradução (PO, XLIFF)

## 📄 Licença

Este projeto é distribuído sob a licença MIT.

## 👨‍💻 Autor

Desenvolvido por **Manus AI**

---

## 💡 Dicas Rápidas

> 🎯 **Use bancos separados** para cada projeto de tradução

> ⚡ **Traduza textos únicos primeiro** - o sistema aprende e aplica automaticamente

> 💾 **Exporte seu banco regularmente** para backup

> 🔍 **Verifique o perfil de regex** se textos não forem extraídos corretamente

---

**Nota**: Este software foi projetado para preservar completamente a estrutura dos arquivos originais. Sempre revise as traduções antes de usar em produção.
