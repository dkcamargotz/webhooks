from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from os import environ

from src.controllers import ConfirmationWebhook, ConfirmationController
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
api.add_resource(
    ConfirmationController, 
    '/api/confirmation/<string:confirmation_id>',
    resource_class_kwargs={
        "subscription_repository": subscription_repository,
        "confirmation_repository": confirmation_repository
    }
)


if __name__ == '__main__':
    app.run(
        debug=True,
        host=environ.get('MAIL_HOST'),
        port=environ.get('MAIL_PORT')
    )
