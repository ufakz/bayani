FROM python:3.11.5-slim

WORKDIR /app
COPY . ./
ENV OPENAI_API_KEY=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


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common 

RUN pip3 install --no-cache-dir --force-reinstall -r requirements.txt

EXPOSE 8501


EXPOSE 50051
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]