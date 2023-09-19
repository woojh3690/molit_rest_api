# -- coding: utf-8 --

from flask import Flask, request, Response
from flask_restx import Resource, Api

from kafka import KafkaProducer

import jpype

from util.Config import Config
from util.Log_manager import LogManger
from util.RPCDriver import RPCClient

import os
import sys
import uuid
import json

_config = Config(config_path = "/root/rest_api/conf/RestApiConfig.yaml")
_config.load_config()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트
api = Api(app)

@api.route('/rest_api_insert')
class RestApiCrawl(Resource):

    global _config

    _rest_api_crawl_config = _config._rest_api_crawl_config
    _log = LogManger("rest_api_insert")
    _log = _log.file_handler(file_path=_rest_api_crawl_config._basic_api_config._log_path+"/rest_api_insert.log", mode="a", level=_rest_api_crawl_config._basic_api_config._log_level)

    _producer = KafkaProducer(
        bootstrap_servers=_rest_api_crawl_config._kafka_producer_config._bootstrap_servers, 
        value_serializer=str.encode
    )

    def post(self):
        try:
            websocket_id = str(uuid.uuid1())

            if request.headers['REST_API_KEY'] not in self._rest_api_crawl_config._rest_api_key_dict:
                err_msg = "[ErrorCode-412] Http header REST_API_KEY Wrong"
                self._log.error("[" + websocket_id + "] " + err_msg)
                return Response(err_msg, status=412)

            if "application/json" not in request.headers['CONTENT_TYPE']:
                err_msg = "[ErrorCode-412] Http header CONTENT_TYPE Wrong"
                self._log.error("[" + websocket_id + "] " + err_msg)
                return Response(err_msg, status=412)

            self._log.debug("[" +  websocket_id + "] # 1. Insert Message Received")
            msg = request.json
            msg = json.dumps(msg)

            self._log.debug("[" +  websocket_id + "] # 2. Send Message To Commander = " + msg)
            self._producer.send(self._rest_api_crawl_config._kafka_producer_config._topic_name, msg)
            self._producer.flush()
        except Exception as e:
            err_msg = "[ErrorCode-520] Unexpected error: " + e.__str__()
            self._log.error("[" + websocket_id + "] " + err_msg)
            return Response(status=520)
        
        self._log.debug("[" +  websocket_id + "] # 3. Send Message Success")
        return Response(status=200)

@api.route('/rest_api_select')
class RestApiSelect(Resource):

    global _config

    _rest_api_sel_config = _config._rest_api_sel_config
    _log = LogManger("rest_api_select")
    _log = _log.file_handler(
        file_path = _rest_api_sel_config._basic_api_config._log_path + "/rest_api_select.log", 
        mode = "a", level = _rest_api_sel_config._basic_api_config._log_level)

    def post(self):
        try:
            websocket_id = str(uuid.uuid1())
            ret = request.headers['REST_API_KEY'] in self._rest_api_sel_config._rest_api_key_dict

            if ret == True:
                if "application/json" in request.headers['CONTENT_TYPE']:
                    
                    self._log.debug("[" +  websocket_id + "] # 1. Receive Search Message")
                    msg = request.json

                    self._log.debug("[" + websocket_id + "] # 1-1. Make WebSession UUID")
                    msg["msg"][0]["msg_header"]["websocket_id"] = websocket_id
                    msg = json.dumps(msg)
                    self._log.debug("[" + websocket_id + "] # 1-1. Msg = " + msg)

                    rpc_client = RPCClient(self._rest_api_sel_config._rabbitmq_rpc_config)

                    self._log.debug("[" + websocket_id + "] # 1-2. Send Msg To RPC Queue")
                    rpc_client.send(msg)

                    self._log.debug("[" + websocket_id + "] # 2. Wait Search Result Message Received")
                    message = rpc_client.receive()

                    self._log.debug("[" + websocket_id + "] # 2. RPC Client Close")
                    rpc_client.close()

                    self._log.debug("[" + websocket_id + "] # 2-1. Parse Msg start")
                    result = str(message, 'utf-8')
                    self._log.debug("[" + websocket_id + "] # 2-1. Parse Msg = " + result)
                    result_msg = json.loads(result)
                    
                    ret_msg_err_code = result_msg["msg"][0]["msg_header"]["msg_err_code"]
                    if(not ret_msg_err_code == "0"):
                        result_msg = json.dumps(result_msg)
                        self._log.error("[" + websocket_id + "] #  if(not ret_msg_err_code == 0)")
                        return Response(result_msg, content_type="application/json", status=412)
                    
                    ret_websocket_id = result_msg["msg"][0]["msg_header"]["websocket_id"]
                    ret_msg_type = result_msg["msg"][0]["msg_header"]["msg_type"]
                    
                    self._log.debug("[" + websocket_id + "] # 3. Send Search Result")
                    del(result_msg["msg"][0]["msg_header"]["websocket_id"])

                    if ret_msg_type == "select" :
                        self._log.debug("[" + websocket_id + "] # 3-1 IF Search Result - limit")
                        result_msg = json.dumps(result_msg)
                        self._log.debug("[" + websocket_id + "] # 3-2 Return Search Result - limit")
                        return Response(result_msg, content_type="application/json", status=200)
                    else:
                        self._log.error("[" + websocket_id + "] #  ret_msg_type wrong = " + ret_msg_type)
                        return Response(result_msg, content_type="application/json", status=412)
                else:
                    err_msg = "[ErrorCode-421] Http header CONTENT_TYPE Wrong"
                    self._log.error("[" + websocket_id + "] " + err_msg)
                    return Response(err_msg, status=412)
            else:
                err_msg = "[ErrorCode-421] Http header REST_API_KEY Wrong"
                self._log.error("[" + websocket_id + "] " + err_msg)
                return Response(err_msg, status=412)
        except Exception as e:
            err_msg = "[ErrorCode-520] Unexpected error: " + e.__str__()
            self._log.error("[" + websocket_id + "] " + err_msg)
            return Response(status=520)

@api.route('/rest_api_cmd')
class RestApiCmd(Resource):

    global _config

    _rest_api_cmd_config = _config._rest_api_cmd_config
    _log = LogManger("rest_api_cmd")
    _log = _log.file_handler(file_path = _rest_api_cmd_config._basic_api_config._log_path + "/rest_api_cmd.log", 
        mode = "a", level = _rest_api_cmd_config._basic_api_config._log_level)

    def post(self):
        try:
            websocket_id = str(uuid.uuid1())

            if request.headers['REST_API_KEY'] not in self._rest_api_cmd_config._rest_api_key_dict:
                err_msg = "[ErrorCode-421] Http header REST_API_KEY Wrong"
                self._log.error("[" + websocket_id + "] " + err_msg)
                return Response(err_msg, status=412)

            if "application/json" not in request.headers['CONTENT_TYPE']:
                err_msg = "[ErrorCode-421] Http header CONTENT_TYPE Wrong"
                self._log.error("[" + websocket_id + "] " + err_msg)
                return Response(err_msg, status=412)

            self._log.debug("[" +  websocket_id + "] # 1. Receive Search Message")
            msg = request.json
            msg["msg"][0]["msg_header"]["websocket_id"] = websocket_id

            # 커멘더에 처리 요청
            rpc_client = RPCClient(self._rest_api_cmd_config._rabbitmq_rpc_config)
            rpc_client.send(json.dumps(msg))
            message = rpc_client.receive()
            rpc_client.close()

            # 웹소켓 아이디 지우고 응답 완료
            result_msg = json.loads(str(message, 'utf-8'))
            ret_websocket_id = result_msg["msg"][0]["msg_header"]["websocket_id"]
            if websocket_id == ret_websocket_id:
                del(result_msg["msg"][0]["msg_header"]["websocket_id"])
                self._log.debug("[" + websocket_id + "] # Return CMD Result - limit")                  
                return Response(json.dumps(result_msg), content_type="application/json", status=200)

        except Exception as e:
            err_msg = "[ErrorCode-520] Unexpected error: " + e.__str__()
            self._log.error("[" + websocket_id + "] " + err_msg)
            return Response(status=520)

if __name__ == "__main__":
    # 앱 시작
    app.run(debug=False, host='0.0.0.0', port=7888)
