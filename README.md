# Unique Id Generator

This Cloudformation script creates a Lambda function which guarantees to return a unique identifier, regardless of how much concurrent identifier generation is performed.  The set of generated unique identifiers is stored in a DynamoDB table, with conditional write logic detecting any clash with a previously created identifier.

Identifiers can be created using different bases (58, 58, 62, 64) with base62 the default specified for the parameter.  Identifiers can be any length (above 5 characters), with 10 the default length specified for the parameter.  Using the defaults provides a population of 8.39E17 unique identifiers.  

The Lambda expects to receive an event of the form:

`
{
	"Base" : "62",
	"Length" : "10"
}
`

If either value is missing from the event, then the value passed as a parameter in the script will be used.

The script creates the following:

![alt text](https://github.com/gford1000-aws/unique-id-generator/blob/master/Unique%20Id%20Generator.png "Script per designer")

The Lambda executes in its own private VPC, with a VPC Endpoint providing access to the DynamoDB table.

Notes:

1. The ENI used by Lambda within a VPC may remain active, causing the stack to wait during deletion.  To resolve, switch to the EC2 Dashboard and manually Detach the ENI (easily identified in the dashboard).  Once the ENI is detached, delete it.  CloudFormation will then detect the dependency has been removed and continue its deletion of the stack.
3. Streaming is optionally available, to support replication of the DynamoDB table to another region.  This is recommended to ensure uniqueness of identifiers during a AWS Region failure.

## Arguments

| Argument                      | Description                                                                     |
| ----------------------------- |:-------------------------------------------------------------------------------:|
| Base                          | The default base to be used in generating the unique identifier                 |
| DDBEndpointPrefixList         | The VPC Endpoint to the DynamoDB service for the region                         |
| EnableReplication             | If true, then attaches a stream to the DynamoDB                                 |
| EnableXRay                    | If true, enables the Lambda to send traces to AWS X-Ray                         |
| ProvisionedReadCapacityUnits  | The read IOPS of the table                                                      |
| ProvisionedWriteCapacityUnits | The write IOPS of the table                                                     |
| Length                        | The default length of the identifier length                                     |
| XRayTraceMode                 | If XRay tracing is enabled, then this parameter specifies the type of tracing   |
| VPCTemplateURL                | The S3 url to the VPC Cloudformation script                                     |


## Outputs

| Output               | Description                                            |
| ---------------------|:------------------------------------------------------:|
| UniqueIdGeneratorArn | The Arn of the Lambda function                         |
| TableStreamArn       | The Arn of the table stream, if replication is enabled |


## Licence

This project is released under the MIT license. See [LICENSE](LICENSE) for details.
