🌐 Síťová konfigurace (Izolovaná LAN)

    IP adresa serveru: 10.10.10.1 (Příklad – uprav dle reality) 

    Maska sítě: 255.255.255.0 (/24) 

    DHCP Scope: 10.10.10.100 – 10.10.10.200 

    DHCP Option 006 (DNS): IP adresa mého serveru 

    DNS Zóna: skola.test 

    DNS A-záznam: jmenoprijmeni.skola.test (např. novakpetr.skola.test) -> IP serveru 

🐳 Aplikace a Docker

    Technologie: Python (Flask) v Docker kontejneru 

    Publikovaný port: 8081:8081 (TCP) 

    Firewall pravidlo (Windows): netsh advfirewall firewall add rule name="LoLAPI" dir=in action=allow protocol=TCP localport=8081 

    Příkaz pro spuštění: docker compose up -d 

🤖 Lokální LLM (AI prvek)

    Model: Ollama (model llama3.2:1b) běžící na CPU 

    API adresa: http://localhost:11434/api 

    Popis: Aplikace bere vstup od uživatele a přes API dotazuje lokální model pro doporučení herního buildu v LoL.

🛠️ Testovací endpointy a ukázkový CURL

    GET /ping: Vrací "pong" pro ověření dostupnosti.

    GET /status: Vrací JSON s aktuálním časem a jménem autora.

    POST /ai: Hlavní funkce pro radu s buildem.

Ukázkový curl pro test z klienta:
Bash

curl -X POST http://jmenoprijmeni.skola.test:8081/ai -H "Content-Type: application/json" -d "{\"prompt\":\"Proti me je Ashe a Mundo, ja jsem Ahri. Co mam stavet?\"}"

🔍 Troubleshooting (Kdyby něco...)

    Pokud se klient nepřipojí, zkontroluj, zda běží Docker kontejner a port naslouchá na 0.0.0.0.

    Pokud nefunguje překlad jména, ověř v příkazovém řádku klienta pomocí nslookup jmenoprijmeni.skola.test.

    Pokud AI neodpovídá, ujisti se, že je spuštěna služba Ollama a model je stažený.
