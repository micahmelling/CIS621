""""
This uses the infrastructure as code framework Pulumi, which you will have to install and configure.
"""

import pulumi_aws as aws
from pulumi import ResourceOptions


def main(database_name, allocated_gb_storage, db_engine, db_engine_version, instance_class, root_password,
         root_username, subnet_group_name, subnet_id_list, security_group_name, vpc_id, allowed_ip_list,
         security_group_port):
    """
    Creates an RDS instance and associated security group.

    :param database_name: name of the database
    :param allocated_gb_storage: number of gigabytes of storage
    :param db_engine: database engine
    :param db_engine_version: database engine version
    :param instance_class: compute instance type
    :param root_password: password for the root user
    :param root_username: username for the root user
    :param subnet_group_name: name of the db subnet group to create
    :param subnet_id_list: list of subnets to launch the instance in
    :param security_group_name: name of the security group to create
    :param vpc_id: id of the VPC to create the security group in
    :param allowed_ip_list: list of ip addresses to allow access to the RDS instance
    :param security_group_port: the port over which traffic should be allowed
    """

    subnet_group = aws.rds.SubnetGroup(
        subnet_group_name,
        name=subnet_group_name,
        subnet_ids=subnet_id_list,
    )

    security_group = aws.ec2.SecurityGroup(
        security_group_name,
        name=security_group_name,
        vpc_id=vpc_id,
        ingress=[aws.ec2.SecurityGroupIngressArgs(
            protocol='tcp',
            from_port=security_group_port,
            to_port=security_group_port,
            cidr_blocks=allowed_ip_list
        )],
        egress=[aws.ec2.SecurityGroupEgressArgs(
            from_port=0,
            to_port=0,
            protocol="-1",
            cidr_blocks=["0.0.0.0/0"],
        )])

    rds = aws.rds.Instance(
        database_name,
        opts=ResourceOptions(depends_on=[subnet_group]),
        allocated_storage=allocated_gb_storage,
        engine=db_engine,
        engine_version=db_engine_version,
        instance_class=instance_class,
        name=database_name,
        password=root_password,
        username=root_username,
        publicly_accessible=True,
        skip_final_snapshot=True,
        db_subnet_group_name=subnet_group_name,
        vpc_security_group_ids=[security_group.id]
