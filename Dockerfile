# Dockerfile
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependência
COPY app/requirements.txt .


RUN apt-get update && apt-get install -y build-essential libffi-dev python3-dev

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt


# Copia o restante da aplicação
COPY . .

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para iniciar o servidor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
