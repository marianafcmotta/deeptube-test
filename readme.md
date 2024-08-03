# Anúncios Transparency

Esta é uma aplicação Python que utiliza FastAPI e Selenium para buscar anúncios de transparência do Google. 

## Requisitos

- Python 3.10.0
- Google Chrome
- ChromeDriver

## Instalação

1. Clone este repositório:

    ```sh
    git clone <URL_DO_REPOSITORIO>
    cd <NOME_DO_DIRETORIO>
    ```

2. Crie um ambiente virtual:

    ```sh
    python -m venv venv
    ```

3. Ativando o ambiente virtual

    No Linux/MacOS, ative o ambiente virtual com:

    ```sh
    source venv/bin/activate
    ```

    No Windows, ative o ambiente virtual com:

    ```sh
    venv\Scripts\activate
    ```

4. Instale as dependências:

    ```sh
    pip install -r requirements.txt
    ```

5. Baixe e descompacte o ChromeDriver para a pasta do projeto (se ainda não fez):

    - [Download do ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

    No Linux/MacOS, use:

    ```sh
    unzip chromedriver_linux64.zip
    ```

    No Windows, você pode usar um programa de descompactação como o WinRAR ou 7-Zip para extrair o `chromedriver.exe` na pasta do projeto.

## Uso

1. Execute a aplicação:

    ```sh
    python main.py
    ```

2. Envie uma solicitação POST para o endpoint `localhost:8000/announcements` com o seguinte corpo JSON:

    ```json
    {
      "keys": ["meusucesso.com", "BANCO SAFRA S/A", "hostgator.com"]
    }
    ```

## Estrutura do Projeto
```
backend/
│
├── .venv/
├── pycache/
├── chromedriver_linux64.zip
├── LICENSE.chromedriver
├── main.py
├── models.py
├── requirements.txt
└── README.md
```

- **main.py**: Contém a lógica principal da aplicação FastAPI.
- **models.py**: Contém a definição dos modelos de dados usados na aplicação.
- **requirements.txt**: Lista de dependências da aplicação.
- **chromedriver_linux64.zip**: Arquivo zip do ChromeDriver (deve ser descompactado antes de usar).

## Dependências

As dependências da aplicação estão listadas no arquivo `requirements.txt`. As principais são:

- `fastapi`: Framework web rápido e moderno para construir APIs com Python 3.7+ baseado em padrões do Python.
- `uvicorn`: Um servidor ASGI para correr as aplicações ASGI, tais como FastAPI.
- `selenium`: Um módulo que permite a automação de navegadores web.
