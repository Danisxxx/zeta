from pluss.Func import connect_to_db
from configs._def_main_ import *
import re
import requests

@rexbt('regen')
async def regen(client, msg):
    # Obtener el BIN desde el callback
    bin_prefix = msg.data.strip()  # Asumimos que el BIN está como parte de la data del callback
    
    # Comprobar que el BIN tiene al menos 6 dígitos
    if len(bin_prefix) < 6:
        await msg.edit_message_text('<b>El BIN no tiene 6 dígitos válidos. Intenta nuevamente.</b>', reply_markup=regene)
        return

    # Realizar la solicitud para obtener la información del BIN
    binreq = requests.get(f'https://bins.antipublic.cc/bins/{bin_prefix}')

    # Si el BIN es inválido, mostramos un error
    if 'Invalid BIN' in binreq.text or 'not found' in binreq.text:
        await msg.edit_message_text('<b>Status Dead ❌ | BIN inválido.</b>', reply_markup=regene)
        return

    try:
        # Obtener los datos del BIN
        bin_data = binreq.json()
        binif = bin_data.get('bin', bin_prefix)
        country = bin_data.get('country', 'Desconocido')
        country_name = bin_data.get('country_name', 'Desconocido')
        country_flag = bin_data.get('country_flag', '🏳️')
        bank = bin_data.get('bank', 'Desconocido')
        vendor = bin_data.get('vendor', 'Desconocido')
        type_ = bin_data.get('type', 'Desconocido')
        level = bin_data.get('level', 'Desconocido')
    except ValueError:
        await msg.edit_message_text('<b>Error al procesar la respuesta del BIN.</b>', reply_markup=regene)
        return

    # Asumimos que el BIN está en msg.data como una cadena con el BIN original
    cc = bin_prefix  # Usamos el BIN recibido
    mes = '01'  # Esto puede ajustarse a cualquier valor de mes
    ano = '2027'  # Año
    cvv = '123'  # CVV

    # Generar las tarjetas (puedes ajustar esta lógica según sea necesario)
    cc1, cc2, cc3, cc4, cc5, cc6, cc7, cc8, cc9, cc10 = cc_gen(cc, mes, ano, cvv)

    # Formatear el mensaje con las nuevas tarjetas generadas
    response = gen.format(
        cc1=cc1, cc2=cc2, cc3=cc3, cc4=cc4, cc5=cc5, cc6=cc6, cc7=cc7, cc8=cc8,
        cc9=cc9, cc10=cc10,
        bin=binif,
        country=country,
        country_name=country_name,
        country_flag=country_flag,
        name=msg.from_user.first_name or 'Usuario',
        bank=bank,
        vendor=vendor,
        type=type_,
        level=level,
        flag=country_flag
    )

    # Actualizar el mensaje con las nuevas tarjetas y mantener los botones
    await msg.edit_message_text(response, reply_markup=regene)
