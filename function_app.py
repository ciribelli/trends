import logging
import azure.functions as func
import os
import requests
from datetime import datetime, timedelta
import psycopg2

app = func.FunctionApp()


# Função para conectar ao banco de dados
def connect_to_db():
    connection = psycopg2.connect(
        host="passisdb.postgres.database.azure.com",
        database="postgres",
        port=5432,
        user="passisdb",
        password = os.getenv('password')
    )
    return connection

# Função para contar check-ins
def count_checkins():
    connection = connect_to_db()
    cursor = connection.cursor()

    # Calcular o início da semana (domingo)
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday() + 1)  # domingo

    # Consulta SQL para contar check-ins
    query = """
    SELECT
        SUM(CASE WHEN checkin = 'academia' THEN 1 ELSE 0 END) AS academia_count,
        SUM(CASE WHEN checkin = 'terco' THEN 1 ELSE 0 END) AS terco_count
    FROM public.checkins
    WHERE "data" >= %s
    """
    
    cursor.execute(query, (start_of_week,))
    result = cursor.fetchone()

    # Fechar a conexão
    cursor.close()
    connection.close()

    return result


def send_wapp_msg(phone_number_id, from_number, coletor, wapp_token):
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages?access_token={wapp_token}"
    payload = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "text": {"body": coletor}
    }
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    logging.info(f"Status code: {response.status_code}")
    logging.info(f"Response: {response.text}")

@app.timer_trigger(schedule="0 0 8-20 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def etl_func(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    # Chama a função de contagem de check-ins
    counts = count_checkins()
    resumo_semana = (f"Academia: {counts[0]}, Terço: {counts[1]}")
    logging.info(resumo_semana)
    # Envia a mensagem via WhatsApp
    phone_number_id = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    phone_number = os.getenv('WHATSAPP_PHONE_NUMBER')
    wapp_token = os.getenv('WHATSAPP_TOKEN')
    logging.info('Executando envio de mensagem via WhatsApp...')
    send_wapp_msg(phone_number_id,phone_number,resumo_semana, wapp_token)
