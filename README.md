# 🎮 Game Translator

Sistema profissional de tradução para arquivos JSON e XML de jogos e mods, com preservação total da estrutura original.

![Version](https://img.shields.io/badge/version-1.2.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-Windows%2011-blue)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🚀 Instalação Rápida (Windows)

### Método 1: Instalador Automático (Recomendado)

1. **Baixe** ou extraia todos os arquivos do projeto
2. **Execute** `INSTALAR.ps1` no PowerShell como administrador
3. **Selecione** a opção `[1] Instalação Completa`
4. **Aguarde** a instalação automática
5. **Pronto!** O executável estará em `dist\GameTranslator.exe`

### Método 2: Execução Direta (Desenvolvimento)

1. Certifique-se de ter Python 3.8+ instalado
2. Execute `EXECUTAR.ps1` no PowerShell
3. As dependências serão instaladas automaticamente

### 🔄 Manter Atualizado

Para manter o Game Translator sempre atualizado:

1. Use `git pull` para obter a versão mais recente
2. Reinstale as dependências se necessário com `pip install -r requirements.txt`
3. **Pronto!** Todas as melhorias e correções serão aplicadas automaticamente

> 💡 **Dica**: Mantenha o repositório atualizado regularmente para obter novos recursos e correções de bugs!

## 📋 Arquivos do Instalador

| Arquivo | Descrição |
|---------|-----------|
| `INSTALAR.ps1` | 🚀 Instalador completo com menu interativo (PowerShell) |
| `EXECUTAR.ps1` | ▶️ Executa o programa rapidamente (PowerShell) |
| `VERIFICAR_SISTEMA.ps1` | 🔍 Verifica compatibilidade do sistema com **cores no terminal** (PowerShell) |

> **Novo! 🎨** Os scripts agora utilizam **cores personalizadas no terminal**:
> - ✅ **Verde brilhante** para operações bem-sucedidas
> - ❌ **Vermelho brilhante** para erros
> - ⚠️ **Amarelo brilhante** para avisos
> - ℹ️ **Ciano brilhante** para informações
> - 🔷 **Azul brilhante** para seções
> - 🌟 **Branco brilhante** para destaques
> - 💜 **Magenta brilhante** para títulos



## 🎯 Características Principais

### Tradução Inteligente
- **Preservação Total**: Nunca altera chaves, tags, IDs, variáveis ou formatação
- **Memória de Tradução**: Banco de dados SQLite local e selecionável
- **Padrões Numéricos**: Traduz "Soldier 1" → "Soldado 1" automaticamente aplica a "Soldier 2", "Soldier 3", etc.
- **Reaproveitamento**: Traduções anteriores são aplicadas automaticamente

### Interface Moderna
- **Tema Escuro**: Design profissional e confortável
- **Copiar/Colar**: Ctrl+C e Ctrl+V para editar traduções em massa no Notepad
- **Seleção Múltipla**: Selecione e edite várias linhas simultaneamente
- **Auto-ajuste de Altura**: Linhas da tabela se ajustam automaticamente ao tamanho do conteúdo
- **Ajuste de Colunas**: Arraste as bordas das colunas para ajustar a largura conforme necessário
- **Visualizador de Banco**: Veja, edite e exclua traduções salvas (tecla Delete)
- **Progresso em Tempo Real**: Acompanhe o status das operações
- **Monitor de Recursos**: Visualize uso de RAM e CPU

### Segurança e Estabilidade
- **Limite de Memória**: Máximo 500MB de RAM
- **Limite de CPU**: Máximo 80% de uso
- **Validação de Arquivos**: Verifica tamanho e integridade
- **Backup Automático**: Cria backup antes de salvar na pasta `backups/`
- **Organização de Backups**: Todos os backups ficam organizados em uma pasta dedicada
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
| **Copiar/Colar** | Ctrl+C para copiar, editar no Bloco de Notas, Ctrl+V para colar |
| **Memória** | Clique em "⚡ Aplicar Memória" (aplica a todas ou apenas às linhas selecionadas) |
| **API** | Clique em "🤖 Traduzir Auto" (traduz todas ou apenas as linhas selecionadas) |

> 💡 **Novo!** Use **Ctrl+C** e **Ctrl+V** para copiar múltiplas linhas e editar no Notepad!

> 💡 **Dica de Tradução Seletiva**: Selecione linhas específicas antes de usar "⚡ Aplicar Memória" ou "🤖 Traduzir Auto" para traduzir apenas essas linhas!

### 4. Salvar

- Clique em **"💾 Salvar"**
- Um backup automático será criado na pasta **`backups/`**
- Os backups ficam organizados no mesmo diretório do arquivo original
- Nome do backup: `[arquivo].backup_[data]_[hora]`

> 💡 **Dica**: Os backups são salvos em uma pasta dedicada para facilitar a organização e recuperação de versões anteriores!

## 🗄️ Visualizador de Banco de Dados

Acesse via **Menu > Banco de Dados > Visualizar** ou botão **"🗄️ Ver Banco"**:

- **Buscar**: Encontre traduções específicas
- **Filtrar**: Por categoria
- **Editar**: Duplo clique para editar
- **Excluir**: Remova traduções incorretas (botão 🗑️ ou tecla Delete)
- **Ajustar Colunas**: Arraste as bordas das colunas para ajustar a largura horizontalmente
- **Auto-ajuste Vertical**: As alturas das linhas se ajustam automaticamente ao conteúdo
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
├── 📄 INSTALAR.ps1          # Instalador principal (PowerShell)
├── 📄 EXECUTAR.ps1          # Execução rápida (PowerShell)
├── 📄 VERIFICAR_SISTEMA.ps1 # Verificação de compatibilidade (PowerShell)
├── 📄 build_exe.ps1         # Script de build do executável (PowerShell)
├── 📄 build.sh              # Script de build alternativo (Bash)
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
│       ├── main_window.py   # Interface gráfica principal
│       └── regex_editor.py  # Editor de perfis de regex
├── 📁 profiles/             # Perfis de regex salvos
├── 📁 bds/                  # Bancos de dados de tradução
├── 📁 docs/                 # Documentação adicional
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
1. Execute `VERIFICAR_SISTEMA.ps1` no PowerShell
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

## 📚 Documentação Técnica

### Módulos do Sistema

O Game Translator é composto por diversos módulos especializados que trabalham em conjunto para fornecer uma solução robusta de tradução:

#### 🎯 **main.py** - Ponto de Entrada
Módulo principal do aplicativo que inicializa a interface gráfica.

**⚙️ Funções principais:**
- `main()`: Função principal que inicializa o QApplication e a janela principal

**✨ Características:**
- Detecta se está rodando como executável PyInstaller ou script Python
- Configura paths corretos para imports funcionarem em ambos os modos
- Aplica tema Fusion para interface moderna

---

#### 🗄️ **database.py** - Memória de Tradução
Gerencia a persistência de traduções usando SQLite com suporte a múltiplos bancos de dados.

**📦 Classe principal:** `TranslationMemory`

**🔌 Métodos de conexão:**
- `connect(db_path)`: Conecta a um arquivo de banco de dados
- `is_connected()`: Verifica se está conectado
- `get_db_path()`: Retorna o caminho do banco atual
- `close()`: Fecha a conexão com o banco

**🌐 Métodos de tradução:**
- `add_translation(original, translated, source_lang, target_lang, category, notes)`: Adiciona ou atualiza uma tradução
- `get_translation(original)`: Busca uma tradução específica
- `get_all_translations(category, search_term, limit, offset)`: Retorna todas as traduções com filtros
- `get_translation_by_id(translation_id)`: Busca tradução por ID
- `update_translation(translation_id, translated_text, category, notes)`: Atualiza uma tradução existente
- `delete_translation(translation_id)`: Deleta uma tradução
- `delete_translations_by_ids(ids)`: Deleta múltiplas traduções

**🛠️ Métodos utilitários:**
- `get_categories()`: Retorna lista de categorias únicas
- `search(term)`: Busca traduções por termo
- `get_stats()`: Retorna estatísticas do banco (total, usos, categorias)
- `export_to_file(filepath)`: Exporta para CSV
- `import_from_file(filepath)`: Importa de CSV
- `clear_all()`: Limpa todo o banco

**⚙️ Função auxiliar:**
- `create_new_database(filepath)`: Cria um novo arquivo de banco de dados

**🗂️ Estrutura do banco:**
- Tabela `translations`: Armazena todas as traduções com metadados
- Tabela `metadata`: Metadados do banco (versão, data de criação)
- Índices otimizados para busca rápida por texto original e categoria

---

#### 🧠 **smart_translator.py** - Tradução Inteligente
Implementa lógica de reaproveitamento automático e reconhecimento de padrões.

**📦 Classe principal:** `SmartTranslator`

**🌐 Métodos de tradução:**
- `translate(text)`: Traduz um texto usando memória e padrões inteligentes
- `batch_translate(texts)`: Traduz múltiplos textos de uma vez
- `auto_translate_batch(texts)`: Tradução automática com detecção de padrões
- `learn_pattern(original, translated)`: Aprende um novo padrão de tradução

**🔍 Métodos internos de padrões:**
- `_find_numeric_pattern(text)`: Busca padrões numéricos (ex: "Soldier 1" → "Soldado 1")
- `_find_similar_numeric_patterns(base_text)`: Busca padrões numéricos similares na memória
- `_find_variation_pattern(text)`: Busca padrões de variação (ex: "Light/Heavy", "Small/Large")

**✨ Padrões suportados:**
- Numéricos: "Item 1", "Item 2", etc.
- Variações: Light/Heavy, Small/Large, Minor/Major, Weak/Strong, Basic/Advanced, Old/New, Young/Old, Male/Female, Upper/Lower

---

#### 🌐 **translation_api.py** - APIs de Tradução
Suporte para múltiplas APIs de tradução com otimizações para planos gratuitos.

**📋 Classes de gerenciamento:**

**⚡ `APILimits`** - Limites dos planos gratuitos:
- DeepL Free: 500.000 caracteres/mês, 5 requisições/segundo
- Google Cloud Free: 500.000 caracteres/mês, 10 requisições/segundo
- LibreTranslate: Sem limites (self-hosted)
- MyMemory Free: 5.000 caracteres/dia

**💾 `TranslationCache`** - Cache em memória:
- `get(text, source_lang, target_lang)`: Busca tradução no cache
- `set(text, translation, source_lang, target_lang)`: Armazena no cache
- `clear()`: Limpa o cache
- Implementa LRU (Least Recently Used) com tamanho máximo de 10.000 entradas

**📊 `UsageTracker`** - Rastreamento de uso:
- `add_usage(api, chars)`: Registra uso de caracteres
- `get_remaining(api)`: Retorna caracteres restantes
- `can_use(api, chars)`: Verifica se pode usar a API
- `get_stats()`: Retorna estatísticas de uso
- Persiste dados em `api_usage.json`

**⏱️ `RateLimiter`** - Controle de taxa:
- `wait_if_needed(api)`: Aguarda se necessário para respeitar limites

**🤖 Classes de tradutores:**

**🔷 `DeepLTranslator`** - API DeepL:
- `translate(text, source_lang, target_lang)`: Traduz texto individual
- `translate_batch(texts, source_lang, target_lang)`: Traduz múltiplos textos
- Detecta automaticamente se é chave gratuita ou paga
- Suporta idiomas: EN, PT-BR, ES, FR, DE, IT, JA, ZH, KO, RU

**🔶 `GoogleTranslator`** - API Google Translate:
- `translate(text, source_lang, target_lang)`: Traduz texto individual
- `translate_batch(texts, source_lang, target_lang)`: Traduz em lotes (até 100 por vez)
- Batching nativo para economizar requisições

**🔸 `MyMemoryTranslator`** - API MyMemory (gratuita):
- `translate(text, source_lang, target_lang)`: Traduz usando MyMemory
- Sem chave: 1000 palavras/dia
- Com email: 10000 palavras/dia

**🔹 `LibreTranslator`** - LibreTranslate (gratuita):
- `translate(text, source_lang, target_lang)`: Traduz usando LibreTranslate
- Suporta múltiplos servidores públicos com fallback automático
- Sem limites em servidores self-hosted

**🎛️ `TranslationAPIManager`** - Gerenciador principal:
- `add_deepl(api_key)`: Adiciona API DeepL
- `add_google(api_key)`: Adiciona API Google
- `add_mymemory(email)`: Adiciona API MyMemory
- `add_libre(server_url, api_key)`: Adiciona API LibreTranslate
- `set_active_api(api_name)`: Define API ativa
- `translate(text, source_lang, target_lang)`: Traduz com fallback automático
- `translate_batch(texts, source_lang, target_lang)`: Traduz múltiplos textos
- `get_available_apis()`: Lista APIs disponíveis
- `get_usage_stats()`: Retorna estatísticas de uso
- `get_api_info()`: Informações sobre APIs configuradas
- **Persistência automática**: Salva configurações em `api_config.json`

---

#### 🔍 **regex_profiles.py** - Perfis de Regex
Gerencia perfis personalizados para extração de texto de diferentes formatos.

**📦 Classe principal:** `RegexProfile`
- `to_dict()`: Converte perfil para dicionário
- `from_dict(data)`: Cria perfil a partir de dicionário

**🎯 Classe gerenciadora:** `RegexProfileManager`

**🔧 Métodos principais:**
- `save_profile(profile)`: Salva perfil em arquivo JSON
- `load_profile(filepath)`: Carrega perfil de arquivo JSON
- `load_all_profiles()`: Carrega todos os perfis do diretório
- `get_profile(name)`: Obtém perfil pelo nome
- `get_all_profile_names()`: Lista todos os perfis
- `delete_profile(name)`: Deleta um perfil
- `export_profile(name, export_path)`: Exporta perfil para compartilhamento
- `import_profile(import_path)`: Importa perfil externo

**⚙️ Função auxiliar:**
- `slugify(text)`: Converte texto em nome de arquivo seguro

**📋 Perfis padrão:**
- JSON Genérico: Extrai valores de strings em JSON
- XML Genérico: Extrai conteúdo de tags XML
- Bannerlord XML: Específico para Mount & Blade II
- RimWorld XML: Específico para RimWorld

**💾 Persistência:**
- Perfis salvos em `profiles/` como arquivos `.json`
- Carregamento automático na inicialização

---

#### 🛡️ **security.py** - Segurança e Otimização
Garante estabilidade, segurança e performance do sistema.

**⚙️ Classe de configuração:** `SecurityLimits`
- MAX_FILE_SIZE_MB: 100 MB
- MAX_MEMORY_USAGE_MB: 500 MB
- MAX_CPU_PERCENT: 80%
- MAX_ENTRIES_PER_FILE: 100.000
- MAX_TEXT_LENGTH: 10.000 caracteres
- OPERATION_TIMEOUT_SEC: 300 segundos
- CHUNK_SIZE: 1.000 itens
- GC_THRESHOLD_MB: 200 MB

**🔒 Classe de validação:** `SecurityValidator`

**✅ Métodos de validação:**
- `validate_file_path(filepath)`: Valida caminho de arquivo (anti-path traversal)
- `validate_file_size(filepath)`: Valida tamanho de arquivo
- `sanitize_text(text)`: Remove padrões perigosos (XSS, scripts)
- `sanitize_sql_param(param)`: Previne SQL injection
- `validate_regex_pattern(pattern)`: Valida regex (anti-ReDoS)

**📊 Classe de monitoramento:** `ResourceMonitor` (Singleton)

**📈 Métodos de monitoramento:**
- `get_memory_usage_mb()`: Retorna uso de RAM em MB
- `get_cpu_percent()`: Retorna uso de CPU em %
- `check_resources()`: Verifica se recursos estão dentro dos limites
- `force_gc_if_needed()`: Força garbage collection se necessário
- `start_monitoring(callback)`: Inicia monitoramento contínuo
- `stop_monitoring()`: Para monitoramento

**🎨 Decoradores de segurança:**
- `@safe_operation(timeout, max_retries)`: Operações com timeout e retry
- `@memory_safe`: Verifica memória antes e depois da operação
- `@validate_input`: Sanitiza inputs de string automaticamente

**⚡ Classe de processamento:** `ChunkProcessor`
- `process(items, processor, progress_callback)`: Processa itens em chunks com callback de progresso
- `cancel()`: Cancela processamento

**⏰ Classe watchdog:** `OperationWatchdog`
- `start()`: Inicia watchdog
- `reset()`: Reseta timer
- `stop()`: Para watchdog

**💾 Classe de auto-save:** `AutoSaveManager`
- `start()`: Inicia auto-save periódico
- `stop()`: Para auto-save
- `mark_changed()`: Marca alterações não salvas
- `mark_saved()`: Marca como salvo

**🛠️ Funções utilitárias:**
- `get_system_info()`: Retorna informações do sistema (CPU, RAM, disco)
- `is_safe_to_proceed()`: Verifica se é seguro prosseguir com operações

---

#### 📝 **logger.py** - Sistema de Logs
Registra todas as operações do sistema com rotação diária.

**📦 Classe principal:** `AppLogger`

**📝 Métodos de log:**
- `debug(message)`: Registra mensagem de debug
- `info(message)`: Registra mensagem informativa
- `warning(message)`: Registra aviso
- `error(message, exc_info)`: Registra erro
- `critical(message, exc_info)`: Registra erro crítico

**🎯 Métodos especializados:**
- `log_file_operation(operation, filepath, success)`: Registra operações de arquivo
- `log_translation(original, translated, method)`: Registra traduções realizadas
- `log_api_call(api_name, success, error)`: Registra chamadas de API
- `log_profile_operation(operation, profile_name, success)`: Registra operações com perfis
- `get_recent_logs(lines)`: Retorna logs recentes

**✨ Características:**
- Logs salvos em `logs/game_translator_YYYYMMDD.log`
- Formato timestamped: `YYYY-MM-DD HH:MM:SS - Nome - Level - Mensagem`
- Dual output: arquivo (INFO+) e console (WARNING+)
- Rotação diária automática

**🌐 Instância global:**
- `app_logger`: Instância global compartilhada

---

#### 📄 **file_processor.py** - Processamento de Arquivos
Extrai, processa e reinsere traduções em arquivos JSON/XML.

**📋 Classe de dados:** `TranslationEntry`
- `index`: Índice da entrada
- `original_text`: Texto original
- `translated_text`: Texto traduzido
- `position`: Posição no arquivo
- `context`: Contexto (linha completa)

**📦 Classe principal:** `FileProcessor`

**📁 Métodos de arquivo:**
- `load_file(filepath)`: Carrega arquivo para processamento
- `save_file(filepath, content, create_backup)`: Salva arquivo traduzido com backup opcional

**🔍 Métodos de extração:**
- `extract_texts()`: Extrai textos traduzíveis do arquivo
- `_extract_json_default()`: Extração padrão para JSON
- `_extract_xml_default()`: Extração padrão para XML
- `_extract_with_profile()`: Extração usando perfil de regex personalizado

**🌐 Métodos de tradução:**
- `apply_translations(translations)`: Aplica traduções ao conteúdo original
- `get_statistics()`: Retorna estatísticas (total, traduzidos, pendentes, progresso)

**✨ Características:**
- Suporta arquivos JSON e XML
- Preserva 100% da estrutura original
- Backup automático em `backups/` com timestamp
- Remove duplicatas mantendo primeira ocorrência
- Processa de trás para frente para manter posições

---

#### 🖥️ **gui/main_window.py** - Interface Gráfica
Interface gráfica completa construída com PySide6 (Qt).

**📦 Classe principal:** `MainWindow`

**✨ Características principais:**
- Tema escuro profissional
- Tabela editável com ajuste automático de altura
- Seleção múltipla de linhas
- Copiar/colar (Ctrl+C/Ctrl+V) para edição em massa
- Visualizador de banco de dados integrado
- Monitor de recursos (RAM/CPU) em tempo real
- Barra de progresso para operações longas
- Editor de perfis de regex

**🎯 Funcionalidades:**
- Importar/exportar arquivos JSON e XML
- Tradução manual, por memória e por API
- Aplicar traduções seletivas (linhas selecionadas)
- Gerenciamento de banco de dados
- Configuração de APIs
- Criação e edição de perfis de regex
- Visualização de logs

---

### 🔧 Fluxo de Trabalho do Sistema

1. **🚀 Inicialização:**
   - `main.py` inicia a aplicação
   - `MainWindow` carrega ou cria banco de dados
   - `RegexProfileManager` carrega perfis disponíveis
   - `ResourceMonitor` inicia monitoramento de recursos

2. **📁 Importação de Arquivo:**
   - `FileProcessor` carrega e analisa o arquivo
   - Aplica perfil de regex selecionado
   - Extrai textos traduzíveis
   - Remove duplicatas

3. **🌐 Tradução:**
   - **✍️ Manual:** Usuário edita diretamente na tabela
   - **💾 Memória:** `TranslationMemory` busca traduções existentes
   - **🧠 Inteligente:** `SmartTranslator` aplica padrões aprendidos
   - **🤖 API:** `TranslationAPIManager` usa APIs externas com fallback

4. **💾 Salvamento:**
   - `FileProcessor` aplica traduções ao conteúdo original
   - Cria backup automático
   - Salva arquivo traduzido
   - `TranslationMemory` persiste novas traduções

5. **🛡️ Segurança:**
   - `SecurityValidator` valida todos os inputs
   - `ResourceMonitor` monitora RAM/CPU continuamente
   - `ChunkProcessor` processa grandes volumes em chunks
   - `AutoSaveManager` salva periodicamente

---

### 📊 Diagrama de Dependências

```
main.py
  └─> gui/main_window.py
       ├─> database.py (TranslationMemory)
       ├─> smart_translator.py (SmartTranslator)
       ├─> translation_api.py (TranslationAPIManager)
       ├─> regex_profiles.py (RegexProfileManager)
       ├─> file_processor.py (FileProcessor)
       ├─> security.py (ResourceMonitor, SecurityValidator)
       └─> logger.py (AppLogger)
```

---

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
