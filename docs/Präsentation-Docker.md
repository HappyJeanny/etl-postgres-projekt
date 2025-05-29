# Kurzpräsentation: Einstieg in Docker mit nginx (für Anfänger)

## Dauer: Max. 10 Minuten

---

## 1. Was ist Docker?

* Tool zur **Containerisierung** von Anwendungen
* Container = leichtgewichtige, isolierte Umgebungen (wie "Mini-VMs")
* Vorteil: Alles, was eine Anwendung braucht, ist enthalten: Code, Laufzeit, Bibliotheken

---

## 2. Warum Docker verwenden?

* **"It works on my machine"**-Problem wird gelöst
* Einfaches Deployment auf jedem System (egal ob Windows, Mac, Linux)
* Automatisierung durch Dockerfiles & docker-compose

---

## 3. Beispiel: nginx Webserver in Docker starten

### Ziel:

* Eine einfache `index.html` über einen nginx Webserver anzeigen

### Schritt 1: Projektstruktur in VS Code

```
my-nginx/
├── docker-compose.yml
└── html/
    └── index.html
```

### Schritt 2: Inhalt der Dateien

**docker-compose.yml**

```yaml
dversion: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"
    volumes:
      - ./html:/usr/share/nginx/html
```

**html/index.html**

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Hello Docker</title>
  </head>
  <body>
    <h1>It works! Docker + nginx</h1>
  </body>
</html>
```

### Schritt 3: Docker starten

```bash
docker-compose up -d
```

* Browser öffnen: `http://localhost:8080`
* Webseite sichtbar ✅

---

## 4. Kontrolle über Docker Desktop

* nginx Container erscheint als **"web"** unter **Containers**
* Image ist unter **Images** sichtbar: `nginx:latest`

---

## 5. Aufräumen

```bash
docker-compose down
```

---

## 6. Fazit

* Docker hilft beim schnellen Bereitstellen und Testen von Services
* Sehr nützlich für Webserver, Datenbanken, ETL-Pipelines
* Ideal für reproducible Environments & DevOps

---

**Tipp**: Dieses Beispiel kann leicht für PostgreSQL oder andere Tools erweitert werden. Siehe: https://hub.docker.com/search?badges=official
