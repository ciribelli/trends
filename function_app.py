import logging
import os
import requests
import azure.functions as func

import grok

app = func.FunctionApp()


def send_wapp_msg(phone_number_id, from_number, coletor, wapp_token):
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages?access_token={wapp_token}"
    payload = {
        "messaging_product": "whatsapp",
        "to": from_number,
        "text": {"body": coletor},
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        logging.info(f"WhatsApp API Status code: {response.status_code}")
        logging.info(f"WhatsApp API Response: {response.text}")
    except Exception as e:
        logging.exception(f"Exception raised while sending WhatsApp message: {e}")


@app.timer_trigger(
    schedule="0 0 9 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=False,
)
def etl_func(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Executando envio de mensagem via WhatsApp...")
    
    try:
        wapp_token = os.getenv("WHATSAPP_TOKEN")
        grok_token = os.getenv("XAI_API_KEY")
        phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "233405413182343")
        from_number = os.getenv("WHATSAPP_PHONE_NUMBER", "5521983163900")

        resultado_busca = grok.consulta_grok(grok_token)
        send_wapp_msg(phone_number_id, from_number, resultado_busca, wapp_token)
    except Exception as e:
        logging.exception(f"Erro na execução da etl_func: {e}")


@app.timer_trigger(
    schedule="0 * * * * *",
    arg_name="verificacaoTimer",
    run_on_startup=False,
    use_monitor=False,
)
def verificar_compromissos(verificacaoTimer: func.TimerRequest) -> None:
    if verificacaoTimer.past_due:
        logging.warning("The timer is past due!")

    logging.info("Executando verificação de compromissos no Heroku...")
    
    heroku_url = os.getenv("HEROKU_APP_URL")
    cron_secret = os.getenv("CRON_SECRET")
    
    if not heroku_url:
        logging.error("HEROKU_APP_URL environment variable is not set.")
        return

    url = f"{heroku_url.rstrip('/')}/trigger_reminders"
    headers = {}
    if cron_secret:
        headers["Authorization"] = cron_secret

    try:
        response = requests.post(url, headers=headers, timeout=30)
        logging.info(f"Status code Heroku: {response.status_code}")
        if response.ok:
            logging.info(f"Lembretes processados com sucesso: {response.text}")
        else:
            logging.error(f"Erro retornado pelo Heroku: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Falha de conexão com o Heroku para processamento de lembretes: {e}")

@app.timer_trigger(
    schedule="0 */20 * * * *",
    arg_name="ml_inferenciaTimer",
    run_on_startup=False,
    use_monitor=False,
)
def realizar_inferencia(ml_inferenciaTimer: func.TimerRequest) -> None:
    if ml_inferenciaTimer.past_due:
        logging.warning("The timer is past due!")

    url = "https://passisml.onrender.com/gera_inferencia_agendada"

    try:
        logging.info("Chamando endpoint de inferência no Render...")
        response = requests.post(url, timeout=30)

        logging.info(f"Status code: {response.status_code}")

        if response.ok:
            logging.info(f"Resposta da inferência: {response.json()}")
        else:
            logging.error(f"Erro na inferência: {response.text}")

    except Exception as e:
        logging.exception(f"Falha ao chamar endpoint de inferência: {e}")


@app.timer_trigger(
    schedule="0 0 12 * * SUN",
    arg_name="weeklyReportTimer",
    run_on_startup=False,
    use_monitor=True,
)
def relatorio_semanal_trigger(weeklyReportTimer: func.TimerRequest) -> None:
    if weeklyReportTimer.past_due:
        logging.warning("The weekly report timer is past due!")

    logging.info("Executando geração e envio do relatório semanal...")
    
    heroku_url = os.getenv("HEROKU_APP_URL")
    cron_secret = os.getenv("CRON_SECRET")
    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "233405413182343")
    recipient = os.getenv("WHATSAPP_PHONE_NUMBER", "5521983163900")
    
    if not heroku_url:
        logging.error("HEROKU_APP_URL environment variable is not set.")
        return

    url = f"{heroku_url.rstrip('/')}/v1/weekly-report"
    headers = {}
    if cron_secret:
        headers["Authorization"] = cron_secret

    payload = {
        "phone_number_id": phone_number_id,
        "recipient": recipient
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        logging.info(f"Status code Heroku: {response.status_code}")
        if response.ok:
            logging.info(f"Relatório semanal processado com sucesso: {response.text}")
        else:
            logging.error(f"Erro retornado pelo Heroku ao processar relatório semanal: {response.status_code} - {response.text}")
    except Exception as e:
        logging.exception(f"Falha de conexão com o Heroku para processamento do relatório semanal: {e}")