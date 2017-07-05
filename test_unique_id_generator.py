import boto3
from concurrent import futures

FUNCTION_ARN_TEMPLATE = 'arn:aws:lambda:{}:{}:function:{}'

def create_unique_id(client, function_arn):
	return client.invoke(FunctionName=function_arn)['Payload'].read()

def concurrent_creation(region_name, account_id, function_name, num_ids, num_workers):
	client = boto3.client('lambda', region_name=region_name)
	with futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
		future_to_id = dict((executor.submit(create_unique_id, client, FUNCTION_ARN_TEMPLATE.format(region_name, account_id, function_name)), x) for x in range(0, num_ids))
		for future in futures.as_completed(future_to_id):
			print '{}: {}'.format(future_to_id[future], future.result())

if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Concurrent unique identifier generation")
	parser.add_argument("-a", "--account_id", type=str, help="Account in which the Lamdba is created", required=True)
	parser.add_argument("-f", "--function_name", type=str, help="Name of the Lambda", required=True)
	parser.add_argument("-r", "--region", type=str, help="AWS Region in which the lambda is located", required=True)
	parser.add_argument("-n", "--num_ids", type=int, help="Number of unique ids to generate", default=100)
	parser.add_argument("-t", "--threads", type=int, help="Number of threads to start", default=4)
	args = parser.parse_args()

	concurrent_creation(args.region, args.account_id, args.function_name, args.num_ids, args.threads)
