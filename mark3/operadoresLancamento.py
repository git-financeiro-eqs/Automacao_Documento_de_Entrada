from pyautogui import hotkey, press, write, FAILSAFE
from pyperclip import paste
from time import sleep
import pyscreeze
import utils


FAILSAFE = True

def escrever_valor_unit(valor_unit_convertido, passos=6):
    press(["right"]*passos)
    valor_unit_convertido = utils.formatador(valor_unit_convertido, casas_decimais="{:.6f}")
    sleep(0.2)
    write(valor_unit_convertido)
    sleep(0.2)
    press(["right"]*3)
    utils.checar_failsafe()
 
 
def verificar_valor_item(lista, indiceX):
    razoes = []
    sleep(0.7)
    cancelar_lancamento = False
    press(["right"]*4)
    sleep(0.7)
    hotkey("ctrl", "c")
    sleep(0.7)
    utils.checar_failsafe()
    valor_do_item_no_siga = paste()
    valor_do_item_no_siga = utils.formatador4(valor_do_item_no_siga)
    valor_do_item_na_NF = lista[indiceX][0]
    valor_do_item_na_NF = utils.formatador3(valor_do_item_na_NF)
    if valor_do_item_no_siga != valor_do_item_na_NF:
        write(lista[indiceX][0])
        sleep(1.5)
        encontrar = utils.encontrar_imagem(r'Imagens\ValItemErrado.png')
        utils.checar_failsafe()
        if type(encontrar) == pyscreeze.Box:
            press("enter", interval=0.5)
            encontrar = utils.encontrar_imagem(r'Imagens\ValItemErrado.png')
            utils.checar_failsafe()
            if type(encontrar) == pyscreeze.Box:
                press("enter")
            press("esc")
            press(["left"]*5)
            sleep(0.2)
            hotkey("ctrl", "c", interval=0.5)
            utils.checar_failsafe()
            quantidade_siga = paste()
            quantidade_siga = utils.formatador4(quantidade_siga)
            quantidade_NF = lista[indiceX][1]
            quantidade_NF = utils.formatador3(quantidade_NF)
            valor_unit_NF = lista[indiceX][2]
            valor_unit_NF = utils.formatador3(valor_unit_NF)
            if quantidade_siga == quantidade_NF:
                escrever_valor_unit(valor_unit_NF, passos=1)
                utils.checar_failsafe()
            else:
                press(["left"]*5)
                sleep(0.2)
                hotkey("ctrl", "c", interval=0.5)
                utils.checar_failsafe()
                desc_prod = paste().lower()
                if "abracadeira" in desc_prod:
                    quantidade_convertida = quantidade_NF * 100
                    valor_unit_convertido = valor_unit_NF / 100
                    if quantidade_convertida == quantidade_siga:
                        escrever_valor_unit(valor_unit_convertido)
                        utils.checar_failsafe()
                    else:
                        razoes, cancelar_lancamento = utils.contar_item_fracionado(quantidade_siga, valor_unit_convertido, quantidade_convertida)
                elif "pilha" in desc_prod or "tubo isolante" in desc_prod:
                    quantidade_convertida = quantidade_NF * 2
                    valor_unit_convertido = valor_unit_NF / 2
                    if quantidade_convertida == quantidade_siga:
                        escrever_valor_unit(valor_unit_convertido)
                        utils.checar_failsafe()
                    else:
                        razoes, cancelar_lancamento = utils.contar_item_fracionado(quantidade_siga, valor_unit_convertido, quantidade_convertida)
                elif "gas" in desc_prod:
                    press("left")
                    hotkey("ctrl", "c", interval=0.5)
                    cod_do_item = paste()
                    press("right")
                    utils.checar_failsafe()
                    if cod_do_item == "0651000053":
                        razoes, cancelar_lancamento = utils.contar_item_fracionado(quantidade_siga, valor_unit_NF, quantidade_NF)
                    else:
                        valor_unit_convertido = valor_do_item_na_NF / quantidade_siga
                        escrever_valor_unit(valor_unit_convertido)
                        utils.checar_failsafe()
                elif "pedrisco" in desc_prod or "cabo" in desc_prod[:4] or "manta" in desc_prod or "lona" in desc_prod:
                    valor_unit_convertido = valor_do_item_na_NF / quantidade_siga
                    escrever_valor_unit(valor_unit_convertido)
                    utils.checar_failsafe()
                else:
                    razoes, cancelar_lancamento = utils.contar_item_fracionado(quantidade_siga, valor_unit_NF, quantidade_NF)
        else:
            press("left")
        utils.checar_failsafe()
    return cancelar_lancamento, razoes


def corrigir_passos_horizontal(cont, item):
    if len(item) > 1:
        press(["right"]*4)
        sleep(1)
        if cont == len(item):
            press(["left"]*4)


def copiar_natureza():
    press("right", interval=0.7)
    hotkey("ctrl", "c")
    sleep(0.7)
    natureza = paste()
    if natureza == "2020081":
        natureza = "2050006"
        utils.escrever_natureza(natureza)
    elif natureza == "2020060":
        natureza = "2050004"
        utils.escrever_natureza(natureza)
    elif natureza in ["2020082", "2020083"]:
        natureza = "2050008"
        utils.escrever_natureza(natureza)
    utils.checar_failsafe()
    return natureza


def selecionar_caso(natureza):
    codigo = {
    "2020067": 0, "2020085": 0, "2020047": 0, "2020049": 0, "2020055": 0,
    "2020045": 0, "2020006": 0, "2020041": 0, "2020048": 0, "2020042": 0,
    "2020046": 0, "2020030": 0, "2020031": 0, "2020074": 0, "2020019": 0,
    "2020040": 0, "2020056": 0, "2020075": 0, "2010016": 0,
    "2010005": 1, "2020027": 1, "2020036": 1,
    "2050003": 2, "2050004": 2, "2050005": 2, "2050006": 2,
    "2050007": 2, "2050008": 2, "2050009": 2,
    "2050001": 3,
    "2040005": 4,
    "2020029": 5, "2020053": 5,
    "2020018": 6, "2040001": 6, "2040003": 6, "2020101": 6, "2020103": 6
}
    return codigo.get(natureza, 7)


def definir_TES(codigo, ctrl_imposto):
    press(["left"]*10)
    tes = ""

    match codigo:
        case 0:
            if ctrl_imposto != "Nenhum imposto":
                tes = "421"
            else:
                tes = "420"
        
        case 1:
            if ctrl_imposto == "Nenhum imposto":
                tes = "402"
            elif ctrl_imposto in ["Apenas ICMS e ICMSST", "Apenas o ICMS", "Apenas o ICMSST"]:
                tes = "405"
            elif ctrl_imposto == "Todos os impostos":
                tes = "407"
            else:
                tes = "403"
        
        case 2:
            if ctrl_imposto not in ["Todos os impostos", "Apenas ICMS e IPI", "Apenas ICMSST e IPI", "Apenas o IPI"]:
                tes = "408"
            else:
                tes = "411"
        
        case 3:
            tes = "423"
        
        case 4:
            if ctrl_imposto not in ["Todos os impostos", "Apenas ICMS e IPI", "Apenas ICMSST e IPI", "Apenas o IPI"]:
                tes = "102"
            else:
                tes = "432"
        
        case 5:
            hotkey("ctrl", "c", interval=0.5)
            tes_padrao = paste()
            if tes_padrao == "406":
                tes = "406"
            else:
                if ctrl_imposto == "Nenhum imposto":
                    tes = "402"
                elif ctrl_imposto == "Todos os impostos":
                    tes = "407"
                elif ctrl_imposto in ["Apenas ICMS e ICMSST", "Apenas o ICMS", "Apenas o ICMSST"]:
                    tes = "405"
                else:
                    tes = "403"
        
        case 6:
            hotkey("ctrl", "c", interval=0.5)
            tes_padrao = paste()
            if tes_padrao == "406":
                tes = "406"
            else:
                press(["left"]*2)
                sleep(0.7)
                hotkey("ctrl", "c", interval=0.5)
                item_especifico = paste()
                press(["right"]*2)
                if item_especifico in ["0207000001", "1312000156", "999920091200", "999949011000", "1303102887", "1302578", "1303100449", "1303100601", "1303100602", "1303100603", "1312000122", "1312000124", "1312000125", "1312000126", "1312000144", "1308002", "1312024", "1303100550", "1303100600", "1303101290", "1303101291", "1303103835", "1303103836", "1303103837", "1312000141"]:
                    if ctrl_imposto != "Nenhum imposto":
                        tes = "421"
                    else:
                        tes = "420"
                else:
                    if ctrl_imposto == "Nenhum imposto":
                        tes = "402"
                    elif ctrl_imposto in ["Apenas ICMS e ICMSST", "Apenas o ICMS", "Apenas o ICMSST"]:
                        tes = "405"
                    elif ctrl_imposto == "Todos os impostos":
                        tes = "407"
                    else:
                        tes = "403"
                
        case 7:
            cancelar_lancamento = True
            utils.cancelar_lancamento()
            utils.voltar_descer()
            sleep(0.3)
            tes = cancelar_lancamento

    utils.checar_failsafe()
    return tes
    

def zerar_imposto(passos_ida=7, passos_volta=8):
    press(["right"]*passos_ida)
    press("enter")
    press("backspace")
    press("enter")
    press(["left"]*passos_volta)
    utils.checar_failsafe()


def escrever_TES(tes):
    press("enter", interval=0.3)
    write(tes)
    press(["right"]*4)
    utils.checar_failsafe()


def inserir_desconto(desc_no_item):
    press(["right"]*3)
    sleep(0.5)
    press("enter")
    desc_no_item = utils.formatador2(desc_no_item)
    write(desc_no_item, interval=0.02)
    sleep(0.5)
    utils.checar_failsafe()


def inserir_frete(frete_no_item):
    press(["right"]*105)
    sleep(0.6)
    press("enter")
    frete_no_item = utils.formatador2(frete_no_item)
    write(frete_no_item, interval=0.05)
    sleep(0.6)
    utils.checar_failsafe()


def inserir_seguro(seg_no_item):
    sleep(0.3)
    press("enter")
    seg_no_item = utils.formatador2(seg_no_item)
    write(seg_no_item, interval=0.05)
    sleep(0.6)
    utils.checar_failsafe()


def inserir_despesa(desp_no_item):
    sleep(0.3)
    press("enter")
    desp_no_item = utils.formatador2(desp_no_item)
    write(desp_no_item, interval=0.05)
    sleep(0.6)
    press(["left"]*112)
    utils.checar_failsafe()


def inserir_ICMS(icms_no_item, bc_icms, aliq_icms):
    press(["right"]*7)
    sleep(0.5)
    press("enter")
    bc_icms = utils.formatador2(bc_icms)
    write(bc_icms)
    press(["right"]*8)
    sleep(0.5)
    press("enter")
    utils.checar_failsafe()
    write(aliq_icms)
    sleep(0.5)
    press(["left"]*9)
    sleep(0.5)
    press("enter")
    icms_no_item = utils.formatador2(icms_no_item)
    write(icms_no_item)
    utils.checar_failsafe()


def inserir_ICMSST(icmsST_no_item, base_icms_ST, aliq_icms_ST, passosST=9):
    press(["right"]*passosST)
    sleep(0.5)
    press("enter")
    base_icms_ST = utils.formatador2(base_icms_ST)
    write(base_icms_ST)
    sleep(0.5)
    press("enter")
    utils.checar_failsafe()
    write(aliq_icms_ST)
    sleep(0.5)
    press("enter")
    icmsST_no_item = utils.formatador2(icmsST_no_item)
    write(icmsST_no_item)
    press(["left"]*12)    
    utils.checar_failsafe()


def inserir_IPI(ipi_no_item, base_ipi, aliq_ipi, passosIPI=12):
    press(["right"]*passosIPI)
    sleep(0.5)
    press("enter")
    base_ipi = utils.formatador2(base_ipi)
    write(base_ipi)
    press(["right"]*5)
    sleep(0.5)
    press("enter")
    utils.checar_failsafe()
    write(aliq_ipi)
    press(["left"]*6)
    sleep(0.5)
    press("enter")
    ipi_no_item = utils.formatador2(ipi_no_item)
    write(ipi_no_item)
    press(["left"]*14)
    utils.checar_failsafe()