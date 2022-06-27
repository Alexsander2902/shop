# Sistema Shop

## Este sistema possúi:

* API REST em Python 3
* Testes Unitários e Funcionais com pytest
* Banco de dados MariaDB
* Nginx
* Docker com Dockerfile e docker-compose.yml
* Frontend em React
* Honeypot

## Este sistema não possúi:

* Jsonschema
* Documentação swagger
* ORM (SQLAlchemy)
* CI/CD no Google Cloud
* Cache Redis
* Script para limpeza de arquivos no projeto

## Considerações para execução do sistema

```shell
# Criação do ambiente
pip install virtualenv
virtualenv env
# Ativar biblioteca
# Windows
env\Scripts\activate
# Linux
source env\bin\activate
# Acessar pasta da aplicação Python
cd dir
# Instalação das biliotecas 
# (Há inconsistências entre plataformas)
pip install -r requirements.txt
#if Windows, install mysql-connector-python==8.0.26
# Executar projeto
python main.py
```
## Considerações para execução do sistema (com Docker)

```shell
#docker-compose up -d --build
docker-compose -f docker-compose-prd.yml up -d --build
docker-compose -f docker-compose-hml.yml up -d --build
```

**Lembre-se de adicionar os arquivos com informação crítica (.gitignore) no projeto**

**JAMAIS INSIRA CREDENCIAIS DE ACESSO OU INFORMAÇÕES SENSÍVEIS NO REPOSITÓRIO**

## Considerações para manutenção da API

```shell
# Tests
#unit test
pytest tests/test_unittest.py --durations=0 -vvl --showlocals
#mutation test
mutmut run --paths-to-mutate=app/utils --tests-dir=tests/ --runner="pytest tests/test_unittest.py --durations=0 -vvl --showlocals" --no-backup
#pytest tests/test_unittest.py --mutate --mutagen-stats #no details
#mut.py --target app.utils.util --unit-test tests.test_unittest -m #dont work
#mut.py --target app.utils.util --unit-test tests.test_unittest #dont work
#functional test
pytest tests/test_pytest.py --durations=0 -vvl --showlocals -n 16
# Security checks
bandit -r app
# Logic checks
pyflakes app
mypy app
# Logic and Style checks
pylint app
flake8 app
pytest --cov=app .
pytest --cov=. app/
```

## Comentários

Utilizar o Gitflow no processo de versionamento do projeto

Utilize o editor de texto que desejar para manipulação do projeto (Notepad++, VSC, Sublime...)
