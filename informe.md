# Ej1.1
Acá veo dos opciones

## Jinja
Hacer un template de Jinja y correrlo a traves de un container para generar el yml en el root del directorio.

## Scale
```bash
$ grep -irl "CLI_ID" .
./docker-compose-dev.yaml
```

Nos dice que `CLI_ID` no es usado en ningún lugar. Genial, entonces hacemos:
```
