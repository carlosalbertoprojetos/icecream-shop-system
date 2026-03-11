# Sistema para gestão de sorveteria - IceCream Shop System

Este projeto é uma **aplicação web baseada em Django** para gerenciar uma sorveteria, incluindo funcionalidades de gerenciamento de produtos, pedidos, clientes e mais.

## Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- Python (>= 3.8)
- Django (4.1.4)
- Um gerenciador de ambiente virtual como `virtualenv` ou `venv`
- PostgreSQL ou SQLite (dependendo da configuração)
- Git (para controle de versão)


## pytest-cov

Para controlar a cobertura de testes dos apps foi utilizado o pytest-cov, uma extensão (plugin) do framework de teste Pytest que é usado para medir a cobertura de código dos testes automatizados em Python. Ele ajuda a determinar quais partes do código-fonte do projeto estão sendo testadas pelos testes e a calcula a porcentagem de cobertura de código.

## Passos de Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/carlosalbertoprojetos/sorveteria.git
cd sorveteria
```

### 2. Criar um ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` no diretório raiz do projeto com as configurações necessárias, como as do banco de dados. Exemplo:

```
SECRET_KEY=sua_chave_secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sua_url_do_banco_de_dados
```

### 5. Aplicar as Migrações

```bash
python manage.py migrate
```

### 6. Criar um Superusuário

```bash
python manage.py createsuperuser
```

### 7. Executar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

Agora você pode acessar a aplicação em `http://127.0.0.1:8000/` no seu navegador.

## Dependências Principais

- **Django 4.1.4**: Framework principal usado para construir a aplicação.
- **Django REST Framework**: Para criação de APIs.
- **Pillow**: Para manipulação de imagens.
- **django-cors-headers**: Para tratar CORS nas APIs.
- **django-session-timeout**: Para gerenciar o tempo de expiração de sessões.
- **python-dotenv**: Para gerenciar variáveis de ambiente.

A lista completa das dependências pode ser encontrada no [requirements.txt](./requirements.txt)【12†source】.

## Funcionalidades

1. **Autenticação de Usuários**: Usuários podem se registrar, fazer login e gerenciar suas contas.
2. **Gerenciamento de Produtos**: Adicionar, atualizar e excluir produtos de sorvete.
3. **Gerenciamento de Pedidos**: Fazer, acompanhar e gerenciar pedidos de clientes.
4. **Gerenciamento de Clientes**: Acompanhar detalhes e preferências dos clientes.
5. **API REST**: Expor os dados da aplicação por meio de uma API REST para integração com outros sistemas.
6. **Tempo de Sessão**: Desloga automaticamente os usuários após um período de inatividade.

