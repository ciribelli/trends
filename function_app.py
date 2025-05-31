import logging
import azure.functions as func
import os
import requests
import grok

app = func.FunctionApp()

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

@app.timer_trigger(schedule="0 0 9-9 * * *", arg_name="myTimer", run_on_startup=False, use_monitor=False)
def etl_func(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    wapp_token = os.getenv('WHATSAPP_TOKEN')
    grok_token = os.getenv('XAI_API_KEY')
    logging.info('Executando envio de mensagem via WhatsApp...')
    resultado_busca = grok.consulta_grok(grok_token)
    send_wapp_msg("233405413182343","5521983163900",resultado_busca, wapp_token)
