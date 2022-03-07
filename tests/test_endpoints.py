import json
import os

import pandas

from valometa.data import sqlite_db_path

body = {
    "date_begin": "2021-05-01",
    "date_end": "2021-10-30"
}


class TestMatchPerDayJSON:
    endpoint = "/valometa/matches-per-day-json"

    def test_db_exists(self):
        assert os.path.exists(sqlite_db_path)

    def test_response_is_200(self, client):
        response = client.post(
            self.endpoint,
            headers={"Content-Type": "application/json"},
            json=body
        )

        assert response.status_code == 200

    def test_data_shape_matches_range(self, client):
        response = client.post(
            self.endpoint,
            headers={"Content-Type": "application/json"},
            json=body
        )

        response_data = (
            pandas
            .DataFrame
            .from_dict(json.loads(response.text))
        )        

        assert response_data.shape == (
            response_data
            .query("date_of_count >= @body['date_begin']")
            .query("date_of_count <= @body['date_end']")
            .shape
        )
