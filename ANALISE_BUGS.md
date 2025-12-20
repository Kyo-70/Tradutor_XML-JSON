# Análise de Bugs - Tradutor XML-JSON

## Data da Análise
19 de dezembro de 2025

## Bugs Identificados

### 1. Bug nas Linhas Selecionáveis (Reportado pelo Usuário)

**Descrição:** Quando o usuário seleciona múltiplas linhas (por exemplo, 4 linhas), mas algumas dessas linhas já possuem tradução, ao realizar a operação de colar (Ctrl+V), o sistema não cola nas linhas selecionáveis corretamente e considera apenas a última linha.

**Localização:** `src/gui/main_window.py`, função `paste_rows()` (linhas 2000-2120)

**Problema Identificado:** 
- A função atual itera sobre as linhas selecionadas sequencialmente (`for i, row in enumerate(selected_rows)`)
- Ela mapeia diretamente `clipboard_lines[i]` para `selected_rows[i]`
- Se uma linha selecionada já tem tradução, ela ainda é considerada no mapeamento
- Isso causa desalinhamento entre as traduções coladas e as linhas que realmente precisam de tradução

**Impacto:** Médio - Afeta a usabilidade ao trabalhar com seleções mistas de linhas traduzidas e não traduzidas

### 2. Falta de Salvamento de Dimensionamento da Tela (Reportado pelo Usuário)

**Descrição:** O sistema não salva as configurações de dimensionamento da tela (tamanho da janela, posição das colunas, etc.). Quando o usuário reabre o programa, todas as configurações visuais são perdidas.

**Localização:** `src/gui/main_window.py`

**Problema Identificado:**
- Existe uma constante `QSettings` configurada (linhas 74-78)
- Há geometria padrão definida (linhas 68-71)
- Mas não há implementação de salvamento/carregamento de:
  - Tamanho e posição da janela
  - Largura das colunas da tabela
  - Estado de divisores (splitters)
  - Outras preferências de UI

**Impacto:** Médio - Afeta a experiência do usuário que precisa reconfigurar a interface toda vez

### 3. Possíveis Bugs Adicionais Identificados

#### 3.1. Validação de Null Inconsistente
**Localização:** Várias partes do código
**Descrição:** Embora haja verificações de null em alguns lugares (linhas 2086-2107), pode haver outros locais onde items da tabela são acessados sem verificação

#### 3.2. Auto-ajuste de Altura Pode Ser Custoso
**Localização:** `_auto_adjust_row_heights()` chamado após paste (linha 2114)
**Descrição:** Se houver muitas linhas, o auto-ajuste pode ser lento

## Prioridades de Correção

1. **Alta:** Bug das linhas selecionáveis (afeta funcionalidade principal)
2. **Alta:** Salvamento de dimensionamento da tela (melhoria de UX significativa)
3. **Média:** Validação de null inconsistente
4. **Baixa:** Otimização de auto-ajuste

## Próximos Passos

1. Corrigir bug das linhas selecionáveis
2. Implementar sistema de salvamento de configurações de UI
3. Testar as correções
4. Commit e push das alterações
