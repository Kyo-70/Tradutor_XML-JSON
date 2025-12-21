# 🌐 Tradutor XML-JSON: A Ferramenta Definitiva para Localização de Jogos

## ✨ Visão Geral

O **Tradutor XML-JSON** é uma aplicação desktop robusta e eficiente, desenvolvida em Python e PySide6, projetada para simplificar e acelerar o processo de localização de jogos e mods. Ele permite que tradutores e desenvolvedores gerenciem grandes volumes de texto em formatos XML e JSON, utilizando uma poderosa **Memória de Tradução (SQLite)** e integração com **APIs de Tradução** para garantir consistência e velocidade.

---

## 🚀 Funcionalidades Principais

| Ícone | Funcionalidade | Descrição |
| :---: | :--- | :--- |
| 💾 | **Gerenciamento de Arquivos** | Suporte completo para importação e exportação de arquivos XML e JSON, preservando a estrutura original. |
| 🗄️ | **Memória de Tradução** | Armazena todas as traduções em um banco de dados SQLite, permitindo a reutilização instantânea de textos já traduzidos. |
| 🌐 | **Tradução Automática** | Integração com APIs de tradução (como Google Translate, DeepL, etc.) para tradução em massa com um clique. |
| ⚙️ | **Perfis Regex** | Gerenciamento de expressões regulares para tradução inteligente e preservação de tags e códigos. |
| 🔒 | **Segurança** | Sistema de segurança integrado para proteger dados sensíveis e chaves de API. |

---

## 🌟 Novidades e Melhorias (Versão Atual)

Esta versão traz melhorias significativas na usabilidade e robustez, focando em controle total e eficiência para o tradutor:

### 1. 🛡️ Estabilidade e Controle de Edição

*   **Seleção de Linhas Robusta:** Implementação de um método centralizado (`_get_selected_rows()`) que garante a seleção correta de **qualquer número de linhas**, eliminando falhas em operações de copiar, colar e limpar.
*   **Sistema de Desfazer (Undo - `Ctrl+Z`):** Agora você pode reverter **até 50 ações** (edição manual, colar, limpar, aplicar memória e tradução automática) com um simples `Ctrl+Z`, garantindo total segurança em suas edições.
*   **Atalho para Edição Rápida:** Pressione **`F2`** ou **`Enter`** na linha selecionada para iniciar a edição da célula de tradução imediatamente, sem a necessidade de duplo clique.

### 2. 🔍 Busca e Aplicação Inteligente

*   **Busca por Similaridade (Case-sensitive):** Adicionado um checkbox **"Case-sensitive"** na toolbar e um algoritmo de **Distância de Levenshtein** para encontrar traduções que são bem parecidas, mas diferem em algum caractere ou número, facilitando a identificação de erros sutis.
*   **Controle de Auto-preenchimento:** O novo checkbox **"Auto-preencher"** permite que você decida se a memória de tradução deve aplicar as traduções automaticamente ou apenas indicar quantas foram encontradas, dando-lhe controle total sobre o processo.

### 3. ⌨️ Guia de Atalhos Interativo

*   Adicionado um botão **"Atalhos"** na toolbar e a função **`F1`** para abrir um guia visual completo.
*   O guia exibe todos os atalhos organizados por categorias (Edição, Arquivo, Tradução, etc.) com descrições detalhadas.

| Categoria | Atalho | Ação |
| :---: | :--- | :--- |
| ✏️ Edição | `Ctrl+Z` | Desfazer última ação |
| | `F2` / `Enter` | Editar linha selecionada |
| | `Ctrl+C` | Copiar linhas selecionadas |
| | `Ctrl+V` | Colar traduções |
| | `Delete` | Limpar traduções selecionadas |
| 🌐 Tradução | `F5` | Traduzir automaticamente via API |
| ❓ Ajuda | `F1` | Mostrar Guia de Atalhos |

---

## 🛠️ Instalação e Uso

### Pré-requisitos

*   Python 3.x
*   Git

### 1. Clonar o Repositório

```bash
git clone https://github.com/Kyo-70/Tradutor_XML-JSON.git
cd Tradutor_XML-JSON
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Executar a Aplicação

```bash
python src/main.py
```

---

## 🤝 Contribuição

Contribuições são sempre bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests* com melhorias, correções de bugs ou novas funcionalidades.

---

<p align="center">Desenvolvido com 💙 por Manus AI</p>
