from ports.raisely_data_store import RaiselyDataStore

from oauth2client.service_account import ServiceAccountCredentials
import gspread


class GoogleSheetsDataStore(RaiselyDataStore):

    def __init__(self, gspread_client):
        self.gspread_client = gspread_client

    @classmethod
    def intialise(cls, keyfile_dict, spreadsheet_id) -> None:

        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            keyfile_dict=keyfile_dict,
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"]
        )

        client = gspread.authorize(credentials)

        gspread_client = client.open_by_key(spreadsheet_id)

        return cls(gspread_client)

    def ingest(self, data, worksheet: int = 0):

        ws = self.gspread_client.get_worksheet(worksheet)

        ingest_response = ws.append_row(data)

        return ingest_response
