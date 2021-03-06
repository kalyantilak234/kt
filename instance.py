#!/usr/bin/env python
import boto3
from prettytable import PrettyTable

client = boto3.client('ec2')
All_Region = []

for region in client.describe_regions()['Regions']:
        All_Region.append(region['RegionName'])

All_Instance = {}

for REGION in All_Region:
    ec2Resource = boto3.resource('ec2',region_name=REGION)
    instances = ec2Resource.instances.filter()
    for instance in instances:
        if instance.state["Name"] == "running":
            if REGION not in All_Instance:
                All_Instance[REGION] =[]
                All_Instance[REGION].append({'Inastance_ID':'{}'.format(instance.id),'Inastance_type':'{}'.format(instance.instance_type),\
                                             'Inastance_state':'{}'.format(instance.state["Name"])})
            else:
                All_Instance[REGION].append({'Inastance_ID':'{}'.format(instance.id),'Inastance_type':'{}'.format(instance.instance_type),\
                                             'Inastance_state':'{}'.format(instance.state["Name"])})
        if instance.state["Name"] == "stopped":
            if REGION not in All_Instance:
                All_Instance[REGION] =[]
                All_Instance[REGION].append({'Inastance_ID':'{}'.format(instance.id),'Inastance_type':'{}'.format(instance.instance_type),\
                                             'Inastance_state':'{}'.format(instance.state["Name"])})
            else:
                All_Instance[REGION].append({'Inastance_ID':'{}'.format(instance.id),'Inastance_type':'{}'.format(instance.instance_type),\
                                             'Inastance_state':'{}'.format(instance.state["Name"])})




result = PrettyTable()
result.field_names = ["Region","Total_Instance","Running","Stopped"]


for region in All_Instance.keys():
    running_count = 0
    stopped_count = 0
    total_count = 0
    for values in All_Instance[region]:
        if values['Inastance_state'] == 'running':
            running_count = running_count+1
        if values['Inastance_state'] == 'stopped':
            stopped_count = stopped_count+1
    total_count = running_count + stopped_count
    result.add_row([region,total_count,running_count,stopped_count])
print(result)
