# EFI2022 Progamacion 1.
import sys
from vista.interfaz import *
from modelo.adminDB import *
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QAbstractItemView

class Controles():
    def __init__(self):
        self.userInterface=MainKiosko() # instancia de la interfaz.

    # Botones para retroceder pagina.
        self.userInterface.botonAtrasEnAjustes.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaMenu))
        self.userInterface.botonAtrasEnActualizar.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaMenu))
        self.userInterface.botonAtrasEnEliminar.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaMenu))
        self.userInterface.botonAtrasEnInfo.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaMenu))
        self.userInterface.botonAtrasEnRegistrar.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaMenu))
        self.userInterface.botonAtrasEnStock.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaMenu))

    # Botones para acceder a las paginas.
        self.userInterface.botonInicial.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaMenu))
        self.userInterface.botonStock.clicked.connect(self.paginaStock)
        self.userInterface.botonRegistrar.clicked.connect(self.paginaRegistrar)
        self.userInterface.botonActualizar.clicked.connect(self.paginaActualizar)
        self.userInterface.botonEliminar.clicked.connect(self.paginaEliminar)
        self.userInterface.botonAjustes.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaAjustes))
        self.userInterface.botonInfo.clicked.connect(lambda:self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaInfo))
     
    def mostrarRegistros(self,tabla): # mustra los datos de la DB en la tabla de cada pagina.
        df=leerTabla() # lee la DB.
        tabla.setRowCount(len(df))
        for registro, numReg in zip(df,range(len(df))):
            for campo,numCampo in zip(registro,range(len(registro))):
                    tabla.setItem(numReg,numCampo,QTableWidgetItem(str(campo)))
        
                    tabla.resizeColumnsToContents() # adapta el contenida de las columnas de izquierda a derecha.
        tabla.setSelectionBehavior(QAbstractItemView.SelectRows)  # selecciona todo el registro (fila).

    def buscar(self): # funcion de los buscadores en las Pagina Stock,Actualizar y Eliminar.
        producto = self.userInterface.inputBuscarEnStock.text().lower()
        for row in range(self.userInterface.tablaStock.rowCount()):
            item1 = self.userInterface.tablaStock.item(row, 1)
            self.userInterface.tablaStock.setRowHidden(row, producto not in item1.text().lower())

        producto = self.userInterface.inputBuscarEnActualizar.text().lower()
        for row in range(self.userInterface.tablaActualizar.rowCount()):
            item2 = self.userInterface.tablaActualizar.item(row, 1)
            self.userInterface.tablaActualizar.setRowHidden(row, producto not in item2.text().lower())

        producto = self.userInterface.inputBuscarEnEliminar.text().lower()
        for row in range(self.userInterface.tablaEliminar.rowCount()):
            item3 = self.userInterface.tablaEliminar.item(row, 1)
            self.userInterface.tablaEliminar.setRowHidden(row, producto not in item3.text().lower())

    def seleccionRow(self): # seleciona el registro y coloca los campos en las LineEdit para editarlos.
        self.row = self.userInterface.tablaActualizar.selectedItems() # obtiene el registro.
        widgets=[self.userInterface.labelIdEnActualizar, self.userInterface.inputProductoEnActualizar,self.userInterface.inputMarcaEnActualizar,self.userInterface.inputPrecioEnActualizar,self.userInterface.inputStockEnActualizar,self.userInterface.inputInflacionEnActualizar]
        for num in range(6):
            widgets[num].setText(f"{self.row[num].text()}")

    def actualizaDB(self): # Actualiza la DB.
        camposValores={'Producto':self.userInterface.inputProductoEnActualizar.text(),'Marca':self.userInterface.inputMarcaEnActualizar.text(),'Precio':int(self.userInterface.inputPrecioEnActualizar.text()),'Stock':int(self.userInterface.inputStockEnActualizar.text()),'Inflacion':int(self.userInterface.inputInflacionEnActualizar.text())}

        for campo in camposValores:
            actualizar('id',int(self.userInterface.labelIdEnActualizar.text()),campo,camposValores[campo])
        
        self.userInterface.labelConfirmacionActualizado.setText("Registro actualizado") # etiqueta confirmacion de actualizacion.
        self.mostrarRegistros(self.userInterface.tablaActualizar)

    def cargaRegistroDB(self): # carga un nuevo registro en la DB.
        producto=self.userInterface.inputProductoEnRegistrar.text()
        marca=self.userInterface.inputMarcaEnRegistrar.text()
        precio=int(self.userInterface.inputPrecioEnRegistrar.text())
        stock=int(self.userInterface.inputStockEnRegistrar.text())
        inflacion=int(self.userInterface.inputInflacionEnRegistrar.text())
        insertarRegistro([(producto,marca,precio,stock,inflacion)])
        self.userInterface.labelConfirmacionDeRegistro.setText("Registrado")

    def eliminar(self): # elimina un refistro de la DB.
        campoSeleccionado = self.userInterface.tablaEliminar.selectedItems()
        if campoSeleccionado:
            fila = campoSeleccionado[0].row()
            id = self.userInterface.tablaEliminar.item(fila,0).text()
            self.userInterface.tablaEliminar.removeRow(fila)
            self.userInterface.tablaEliminar.clearSelection()
            borrar(id)
            self.userInterface.labelConfirmacionEliminado.setText(f"Registro Eliminado")
        else:
            self.userInterface.labelConfirmacionEliminado.setText(f"¡Seleccione un Producto!")

    def paginaStock(self): # funcionalidades de la pagina Stock.
        self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaStock) # Mustra la pagina de Stock de la interfaz.
        self.mostrarRegistros(self.userInterface.tablaStock) # llamada a la funcion que muestra los registros en la tabla.
        self.userInterface.inputBuscarEnStock.textChanged.connect(self.buscar) # llamada a la funcion buscar del buscador en esta pagina.

    def paginaRegistrar(self): # funcionalidades de la pagina Registrar.
        self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaRegistrar) # Mustra la pagina de Registrar de la interfaz.
        self.userInterface.botonRegistrarEnRegistrar.clicked.connect(self.cargaRegistroDB) # llamada a la funcion que carga un nuevo registro en la DB.

    def paginaActualizar(self): # funcionalidades de la pagina Actualizar.
        self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaActualizar) # Mustra la pagina de Actualizar de la interfaz.
        self.mostrarRegistros(self.userInterface.tablaActualizar)
        self.userInterface.tablaActualizar.itemClicked.connect(self.seleccionRow) # seleccion con click sobre el registro.
        self.userInterface.botonActualizarEnActualizar.clicked.connect(self.actualizaDB) # llamada a la funcion que actualiza la DB.
        self.userInterface.inputBuscarEnActualizar.textChanged.connect(self.buscar)
        
    def paginaEliminar(self): # funcionalidades de la pagina Eliminar.
        self.userInterface.paginas.setCurrentWidget(self.userInterface.paginaEliminar) # Mustra la pagina de Eliminar de la interfaz.
        self.mostrarRegistros(self.userInterface.tablaEliminar)
        self.userInterface.botonEliminarEnEliminar.clicked.connect(self.eliminar) # llamada a la funcion que elimina el registro de la DB.
        self.userInterface.inputBuscarEnEliminar.textChanged.connect(self.buscar)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Controles()
    sys.exit(app.exec_())