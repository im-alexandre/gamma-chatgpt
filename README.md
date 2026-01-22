Perfeito. Segue um **README mínimo**, mas **bem organizado**, com **demo**, **visão geral**, **como usar** e **documentação suficiente** para alguém entender o projeto sem te perguntar nada.

Pode subir **exatamente assim** no GitHub.

---

````markdown
# AI Slides Pipeline (ChatGPT + Gamma + Python)

Pipeline simples para **gerar apresentações automaticamente** a partir de texto estruturado, usando **Python**, **ChatGPT** e **Gamma**.

A ideia central é separar responsabilidades:
- o humano cria o conteúdo,
- o código organiza,
- a IA estrutura,
- a ferramenta visual cuida do design.

---

## 🎯 Objetivo

Reduzir drasticamente o tempo gasto criando apresentações, aulas, cursos e palestras, automatizando:
- estruturação de slides
- organização de ideias
- consistência visual

Tudo isso sem perder controle sobre o conteúdo.

---

## 🧠 Como funciona (visão geral)

1. O conteúdo é escrito em **Markdown**  
2. Arquivos de apoio (ex: DOCX) são anexados via API  
3. Um script em **Python** chama a API do ChatGPT  
4. A IA gera os **cards estruturados**  
5. O resultado é enviado ao **Gamma**, que gera a apresentação visual

O humano entra apenas para ajustes finais, quando necessário.

---

## 📂 Estrutura do projeto

```text
.
├── prompt_gpt.md        # Prompt usado para geração dos cards
├── gera_cards.py        # Script principal em Python
├── cards/               # Cards exportados (um por apresentação)
├── exemplo/
│   ├── conteudo.docx
│   ├── rot.docx
│   └── cards.md
└── README.md
````

---

## ▶️ Demo rápida

Exemplo de entrada (`cards.md` gerado):

```markdown
# Automatizando a criação de apresentações

---

## O problema
Criar apresentações consome tempo e energia...

---

## A solução
Separar conteúdo de visual usando automação...
```

Esse arquivo pode ser **colado diretamente no Gamma**, gerando um carrossel ou apresentação em segundos.

---

## 🚀 Como usar

### 1. Pré-requisitos

* Python 3.10+
* Chave de API configurada:

```bash
export OPENAI_API_KEY="sua_chave_aqui"
```

### 2. Executar o pipeline

```bash
python gera_cards.py --root .
```

Ou apenas uma pasta específica:

```bash
python gera_cards.py --only dic_docx --force
```

---

## ⚙️ Personalização

* Ajuste o comportamento alterando o arquivo `prompt_gpt.md`
* O número de cards, nível de detalhe e estilo vêm **do prompt**
* O pipeline foi pensado para ser simples, previsível e modificável

---

## 🧩 Filosofia do projeto

* Automação > perfeição
* Pipeline confiável > resultado ideal
* IA como **alavanca**, não substituta
* Intervenção humana apenas onde agrega valor

---

## 📌 Observações

* O projeto **não tenta resolver tudo automaticamente**
* Revisões finais são feitas diretamente na ferramenta visual (ex: Gamma)
* O foco é produtividade, não geração “mágica” de conteúdo

---

## 📄 Licença

Uso livre para fins educacionais e experimentais.

