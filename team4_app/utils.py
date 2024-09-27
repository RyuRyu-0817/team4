import boto3
from django.conf import settings
# from django.conf import settings
# AWSの設定が必要


def upload_file_to_s3(file, filename):
    # S3クライアントを作成
    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )

    # ファイルをS3にアップロード
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    s3.upload_fileobj(file, bucket_name, filename)

    # アップロードされたファイルのURLを生成
    file_url = f"https://{bucket_name}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{filename}"
    
    return file_url