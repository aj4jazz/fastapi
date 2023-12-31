import os
from pprint import pprint

from databricks_api import DatabricksAPI
from obfuscate_op import o2, o3

#os.environ["DATABRICKS_HOST"] = "https://xyz.azuredatabricks.net"
#os.environ["DATABRICKS_TOKEN"] = "dapi..."

# Provide a host and token
db = DatabricksAPI(
    host=os.getenv("DATABRICKS_HOST"),
    token=os.getenv("DATABRICKS_TOKEN")
)

clusters = db.cluster.list_clusters()
pprint(o2(clusters))

print("==============================")
#https://docs.databricks.com/dev-tools/api/latest/clusters.html
cluster_events = db.cluster.get_events(
    cluster_id=o3('4106-080702-jrryux37'),
    #event_types=['RUNNING', 'RESIZING', 'TERMINATING'],
    #offset=None,
    #limit=None,
    #order='DESC',
)

# cluster_events = db.cluster.get_events(
#     cluster_id=o3('4106-080702-jrryux37'),
#     #event_types=['RUNNING', 'RESIZING', 'TERMINATING'],
#     offset=250,
#     limit=100,
#     order='ASC',
# )

pprint(o2(cluster_events))