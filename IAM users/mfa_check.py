import boto3
from botocore.exceptions import ClientError


# loop through virtual mfa to find users that actually have it
def handler(event, context):

	session = boto3.Session(region_name="us-east-1")


	client = session.client("iam")
	# client = boto3.client('iam')

	#sns = boto3.client('sns')
	sns = session.client('sns')

	response 			= client.list_users()
	userVirtualMfa 		= client.list_virtual_mfa_devices(AssignmentStatus='Assigned')

	userList = response['Users']

	iam = session.resource('iam')

	noPassword  = []
	withMfA     = []
	badUser     = []
	goodUsers   = []
	bad_user = 0
	strin = ""
    
	for virtual in userVirtualMfa['VirtualMFADevices']:
		withMfA.append(virtual['User']['UserName'])

	for user in iam.users.all():
		# Nothing is initially loaded
		profile = user.LoginProfile()
		try:
			profile.load()
			# We don't care if this works
		except ClientError as e:
			if 'NoSuchEntity' in e.response['Error']['Code']:
				nm = user.name
				#print(nm,"is a service account.")
				noPassword.append(nm)
		goodUsers = noPassword + withMfA
		userMfa = client.list_mfa_devices(UserName= user.name)
		if len(userMfa['MFADevices']) == 0:
			# loops through users to find BadUsers(users with PASSWORD and without MFA)
			if user.name not in goodUsers:
				badUser.append(user.name)
				bad_user += 1
			

#You can uncomment the print statement to see the outcomes on logfile
# 	print "MFA is not enabled for the following users: \n\n" + "\n".join(badUser) + "\ntotal users number wthout MFA is: %s" %(bad_user)



	if len(badUser) > 0:
		strin = "MFA is not enabled for the following users: \n\n" + "\n".join(badUser) + "\ntotal users number is: %s" %(bad_user)
	else:
		return None

	response = sns.publish(TopicArn ='arn:aws:sns:us-east-1:account_number:mfa_alert', Message = strin, Subject = "Enable MFA")