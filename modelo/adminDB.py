import sqlite3 as db

def openCloseDB(func):
    def funcionDec(*args,**kwargs):
        conn = db.connect("modelo/kioskoDB.db")
        cursor = conn.cursor()

        data=func(cursor,*args,**kwargs)

        conn.commit()
        conn.close()
        return data
    return funcionDec

@openCloseDB
def crearDB(cursor):
    campos=('Producto text','Marca text', 'Precio integer','Stock integer', 'Inflacion integer')
    cursor.execute(f"CREATE TABLE Productos ('id' integer primary key autoincrement, {','.join(campos)})")

@openCloseDB
def insertarRegistro(cursor,registros):
    cursor.executemany(f"INSERT INTO Productos VALUES (NULL,{','.join('?'*len(registros[0]))})",registros)

@openCloseDB
def leerTabla(cursor):
    df=cursor.execute(f"SELECT * FROM Productos").fetchall()
    return df

@openCloseDB
def buscarRegistros(cursor, valorBuscado, campoEnDondeBuscar="Producto", comparacion='like',aprox='%'):
    df=cursor.execute(f"SELECT * FROM Productos WHERE {campoEnDondeBuscar} {comparacion} '{valorBuscado}{aprox}'").fetchall() # por defecto aproxima.
    return df

@openCloseDB
def actualizar(cursor,campoDelRegistro, registro, campoAModificar, newValor):
    cursor.execute(f"UPDATE Productos SET {campoAModificar}='{newValor}' WHERE {campoDelRegistro} like '{registro}%'") 

@openCloseDB
def borrar(cursor,id):
    cursor.execute(f"DELETE FROM Productos WHERE id={id}")


if __name__=='__main__':

    dataFake=[('Yerba','Nobleza Gaucha',500,10,3), ('Yerba','Taragüi',320,5,2),('Yerba','CBC',400,7,2),
    ('Yerba','Playadito',320,5,2),('Yerba','Canarias',300,5,2),('Yerba','Rosamonte',300,5,2),('Fideo','Marolio',100,5,4),
    ('Fideo','Lucchetti',150,10,4),('Fideo','Matarazzo',170,12,4),('Fideo','Barilla',160,10,4),
    ('Azúcar','Arcor',100,10,6),('Azúcar','Domino',90,7,6),('Leche','Ramolac',200,7,6),('Leche','Arcor',190,5,6),
    ('Leche','Manfrey',150,7,6),('Oregano','Alicante',70,12,2),('Arroz','Gallo',100,12,3),('Arroz','Lucchetti',110,12,3),
    ('Mermelada','Canale',70,12,3),('Miel','Abejita',200,11,1),('Shampoo','Plusbelle',320,13,3),
    ('Mortadela','Paladini',300,3,10),('Mortadela','Amatriciana',450,6,7),('Jabon neutro','Dove',70,12,10),
    ('Jabon blanco','ala',80,7,10),('Yerba','Union',300,4,2),('Yerba','La Merced',360,4,1),('Jabon en polvo','ala',110,5,9),
    ('Jabon en polvo','Ariel',170,3,7),('Detergente','Magistral',140,2,4),('Detergente','Cif',130,8,8)]
    
    try:
        crearDB()
    except:
        print('La Base de datos con esa tabla ya existe.')
    
    #insertarRegistro(dataFake)

    #print(buscarRegistros('leche'))

    #actualizar('Marca','marolio','Precio',150)

    #borrar(19)

    #print(leerTabla())