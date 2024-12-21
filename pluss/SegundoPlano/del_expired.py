import asyncio
from datetime import datetime, timedelta
import re
from database.connect_to_db import connect_to_db  # Asegúrate de que connect_to_db esté definido

# Intervalo de actualización en segundos
update_interval = 1

async def update_viped():
    while True:
        conn = connect_to_db()
        cursor = conn.cursor()

        cursor.execute("SELECT id, dias, expiracion, rango FROM Users")
        users = cursor.fetchall()

        for user in users:
            user_id, days, expiration, rank = user

            if rank.lower() not in ['free user', 'premium']:
                if days >= 1:
                    if not expiration or expiration == "":
                        expiration = "0 días 23 horas 59 minutos 59 segundos" if days == 1 else f"{days-1} días 23 horas 59 minutos 59 segundos"
                        cursor.execute("UPDATE Users SET expiracion = %s WHERE id = %s", (expiration, user_id))

                    match = re.match(r"(\d+) días (\d+) horas (\d+) minutos (\d+) segundos", expiration)
                    if match:
                        days_left, hours_left, minutes_left, seconds_left = map(int, match.groups())

                        if days_left != days - 1:
                            days_left = days - 1
                            hours_left = 23
                            minutes_left = 59
                            seconds_left = 59

                        if seconds_left > 0:
                            seconds_left -= 1
                        elif minutes_left > 0:
                            minutes_left -= 1
                            seconds_left = 59
                        elif hours_left > 0:
                            hours_left -= 1
                            minutes_left = 59
                            seconds_left = 59
                        elif days_left > 0:
                            days_left -= 1
                            hours_left = 23
                            minutes_left = 59
                            seconds_left = 59

                        if days_left == 0 and hours_left == 0 and minutes_left == 0 and seconds_left == 0:
                            cursor.execute("UPDATE Users SET expiracion = '', dias = dias - 1 WHERE id = %s", (user_id,))
                        else:
                            new_expiration = f"{days_left} días {hours_left} horas {minutes_left} minutos {seconds_left} segundos"
                            cursor.execute("UPDATE Users SET expiracion = %s WHERE id = %s", (new_expiration, user_id))

                elif days == 0 and expiration != "":
                    cursor.execute("UPDATE Users SET expiracion = '' WHERE id = %s", (user_id,))

            else:  # Caso de Premium
                if days >= 1:
                    cursor.execute("UPDATE Users SET rango = 'Premium' WHERE id = %s", (user_id,))

                    if not expiration or expiration == "":
                        expiration = "0 días 23 horas 59 minutos 59 segundos" if days == 1 else f"{days-1} días 23 horas 59 minutos 59 segundos"
                        cursor.execute("UPDATE Users SET expiracion = %s WHERE id = %s", (expiration, user_id))

                    match = re.match(r"(\d+) días (\d+) horas (\d+) minutos (\d+) segundos", expiration)
                    if match:
                        days_left, hours_left, minutes_left, seconds_left = map(int, match.groups())

                        if days_left != days - 1:
                            days_left = days - 1
                            hours_left = 23
                            minutes_left = 59
                            seconds_left = 59

                        if seconds_left > 0:
                            seconds_left -= 1
                        elif minutes_left > 0:
                            minutes_left -= 1
                            seconds_left = 59
                        elif hours_left > 0:
                            hours_left -= 1
                            minutes_left = 59
                            seconds_left = 59
                        elif days_left > 0:
                            days_left -= 1
                            hours_left = 23
                            minutes_left = 59
                            seconds_left = 59

                        if days_left == 0 and hours_left == 0 and minutes_left == 0 and seconds_left == 0:
                            cursor.execute("UPDATE Users SET rango = 'Free user', expiracion = '', dias = dias - 1 WHERE id = %s", (user_id,))
                        else:
                            new_expiration = f"{days_left} días {hours_left} horas {minutes_left} minutos {seconds_left} segundos"
                            cursor.execute("UPDATE Users SET expiracion = %s WHERE id = %s", (new_expiration, user_id))

                elif days == 0 and expiration != "":
                    cursor.execute("UPDATE Users SET rango = 'Free user', expiracion = '' WHERE id = %s", (user_id,))

        conn.commit()
        conn.close()

        await asyncio.sleep(update_interval)

# Ejecutar el bucle de actualización
loop = asyncio.get_event_loop()
loop.create_task(update_viped())
loop.run_forever()
