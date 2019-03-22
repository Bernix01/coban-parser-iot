import logging
import socket
import time
from math import floor


def send_data(data_gram, socket_client):
    # Data device
    # Message tracking, may be the date
    device_id = data_gram["Dispositivo"]    # 0000 + telephone number
    latitud = to_dms(data_gram['Latitud'],'y')  # dddmm.mmmm format
    longitud = to_dms(data_gram['Longitud'])
    date = f"{data_gram['Fecha:yyyyMMdd'][2:]}{data_gram['hora']}"  # YYMMDDHHSS
    availability = 'A'
    # speed = '128.5'  # km/h
    times = time.strftime('%H%M%S')  # HHMMSS
    imei = get_imei(device_id)

    content = f",tracker,{date},,F,{times}.000,{availability},0{latitud[:-1]},{latitud[-1:]},{longitud[:-1]},{longitud[-1:]},,1,,,,,,"
    message = f"imei:{imei}{content};"

    logger = logging.getLogger('GPSTranslator')
    logger.debug('gprs_client-> send_all():data: %s', message)
    socket_client.sendall(message.encode('utf-8'))


def get_imei(device_id):
    ## returns an imei with a fixed prefix and a portion of the id (last 6 chars)
    ddid = device_id.replace("-", "")
    if len(ddid) > 6:
        ddid = ddid[-6:]
    return f"864180037{int(ddid):06d}"


def create_client(address, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((address, port))
        return sock
    except:
        logger = logging.getLogger('GPSTranslator')
        logger.debug('gprs_client-> Connect() %s', 'Connection failed')
        return None


def send_login(socket_client, device_id):
    imei = get_imei(device_id)
    logger = logging.getLogger('GPSTranslator')
    login_data = f"##,imei:{imei},A;"
    logger.debug('gprs_client-> login() data: %s', login_data)
    socket_client.sendall(login_data.encode('utf-8'))
    received = str(socket_client.recv(1024))
    logger = logging.getLogger('GPSTranslator')
    logger.debug('gprs_client-> send_all() %s', received)
    return True


def to_dms(dd, direction='x'):
    if type(dd) != 'float':
        try:
            decimaldegree = float(dd)
        except:
            print('\nERROR: Could not convert %s to float.' %
                  (type(dd)))
            return 0

    if direction == 'x':
        appendix = 'E'
    else:
        appendix = 'N'
    if direction == 'x' and decimaldegree < 0:
        appendix = 'W'
    elif decimaldegree < 0:
        appendix = 'S'
    if decimaldegree < 0:
        decimaldegree = -decimaldegree
    minutes = decimaldegree % 1.0*60
    seconds = minutes % 1.0*60
    return f"{int(floor(decimaldegree)):02d}{int(floor(minutes)):02d}.{int(floor((seconds/60)*10000))}{appendix}"
