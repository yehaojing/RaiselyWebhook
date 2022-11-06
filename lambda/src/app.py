from aws_lambda_powertools.event_handler import (
    APIGatewayRestResolver,
    CORSConfig
)
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities import parameters

import os

from adapters.google_sheets_data_store import GoogleSheetsDataStore

cors_config = CORSConfig(allow_origin="*", max_age=300)
app = APIGatewayRestResolver(cors=cors_config)
logger = Logger()


@logger.inject_lambda_context
@app.post('/raisely/webhook')
def post_raisely_webhook():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    if app.current_event.json_body:
        sheets = GoogleSheetsDataStore.intialise(
            keyfile_dict=parameters.get_secret(
                os.environ["GOOGLE_SERVICE_ACCOUNT_SECRET"],
                transform="json"
            ),
            spreadsheet_id=os.environ["GOOGLE_SHEET_ID"]
        )

        body = app.current_event.json_body

        donation_type = body["data"]["type"]
        created_at = body["data"]["data"]["createdAt"]
        donation_amount = body["data"]["data"]["amount"]
        message = body["data"]["data"]["message"]

        data = [donation_type, created_at, donation_amount, message]

        ingest_resp = sheets.ingest(data)

        return {
            "statusCode": 201,
            "body": {
                "message": "Data ingestion successful.",
                "ingest_resp": ingest_resp
            }
        }
    else:  # empty POST means handshake with Raisely
        return {
            "statusCode": 202,
            "body": {
                "message": "Empty POST acknowledged."
            }
        }


def lambda_handler(event, context):
    return app.resolve(event, context)
