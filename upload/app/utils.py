from fastapi import HTTPException, status

MAX_FILE_SIZE = 10 * 1024 * 1024

def validate_file_size(file_size: int):
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File size exceeds the maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024)} MB.",
        )

def validate_file_type(content_type: str):
    if content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file format. Only PDF files are accepted.",
        )
