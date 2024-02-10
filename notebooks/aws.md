## AWS CLI

- Install AWS CLI [Link](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- configure aws using access keys from user security credentials.

## S3 bucket generation

With S3, it is possible to use either: high-level S3 commands (i.e. commands that start with aws s3) or low level S3 commands (i.e. commands that start with aws s3api). The high level aws s3 commands are typically used to execute common S3 tasks with simplified commands. The low level aws s3api commands are used for more advanced or custom interactions with S3 through API calls.

```bash
aws s3 mb s3://your_bucket_name
aws s3 mb s3://your_bucket_name --region your_aws_region
```

OR

```bash
aws s3api create-bucket --bucket your_bucket_name
aws s3api create-bucket --bucket your_bucket_name --region your_aws_region
```

To check if your bucket has been created, run the command:

```bash
aws s3 ls
```

You can create folder or boject into a bucket by running:

```bash
# create new folder
aws s3api put-object --bucket your_bucket_name --key your_folder_name/
# create object inside of a folder
aws s3api put-object --bucket your_bucket_name --key your_folder_name/your_object_name
# delete an object
aws s3 rm s3://your_bucket_name/name_of_object_to_delete
#or
aws s3api delete-object --bucket your_bucket_name --key name_of_object_to_delete

# delete all object inside of a bucket
aws s3 rm s3://name_of_bucket --recursive
# delete a bucket
aws s3api delete-bucket --bucket your_bucket_name
```

To check the contents of your bucket

```bash
aws s3 ls s3://your_bucket_name
```

Copying local files to S3 bucket

```bash
aws s3 cp your_local_file_path s3://your_bucket_name/your_folder_name/
```

## Connecting to AWS codecommit

- Generate HTTPS Git credentials for AWS CodeCommit for the user

Then, create a repesoritory in codecommit and add the repo as remote repository in your local git repo.

```bash
git remote add <remote_name> <remote_repo_link>
# push the code to the remote repo
git push <remote_name>
```
