from fastapi import File, UploadFile, APIRouter, status
from fastapi.responses import FileResponse

from src.api.utils.routes import make_json_response, make_error_response
from src.api.constants import VALID_CONTENT_TYPES, VALID_FILE_TYPES
from src.api.utils.routes import save_client_data

router = APIRouter(prefix="/api", tags=["file"])


@router.post(
    "/dataset/upload",
    summary="Uploads a {csv, xls, xlsx} file.",
    status_code=status.HTTP_200_OK,
)
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint para fazer upload de um arquivo.

    Parâmetros:
    file (UploadFile): O arquivo a ser enviado.

    Retorna:
    dict: Um dicionário contendo informações sobre o arquivo enviado.
    """
    # Validate file size and type
    if file.content_type in VALID_CONTENT_TYPES:
        # Save the file or process it as needed
        save_client_data(provider_id, client_id, file)

        content = {"file": file.filename}
        return make_json_response(200, content)
    else:
        message = f'Invalid file type. Must be one of: {VALID_FILE_TYPES}'
        content = {"error": message}
        return make_error_response(content)


@router.get(
    "/dataset/download",
    summary="Downloads a file.",
    status_code=status.HTTP_200_OK,
)
async def download_file(file_name: str):
    """
    Endpoint para baixar um arquivo.

    Parâmetros:
        file_name (str): O nome do arquivo a ser baixado.

    Retorna:
        FileResponse: Um objeto FileResponse representando o arquivo a ser baixado.
    """
    # Assuming the file is located in a specific directory
    # Generate the full path dynamically based on the file_name parameter
    file_path = f"uploads/{file_name}"
    return FileResponse(file_path, filename=file_name)
