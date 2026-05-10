from fastapi import APIRouter, HTTPException, Query, UploadFile, File

from services.parse_data_service import ParseDataService
from services.dadata_app_service import DadataAppService

router = APIRouter()

@router.post(
    "/file", 
    summary="Получаем данные из файла"
)
async def add_user(file: UploadFile = File(...)):
    parser_service = ParseDataService(file)
    parse_data = await parser_service.extract_json_by_patern()
    
    return {
        "count" : len(parse_data),
        "data": parse_data
    }

@router.post(
    "/file-import", 
    summary="Импортируем данные из файла"
)
async def add_user(file: UploadFile = File(...)):
    parser_service = ParseDataService(file)
    dadata_service = DadataAppService()
    parse_data = await parser_service.extract_json_by_patern()

    # return dadata_service.get_clean('Московская обл, Люберцы г, Марусино д, Заречная ул, дом № 29')
    # return dadata_service.get_by_id('fias_id')
    data = []

    for index, address in enumerate(parse_data):
        if index not in [0, 10] and index % 9 != 0:
            continue

        dadata_result = dadata_service.get_clean(address)

        data.insert(
            index,
            {
                "input_adress": address,
                "dadata_output": {
                    "result": dadata_result["result"],
                    "fias_id": dadata_result["fias_id"],
                    "fias_code": dadata_result["fias_code"],
                    "kladr_id": dadata_result["fias_code"]
                }
            }
        )
        # return dadata_service.get_clean(address)
    
    return data



@router.post(
    "/import-by-adress", 
    summary="Запрос по адресу"
)
async def by_address(address):
    dadata_service = DadataAppService()

    return dadata_service.get_clean(address)