from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from src.controllers import ConfirmationWebhook
from src.respositories import WebhookSubscriptionDatabaseRepository, ConfirmationDatabaseRepository
load_dotenv()
app = Flask(__name__)
api = Api(app)

subscription_repository = WebhookSubscriptionDatabaseRepository()
confirmation_repository = ConfirmationDatabaseRepository()

# rounting definitions
api.add_resource(
    ConfirmationWebhook, 
    '/webhook/confirmation',
    resource_class_kwargs={
        "subscription_repository": subscription_repository,
        "confirmation_repository": confirmation_repository
    }
)



if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
        port='8080'
    )
