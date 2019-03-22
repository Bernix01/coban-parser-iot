def Convetir_decimal(s):
    s = int(s)
    return s


def Hex_decimal(s):
    n = int(s, 16)
    return n


def signo(s):
    if s == "0":
        return "-"
    elif s == "1":
        return "+"


def generarDatosPeticion(c1):
    datos = {}
    actual = 0
    inicio = c1[0:2]
    actual = actual+2
    longCampo = c1[actual:actual+2]
    actual = actual+2
    longCampo = Hex_decimal(longCampo)
    actual = longCampo+4
    dispositivo = c1[4:actual]
    print("#Serie de dispositivo", dispositivo)
    # Latitud
    nsimb = c1[actual+1]
    actual = actual+1
    signoLat = signo(nsimb)
    lclatitud = c1[actual:actual+2]
    actual = actual+2
    lclatitud = Hex_decimal(lclatitud)
    lclatitudDec = c1[actual:actual+2]
    lclatitudDec = Hex_decimal(lclatitudDec)
    actual = actual+2
    vLatitud = c1[actual:actual+lclatitud]
    actual = actual+lclatitud
    vLatitudDec = c1[actual:actual+lclatitudDec]
    actual = actual+lclatitudDec
    print("latitud: %s%s%s%s" % (signoLat, vLatitud, ".", vLatitudDec))
    latitud = signoLat+vLatitud+"."+vLatitudDec
    # Longitud
    nsimblong = c1[actual:actual+1]
    actual = actual+1
    simblong = signo(nsimblong)
    lclongitud = c1[actual:actual+2]
    actual = actual+2
    lclongitud = Hex_decimal(lclongitud)
    lclongitudDec = c1[actual:actual+2]
    lclongitudDec = Hex_decimal(lclongitudDec)
    actual = actual+2
    vLongitud = c1[actual:actual+lclongitud]
    actual = actual+lclongitud
    vLongitudDec = c1[actual:actual+lclongitudDec]
    actual = actual+lclongitudDec

    print("longitud: %s%s%s%s" % (simblong, vLongitud, ".", vLongitudDec))
    longitud = simblong+vLongitud+"."+vLongitudDec
    # Fecha
    fecha = c1[actual:actual+8]
    actual = actual+8
    hora = c1[actual:actual+6]
    actual = actual+6
    print("Fecha:yyyyMMdd", fecha)
    print("hora,", hora)
    # Posiciones
    lcIDpos = c1[actual:actual+2]
    lcIDpos = Hex_decimal(lcIDpos)
    actual = actual+2
    idpos = c1[actual:actual+lcIDpos]
    print("Identificador de posicion: ", idpos)
    actual = actual+lcIDpos
    lidposanterior = c1[actual:actual+2]
    actual = actual+2
    lidposanterior = Hex_decimal(lidposanterior)
    idposanterior = c1[actual:actual+lidposanterior]
    actual = actual+lidposanterior
    print("Identificador de poscion anterior:", idposanterior)
    # MENSAJE
    ltmensaje = c1[actual:actual+2]
    ltmensaje = Hex_decimal(ltmensaje)
    actual = actual+2
    tipomensaje = c1[actual:actual+ltmensaje]
    print("Tipo de Mensaje:", tipomensaje)
    actual = actual+ltmensaje
    lmensaje = c1[actual:actual+3]
    lmensaje = Hex_decimal(lmensaje)
    actual = actual+3
    mensaje = c1[actual:actual+lmensaje]
    print("Mensaje: ", mensaje)
    datos["Trama"] = inicio
    datos["Dispositivo"] = dispositivo
    datos["Latitud"] = latitud
    datos["Longitud"] = longitud
    datos["Fecha:yyyyMMdd"] = fecha
    datos["hora"] = hora
    datos["ID Posicion actual"] = idpos
    datos["ID posicion anterior"] = idposanterior
    datos["Tipo de Mensaje"] = tipomensaje
    datos["Mensaje"] = mensaje
    return datos


def generar_respuesta(d):
    respuesta = "$$"
    idposicion = d["ID Posicion actual"]
    longID = format(len(idposicion), 'x')
    if len(longID) == 1:
        longID = "0" + longID
    respuesta += longID
    respuesta += idposicion

    return respuesta
