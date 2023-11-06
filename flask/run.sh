docker-compose exec flask flask db upgrade
docker-compose exec flask python /app/src/commands/add_user.py
docker-compose exec flask python /app/src/commands/pop.py