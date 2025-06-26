from utils.trt1.civel_trt1 import emitir_certidao_civel
from utils.trt1.criminal_trt1 import emitir_certidao_criminal
from utils.trt1.eleitoral_trt1 import emitir_certidao_eleitoral
from utils.nada_consta.civel_nada_consta import emitir_civel_cnc_tjdft
from utils.nada_consta.criminal_nada_consta import emitir_criminal_cnc_tjdft
from utils.nada_consta.especial_nada_consta import emitir_especial_cnc_tjdft
from utils.nada_consta.falencia_nada_consta import emitir_falencia_cnc_tjdft

# cpf = "09240380124"
# id_registro = "1"  # ID que você quiser

teste = emitir_certidao_eleitoral(
    cpf="09240380124",    
    id_registro="21"
)

print(teste)