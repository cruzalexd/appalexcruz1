from flask import Flask ,jsonify,request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)
CORS(app)
# configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://sql10508515:QrWmDMJb2V@sql10.freemysqlhosting.net/sql10508515'#ACA CONFIGURAR LA BASE DE DATOS
#                                               user:clave@localhost/nombreBaseDatos

'''
Server: sql10.freemysqlhosting.net
Name: sql10508515
Username: sql10508515
Password: QrWmDMJb2V
Port number: 3306



'''




app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False#root:root@localhost/flaskmysql' ESTO VA EN LA LINEA 8 Y LO BORRE PARA PROBAR
db= SQLAlchemy(app)
ma=Marshmallow(app)
# defino la tabla
class Producto(db.Model):   # la clase Producto hereda de db.Model     
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(500))#Esto se cambio a 500 y antes era 100, esta en el video 2 donde dice el cambio
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    def __init__(self,nombre,precio,stock):   #crea el  constructor de la clase
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento
        self.precio=precio
        self.stock=stock
 
db.create_all()  # crea las tablas
#  ************************************************************
 
class ProductoSchema(ma.Schema):
    class Meta:
        fields=('id','nombre','precio','stock')
producto_schema=ProductoSchema()            # para crear un producto
productos_schema=ProductoSchema(many=True)  # multiples registros


@app.route('/')
def index():
    return "<h1>Corriendo servidor Flask</h1>"



 
 
# crea los endpoint o rutas (json)
@app.route('/productos',methods=['GET'])
def get_Productos():
    all_productos=Producto.query.all()     # query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # .dump() lo hereda de ma.schema
    return jsonify(result)
 
 
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id):
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)

 
@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)

#ESTO SE AGREGADO PARA EL POST, LO PUSE ACA
@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    new_producto=Producto(nombre,precio,stock)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)
#ESTO SE AGREGADO PARA EL POST, LO PUSE ACA

#ESTO ES EL PUT

@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
   
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
 
    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    db.session.commit()
    return producto_schema.jsonify(producto)
# FIN DEL PUT

  
# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True)#, port=5000) #SE SACO EL PUERTO 











    