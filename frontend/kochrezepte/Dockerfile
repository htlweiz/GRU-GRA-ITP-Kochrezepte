# Basis-Image mit Node.js
FROM node:18

# Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere package.json und package-lock.json
COPY package*.json ./

# Installiere Abhängigkeiten
RUN npm install

# Kopiere den Rest des Codes
COPY . .

EXPOSE 5173

# Startbefehl für den Entwicklungsmodus
CMD ["npm", "run", "dev", "--host"]
