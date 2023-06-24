import boto3
from dotenv import load_dotenv
import os


def saveAllToS3(folderPath: str, S3subFolder: str, delete: bool = False) -> None:


    load_dotenv(f"{os.getcwd()}/.env")

    # Get connection handle
    session = boto3.session.Session(aws_access_key_id=os.environ.get("Amazon_s3_akey"),
                                    aws_secret_access_key=os.environ.get("Amazon_s3_skey"),
                                    region_name='eu-west-1')
    bucket='s3paragon225211-dev'
    s3 = session.resource('s3')


    # Save files sequentially
    fileList = os.listdir(folderPath)

    fileToSave = ['.mp4', '.png', '.json']

    for item in  fileList:
        if 'mp4' in item:
            videoId = item.replace('.mp4', '')
            s3_subfolder = f'videos/{S3subFolder}/videoId={videoId}/'

            for fileType in fileToSave:
                if fileType == '.mp4':
                    videoId = 'video'
                elif fileType == '.png':
                    videoId = 'thumbnail'
                elif fileType == '.json':
                    videoId = 'metadata'
                s3_path = s3_subfolder + videoId + fileType
                local_path = folderPath + videoId + fileType
                
                s3.meta.client.upload_file(Filename=local_path, Bucket=bucket, Key=s3_path)
                if delete:
                    os.remove(local_path)





if __name__ == '__main__':
    saveAllToS3(f"{os.getcwd()}/Paragon_Backend/Python/Data/videos/")