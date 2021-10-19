from flask import Flask
from flask import request
from main import *
import logging
from flask_celery import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://redis:6379',
    CELERY_RESULT_BACKEND='redis://redis:6379',
)
celery = make_celery(app)

@celery.task
def create_order(data):
    with open('offers.json', 'r') as f:
        offers = json.load(f)
    driver = get_driver()
    login(driver)
    go_to_sales(driver)
    add_order(
        driver,
        data['email'],
        offers[data['offer']],
        pay_type=data.get('pay_type', 'BILL'),
        comment='POSCREDIT',
    )
    driver.close()

@app.route("/getgc", methods=["POST"])
def getgc():
    data = request.get_json(force=True)
    create_order.delay(data)
    return json.dumps({'success': True})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
