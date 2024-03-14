from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

# inisialisasi object flask
app = Flask(__name__)

#  inisialisasi object flask_restfull
api = Api(app)

#  inisialisasi object flask_cors
CORS(app)

# inisialisasi variabel global kosong tipe dicrionary
identitas = {} 

# buat class resource
class MyResource(Resource):
    # method get dan post
    def get(self):
        # response = {"messages":"Halo Guys"}
        # return response
        return identitas

    def post(self):
        nama = request.json["nama"]
        umur = request.json["umur"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        response = {"messages":"Berhasil menambahkan data"}
        return response
    
#  setup resource nya
api.add_resource(MyResource, "/home", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=8080)