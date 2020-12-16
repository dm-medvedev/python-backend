1. Включи сервер ./server.py config
2. Включи клиент ./client.py game_url.txt 10
3. Жди возможно долго
4. Убей сервер прпавильно: 
> ps aux | grep server.py
> kill -SIGUSR1 PID