import json
import boto3
import datetime


# Setting the retention period to 2 days
retentionDate = datetime.datetime.now() - datetime.timedelta(days=${retentionDays})


def lambda_handler(event, context):
    print("Connecting to RDS")
    rds = boto3.setup_default_session(region_name='${target_region}')
    client = boto3.client('rds')
    for snapshot in client.describe_db_snapshots(SnapshotType='manual',DBInstanceIdentifier='${rds_instances}', MaxRecords=50)['DBSnapshots']:
        create_ts = snapshot['SnapshotCreateTime']
        create_ts = create_ts.replace(tzinfo=None)
        #print "create_ts = % " % create_ts
        print "Detected DBInstanceIdentifier =" , snapshot['DBInstanceIdentifier']
        if create_ts < retentionDate:
            print "Deleting snapshot id:", snapshot['DBSnapshotIdentifier']
            client.delete_db_snapshot(DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier'])
            print "========================================"
