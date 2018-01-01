import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '485533690:AAHYXUtAohyuRxRKNFueQtqXYm81TP_Ij1E'
WEBHOOK_URL = 'https://1aec9aa1.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
    	'init',
        'start',
        'best',
        'bestRes',
        'all',
        'all_bank',
        'allRes',
        'calc',
        'calc_best_sell',
        'calc_best_buy',
        'calc_best_sellRes',
        'calc_best_buyRes',
        'calc_spec_sell',
        'calc_spec_buy',
        'calc_spec_sell_bank',
        'calc_spec_buy_bank',
        'calc_spec_sellRes',
        'calc_spec_buyRes',
        'about',
        'help',
        'explain',
        'info'
    ],
    transitions=[
        {    # * -> start
            'trigger': 'advance',
            'source': '*',
            'dest': 'start',
            'conditions': 'is_going_to_start'
        },
        {   # start -> best
            'trigger': 'advance',
            'source': 'start',
            'dest': 'best',
            'conditions': 'is_going_to_best'
        },
        {
            'trigger': 'advance',
            'source': 'best',
            'dest': 'bestRes',
            'conditions': 'is_going_to_bestRes'
        },
        {   # start -> all
            'trigger': 'advance',
            'source': 'start',
            'dest': 'all',
            'conditions': 'is_going_to_all'
        },
        {
            'trigger': 'advance',
            'source': 'all',
            'dest': 'all_bank',
            'conditions': 'is_going_to_all_bank'
        },
        {
            'trigger': 'advance',
            'source': 'all_bank',
            'dest': 'allRes',
            'conditions': 'is_going_to_allRes'
        },
        {   # start -> calc
            'trigger': 'advance',
            'source': 'start',
            'dest': 'calc',
            'conditions': 'is_going_to_calc'
        },
        {   # best calc
            'trigger': 'advance',
            'source': 'calc',
            'dest': 'calc_best_sell',
            'conditions': 'is_going_to_best_sell'
        },
        {
            'trigger': 'advance',
            'source': 'calc',
            'dest': 'calc_best_buy',
            'conditions': 'is_going_to_best_buy'
        },
        {
            'trigger': 'advance',
            'source': 'calc_best_sell',
            'dest': 'calc_best_sellRes',
            'conditions': 'is_going_to_best_sellRes'
        },
        {
            'trigger': 'advance',
            'source': 'calc_best_buy',
            'dest': 'calc_best_buyRes',
            'conditions': 'is_going_to_best_buyRes'
        },
        {   # spec calc
            'trigger': 'advance',
            'source': 'calc',
            'dest': 'calc_spec_sell',
            'conditions': 'is_going_to_spec_sell'
        },
        {
            'trigger': 'advance',
            'source': 'calc',
            'dest': 'calc_spec_buy',
            'conditions': 'is_going_to_spec_buy'
        },
        {
            'trigger': 'advance',
            'source': 'calc_spec_sell',
            'dest': 'calc_spec_sell_bank',
            'conditions': 'is_going_to_spec_sell_bank'
        },
        {
            'trigger': 'advance',
            'source': 'calc_spec_buy',
            'dest': 'calc_spec_buy_bank',
            'conditions': 'is_going_to_spec_buy_bank'
        },
        {
            'trigger': 'advance',
            'source': 'calc_spec_sell_bank',
            'dest': 'calc_spec_sellRes',
            'conditions': 'is_going_to_spec_sellRes'
        },
        {
            'trigger': 'advance',
            'source': 'calc_spec_buy_bank',
            'dest': 'calc_spec_buyRes',
            'conditions': 'is_going_to_spec_buyRes'
        },
        {   # start -> about
            'trigger': 'advance',
            'source': 'start',
            'dest': 'about',
            'conditions': 'is_going_to_about'
        },
        {
            'trigger': 'advance',
            'source': 'about',
            'dest': 'help',
            'conditions': 'is_going_to_help'
        },
        {
            'trigger': 'advance',
            'source': 'about',
            'dest': 'explain',
            'conditions': 'is_going_to_explain'
        },
        {
            'trigger': 'advance',
            'source': 'about',
            'dest': 'info',
            'conditions': 'is_going_to_info'
        },
        {   # go back transitions
            'trigger': 'go_about',
            'source': [
                'help',
                'explain',
                'info'
            ],
            'dest': 'about'
        },
        {
            'trigger': 'go_calc',
            'source': [
                'calc_best_sellRes',
                'calc_best_buyRes',
                'calc_spec_sellRes',
                'calc_spec_buyRes'
            ],
            'dest': 'calc'
        },
        {
            'trigger': 'go_back',
            'source': [
                'bestRes',
                'allRes',
                'calc'
            ],
            'dest': 'start'
        }
    ],
    initial='init',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
