import logging
import azure.functions as func
import os

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 8-20 * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def etl_func(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    wapp_token = os.getenv('WHATSAPP_TOKEN')
    logging.info('Teste de leitura variável de ambiente')
    logging.info(wapp_token)