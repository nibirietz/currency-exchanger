docker rm -f currency-exchanger 2>/dev/null || true
docker run -d --name currency-exchanger -p 8080:8080 currency-exchanger
