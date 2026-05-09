FROM eclipse-temurin:8-jre-focal

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y wget unzip && rm -rf /var/lib/apt/lists/*

# Скачиваем BMP (одной строкой с полной ссылкой)
RUN wget https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-2.1.4/browsermob-proxy-2.1.4-bin.zip \
    && unzip browsermob-proxy-2.1.4-bin.zip \
    && rm browsermob-proxy-2.1.4-bin.zip

WORKDIR /browsermob-proxy-2.1.4/bin

# Используем JSON-формат для CMD. 
# Чтобы использовать переменные окружения, вызываем через sh
CMD ["sh", "-c", "./browsermob-proxy -port ${API_PORT} -proxyPortRange ${PROXY_RANGE}"]