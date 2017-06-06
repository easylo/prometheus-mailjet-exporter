
```
version: '2'
services:
  mailjet-exporter:
    build: .
    ports:
      - 9187:9187
    environment:
      - BIND_PORT=9187
      - APIKEY_PRIVATE=YOUR_API_KEY_HERE
      - APIKEY_PUBLIC=YOUR_API_KEY_HERE
```