import os
import uuid
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from config import settings


class StorageService:
    def __init__(self):
        self.storage_path = Path(settings.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.use_s3 = False

        self.s3_client = None
        if self.use_s3:
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region,
            )

    def save_file_locally(self, file_bytes: bytes, filename: str) -> str:
        unique_name = f"{uuid.uuid4().hex}_{filename}"
        file_path = self.storage_path / unique_name
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        return str(file_path)

    def upload_to_s3(self, file_bytes: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
        if not self.s3_client:
            raise RuntimeError("S3 is not configured")

        unique_name = f"{uuid.uuid4().hex}_{filename}"
        try:
            self.s3_client.put_object(
                Bucket=settings.aws_bucket_name,
                Key=unique_name,
                Body=file_bytes,
                ContentType=content_type,
            )
            return f"https://{settings.aws_bucket_name}.s3.{settings.aws_region}.amazonaws.com/{unique_name}"
        except (BotoCoreError, ClientError) as e:
            raise RuntimeError(f"Failed to upload file to S3: {e}")

    def save_file(self, file_bytes: bytes, filename: str, content_type: str = "application/octet-stream") -> str:
        if self.use_s3:
            return self.upload_to_s3(file_bytes, filename, content_type)
        return self.save_file_locally(file_bytes, filename)