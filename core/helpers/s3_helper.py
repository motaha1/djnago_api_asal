# from abc import ABC
# import uuid
#
# from storages.backends.s3boto3 import S3Boto3Storage
#
#
# class UserAvatarMediaStorage(S3Boto3Storage, ABC):
#     location = 'users-media/'
#
#
# def avatars_directory_path(instance, filename):
#     file_uuid = uuid.uuid4().hex
#     return f'avatar/{file_uuid}/{filename}'