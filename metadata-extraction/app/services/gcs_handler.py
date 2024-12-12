import logging
import os

from google.cloud import storage


logger = logging.getLogger(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))

credentials_path = os.path.join(project_dir, 'credentials.json')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

storage_client = storage.Client()

def download_pdf_from_gcs(bucket_name, document_id, destination_file):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(f"pdf/{document_id}.pdf")
        blob.download_to_filename(destination_file)
        logger.info(f"Downloaded PDF {document_id} from GCS.")
    except Exception as e:
        logger.error(f"Error downloading PDF {document_id} from GCS: {e}")
        raise
