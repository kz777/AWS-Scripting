import boto3
# import dateutil.parser
import datetime
from dateutil import parser
from dateutil.parser import *
# import calendar
# import pytz




def handler(event, context):
	count = 0
	new_servers=[]
	
	session = boto3.Session(region_name="us-east-1")
	ec2 = session.resource('ec2')

	#sns = boto3.client('sns')
	sns = session.client('sns')

	instances = ec2.instances.all()
	for i in instances:
		launch_time = i.launch_time
		current_time = datetime.datetime.now(i.launch_time.tzinfo)
		running_time = current_time - launch_time
		if running_time.days > 1:
			continue
		else:
			for t in i.tags:
				if t['Key'] == 'Name':
					new_servers.append(t["Value"])
					new_servers += [i.private_ip_address]
					count +=1

	# print new_servers

	# print count
	# print "The following servers were created in the last 24 hours: \n\n" + "\n".join(new_servers or "" for new_servers in new_servers) + "\n\ntotal new servers number is: %s" %(count)

	if len(new_servers) > 0:
		strin = "The following servers were created in the last 24 hours: \n\n" + "\n".join(new_servers or "" for new_servers in new_servers) + "\n\n The total number of newly created server(s) is: %s" %(count)
	else:
		return None

	response = sns.publish(TopicArn ='arn:aws:sns:us-east-1:aws_account:new_servers', Message = strin, Subject = "Newly Created Servers List")

handler(1,2)