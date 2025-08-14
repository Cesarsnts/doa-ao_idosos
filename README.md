  # instruções para rodar o codigo
  
1. baixe os arquivos ou clone o repositorio
   
2. criar ambiente virtual e ativar
     python -m venv venv
     ( Windows )
     venv\Scripts\activate
     ( Linux/Mac )
     source venv/bin/activate
   
3.Instale as dependências do projeto
      pip install -r requirements.txt

4.Inicialize o banco de dados
     python iniciar_banco.py
     
5.Execute a aplicação Flask em modo de desenvolvimento
     flask run --debug
     
6. acesse o localhost na barra de navegaçãp
     localost:5000

  # Dependências

Python 3.x

Flask
#flask-login

SQLite3

