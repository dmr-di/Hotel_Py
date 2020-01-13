import sqlite3

import variables, conexion

def limpiarLabel():
    variables.lbldnires.set_text('')
    variables.lblapelres.set_text('')
    variables.lblnoches.set_text('')

def limpiarEntry(fila):
    limpiarLabel()
    for i in range(len(fila)):
        fila[i].set_text('')
    variables.cbreshab.set_active(-1)


def listarreshab():
    try:
        conexion.cur.execute('SELECT numero FROM habitaciones')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listar():
    try:
        conexion.cur.execute('SELECT cod, dni, apel, nhab, chk_in, chk_out FROM reservas')
        listado = conexion.cur.fetchall()
        conexion.conex.commit()
        return listado
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadoreshab(listreshab):
    try:
        variables.listadoreshab = listarreshab()
        listreshab.clear()
        for registro in variables.listadoreshab:
            listreshab.append(registro)
    except:
        print('Error en cargar ComboBox')

def insertarres(fila):
    try:
        conexion.cur.execute("INSERT INTO reservas (dni, apel, nhab, chk_in, chk_out) VALUES (?,?,?,?,?)", fila)
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def listadores(listreservas):
    try:
        variables.listadores = listar()
        listreservas.clear()
        for registro in variables.listadores:
            listreservas.append(registro)
    except:
        print('Error en cargar treeview')

def bajares(cod):
    try:
        conexion.cur.execute('DELETE FROM reservas WHERE cod = ?', (cod,))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

#Esta función modifica los datos de una reserva
def modifres(registro):
    try:
        conexion.cur.execute('UPDATE reservas SET cod = ?, dni = ?, apel = ?, nhab = ?, chk_in = ?, chk_out = ? WHERE numero = ?', (registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[0]))
        conexion.conex.commit()
    except sqlite3.OperationalError as e:
        print(e)
        conexion.conex.rollback()

def selecregistro(nhab):
    try:
        conexion.cur.execute("select (select count(*) from habitaciones b where a.numero >= b.numero) as cnt from habitaciones a where numero = ?", (nhab,))
        nregistro = conexion.cur.fetchone()
        conexion.conex.commit()
        return nregistro
    except:
        print("Error en el numero de registro")

