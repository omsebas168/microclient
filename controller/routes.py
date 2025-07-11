from flask import Blueprint, request, jsonify
from usecases import  use_cases_client
from entities.model import Client
import logging

client_bp=Blueprint("client_bp", __name__)
request_mapping="/client"

@client_bp.route(request_mapping, methods=["POST"])
def insert():
    json=request.get_json()
    if not json:
        logging.warning("empty body insert")
        return {"message": "empty body"}, 400
    try:
        if use_cases_client.insert(Client(**json)):
            logging.info("OK INSERT")
            return {"message": "inserted"}, 201
    except Exception as ex:
        logging.error("ERROR INSERT: {%s}", ex)
    
    return {"message": "server error"}, 500

@client_bp.route(request_mapping, methods=["GET"])
def select():
    try:
        data=use_cases_client.select_all()
        if data:
            dictionary=[{"id":t.id, "name": t.name, "address": t.address, "email": t.email} for t in data]
            logging.info("GET ALL CLIENTS OK")
            return jsonify(dictionary)
    except Exception as ex:
        logging.error("ERROR GET ALL CLIENTS {%s}", ex)
    return {"message": "server error"}, 500

@client_bp.route(request_mapping, methods=['DELETE'])
def delete():
    id=request.args["id"]
    if not id:
        logging.warning("QUERY PARAMETER ID DOESN'T EXIST DELETE")
        return {"message": "must be exists query parameter id"}
    try:
        if use_cases_client.deleted_by_id(id):
            logging.info("DELETE OK")
            return {"message": "OK"}, 200
        else:
            logging.info("ID {%s} DOESN'T EXISTS DELETE", id)
            return {"message": "client {%s}".format(id)}
    except Exception as ex:
        logging.error("ERROR DELETE {%s}", ex)
    return {"message": "server error"}, 500

@client_bp.route(request_mapping, methods=["PUT"])
def update():
    data=request.get_json()
    if not data:
        logging.warning("body empty update")
        return {"message": "empty body"}, 400
    try:
        if use_cases_client.update(Client(**data)):
            logging.info("UPDATE OK")
            return {"message": "OK"}, 200
        else:
            logging.warning("CLIENT {%s} DOESN'T EXISTS", data['id'])
            return {"message":"CLIENT DOESN'T EXISTS"}, 404
    except Exception as ex:
        logging.error("ERROR UPDATE {%s}", ex)
    return {"message":"server error"}, 500

