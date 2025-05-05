import logging
import requests
import azure.functions as func
import os

app = func.FunctionApp()

def send_wapp_msg(phone_number_id, from_number, coletor, wapp_token):
    fb_url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages?access_token={wapp_token}"
    payload = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "text": {"body": coletor}
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(fb_url, json=payload, headers=headers)
    # print(response.content, "content")
    return response

@app.timer_trigger(schedule="0 0 14-20 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def etl_func(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('Log de teste')

    wapp_token = os.environ.get('WHATSAPP_TOKEN')
    logging.info(wapp_token)
    logging.info('Rodando a aplicação!')
    a = send_wapp_msg("233405413182343","5521983163900","_mensagem teste api response pela Azure!_", wapp_token)
    logging.info(a.text)







