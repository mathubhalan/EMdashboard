from influxdb_client import InfluxDBClient
import pandas as pd

class time_series():
  def __init__(self):
    self.my_token = "xDKAeRdhESSn8OMteSlvEqwTJVPDeGdkbFwaSUrLV6jhhzIIcmOa3evIArNtd8_ct4D1FZHLT5BjT24GJL_vZw=="
    self.my_org = "Flexibility"
    self.bucket = "timeseries"
    self.url="https://influxdb.electricmiles.com/"
    
  def fetch_data(self):
    query='''
          from(bucket: "timeseries")
            |> range(start: -3d)
            |> filter(fn: (r) => r["_measurement"] == "meter_reading" )
            |> filter(fn: (r) => r["_field"] == "power")
            |> keep(columns: ["_time","_field","_value","asset_id"])
            |> yield()'''
            
    client = InfluxDBClient(url=self.url, token=self.my_token, org=self.my_org, debug=False)
    data_ts = client.query_api().query_data_frame(org=self.my_org, query=query)
    return (data_ts)
