import os
import shutil
import tempfile
from fastapi import FastAPI, HTTPException, status, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List

# --- 1. DEFINIÇÃO DOS MODELOS DE DADOS (PYDANTIC) ---
# (Nenhuma mudança aqui, mantendo os modelos de antes)

class Imovel(BaseModel):
    """Modelo para os dados do imóvel."""
    matricula_imovel: str = Field(..., description="Número da matrícula do imóvel.")
    numero_iptu: str = Field(..., description="Número do IPTU do imóvel.")
    cartorio_imovel: str = Field(..., description="Cartório de registro do imóvel.")

class ProprietarioPF(BaseModel):
    """Modelo para um proprietário Pessoa Física."""
    nome_completo: str = Field(..., description="Nome completo do proprietário.")
    nome_mae: str = Field(..., description="Nome da mãe do proprietário.")
    cpf: str = Field(..., description="CPF do proprietário (formato: 123.456.789-00).")

class SolicitacaoPF(BaseModel):
    """Modelo completo para a requisição de certidão de Pessoa Física."""
    id: str = Field(..., description="ID único da solicitação.")
    proprietarios: List[ProprietarioPF] = Field(..., description="Lista de proprietários PF.")
    imovel: Imovel

class ProprietarioPJ(BaseModel):
    """Modelo para um proprietário Pessoa Jurídica."""
    razao_social: str = Field(..., description="Razão social da empresa.")
    cnpj: str = Field(..., description="CNPJ da empresa (formato: 12.345.678/0001-90).")

class SolicitacaoPJ(BaseModel):
    """Modelo completo para a requisição de certidão de Pessoa Jurídica."""
    id: str = Field(..., description="ID único da solicitação.")
    proprietarios: List[ProprietarioPJ] = Field(..., description="Lista de proprietários PJ.")
    imovel: Imovel


# --- 2. CONFIGURAÇÃO DA APLICAÇÃO FASTAPI ---
app = FastAPI(
    title="API de Solicitação de Certidões",
    description="Esta API recebe dados de solicitações, cria pastas e permite upload/download de arquivos.",
    version="1.3.0"
)

# Nomes das pastas base
CERTIDOES_BOT_DIR = "certidoes_bot"
CERTIDOES_DOWNLOAD_DIR = "certidoes_download"

# --- 3. EVENTO DE STARTUP ---
@app.on_event("startup")
def on_startup():
    """Cria os diretórios base na inicialização da API."""
    print("Iniciando a API e verificando as pastas base...")
    os.makedirs(CERTIDOES_BOT_DIR, exist_ok=True)
    os.makedirs(CERTIDOES_DOWNLOAD_DIR, exist_ok=True)
    print(f"Pasta '{CERTIDOES_BOT_DIR}' pronta.")
    print(f"Pasta '{CERTIDOES_DOWNLOAD_DIR}' pronta.")


# --- FUNÇÕES AUXILIARES ---
def criar_pastas_para_solicitacao(solicitacao_id: str):
    """Cria as pastas para uma solicitação específica."""
    try:
        path_bot = os.path.join(CERTIDOES_BOT_DIR, solicitacao_id)
        path_download = os.path.join(CERTIDOES_DOWNLOAD_DIR, solicitacao_id)
        os.makedirs(path_bot, exist_ok=True)
        os.makedirs(path_download, exist_ok=True)
        return path_bot, path_download
    except OSError as e:
        print(f"ERRO ao criar pastas para ID {solicitacao_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Não foi possível criar as pastas no servidor. Verifique as permissões. Erro: {e}"
        )

def cleanup_temp_dir(temp_dir: str):
    """Função para limpar (remover) o diretório temporário após o envio do arquivo."""
    print(f"Limpando diretório temporário: {temp_dir}")
    shutil.rmtree(temp_dir)


# --- 4. ROTAS DE SOLICITAÇÃO ---

@app.get("/")
async def root():
    return {"message": "Bem-vindo à API de Certidões! Acesse /docs para ver a documentação."}


@app.post("/solicitacao/pf", status_code=status.HTTP_201_CREATED)
async def criar_solicitacao_pf(solicitacao: SolicitacaoPF):
    """Recebe dados de PF e cria as pastas."""
    path_bot, path_download = criar_pastas_para_solicitacao(solicitacao.id)
    return {
        "message": "Solicitação para Pessoa Física recebida com sucesso!",
        "solicitacao_id": solicitacao.id,
        "pastas_criadas": [path_bot, path_download],
        "dados_recebidos": solicitacao
    }


@app.post("/solicitacao/pj", status_code=status.HTTP_201_CREATED)
async def criar_solicitacao_pj(solicitacao: SolicitacaoPJ):
    """Recebe dados de PJ e cria as pastas."""
    path_bot, path_download = criar_pastas_para_solicitacao(solicitacao.id)
    return {
        "message": "Solicitação para Pessoa Jurídica recebida com sucesso!",
        "solicitacao_id": solicitacao.id,
        "pastas_criadas": [path_bot, path_download],
        "dados_recebidos": solicitacao
    }


# --- 5. ROTAS DE UPLOAD ---

@app.post("/upload/bot/{solicitacao_id}", status_code=status.HTTP_201_CREATED)
async def upload_file_to_bot_folder(solicitacao_id: str, file: UploadFile = File(...)):
    """
    Faz o upload de um arquivo para a pasta 'certidoes_bot' de uma solicitação.
    Se a pasta da solicitação não existir, ela será criada.
    """
    # Garante que a pasta de destino exista
    criar_pastas_para_solicitacao(solicitacao_id)
    
    # Constrói o caminho de destino do arquivo de forma segura
    destination_dir = os.path.join(CERTIDOES_BOT_DIR, solicitacao_id)
    file_path = os.path.join(destination_dir, file.filename)

    # Medida de segurança para evitar que usuários salvem arquivos fora do diretório esperado
    if ".." in file.filename or "/" in file.filename or "\\" in file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de arquivo inválido."
        )

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Não foi possível salvar o arquivo. Erro: {e}"
        )
    finally:
        file.file.close()

    return {
        "message": f"Arquivo '{file.filename}' salvo com sucesso!",
        "solicitacao_id": solicitacao_id,
        "path_salvo": file_path
    }


# --- 6. ROTAS DE DOWNLOAD ---

@app.get("/download/list/{solicitacao_id}")
async def list_downloadable_files(solicitacao_id: str):
    """Lista todos os arquivos disponíveis para download para uma solicitação."""
    target_dir = os.path.join(CERTIDOES_DOWNLOAD_DIR, solicitacao_id)

    if not os.path.isdir(target_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solicitação com ID '{solicitacao_id}' não encontrada."
        )

    try:
        files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
        if not files:
            return {"id": solicitacao_id, "message": "Nenhum arquivo disponível para download.", "files": []}
        return {"id": solicitacao_id, "files": files}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar os arquivos: {e}"
        )


@app.get("/download/file/{solicitacao_id}/{filename}", response_class=FileResponse)
async def download_single_file(solicitacao_id: str, filename: str):
    """Faz o download de um arquivo específico de uma solicitação."""
    file_path = os.path.join(CERTIDOES_DOWNLOAD_DIR, solicitacao_id, filename)

    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome de arquivo inválido."
        )

    if not os.path.isfile(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Arquivo '{filename}' não encontrado para a solicitação '{solicitacao_id}'."
        )

    return FileResponse(path=file_path, media_type='application/octet-stream', filename=filename)


@app.get("/download/zip/{solicitacao_id}", response_class=FileResponse)
async def download_certidoes_zip(solicitacao_id: str, background_tasks: BackgroundTasks):
    """
    Compacta e faz o download de TODOS os arquivos da pasta 'certidoes_download' 
    para um determinado ID de solicitação em um arquivo ZIP.
    """
    target_dir = os.path.join(CERTIDOES_DOWNLOAD_DIR, solicitacao_id)

    if not os.path.isdir(target_dir) or not os.listdir(target_dir):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Solicitação com ID '{solicitacao_id}' não encontrada ou pasta de download vazia."
        )

    temp_dir = tempfile.mkdtemp()
    zip_path_base = os.path.join(temp_dir, solicitacao_id)

    try:
        zip_path = shutil.make_archive(base_name=zip_path_base, format='zip', root_dir=target_dir)
    except Exception as e:
        cleanup_temp_dir(temp_dir)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Falha ao compactar os arquivos. Erro: {e}"
        )

    background_tasks.add_task(cleanup_temp_dir, temp_dir)

    return FileResponse(
        path=zip_path,
        media_type='application/zip',
        filename=f"{solicitacao_id}_certidoes.zip"
    )