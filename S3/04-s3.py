import boto3
import pprint


def handler(event, context):
	count = 0
	listVersions = []
	extraVersions = []
	bucket = 'mybucket8815'
	key = 'About Me.pages'
	session = boto3.Session(region_name="us-east-1")
	s3 = session.resource('s3')
	versions = s3.Bucket(bucket).object_versions.filter(Prefix=key)

	for version in versions:
		listVersions.append(version)

		# print version
		# objectss = version.get()
		# for objs in objectss:
		# 	listVersions.append(objs)
		count += 1
	for objs in listVersions[2:]:
		# print objs
		extraVersions.append(objs)

	for ver in extraVersions:
		
		ver.delete()
		print ver
		
	# print listVersions
	print count


    

	




handler(1,2)