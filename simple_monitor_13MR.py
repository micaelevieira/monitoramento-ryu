# Copyright (C) 2016 Nippon Telegraph and Telephone Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from operator import attrgetter

import simple_switch_13
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.lib import hub
import json


class SimpleMonitor13(simple_switch_13.SimpleSwitch13):

    def __init__(self, *args, **kwargs):
        super(SimpleMonitor13, self).__init__(*args, **kwargs)
        self.datapaths = {}

        self.port_stats = {}
        self.port_speed = {} # estrutura para medir a velocidade das portas
        
        self.flow_stats = {}
        self.flow_speed = {} # estrutura para medir a velocidade dos fluxos

        # thread para medir as informações sobre portas e fluxos
        self.monitor_thread = hub.spawn(self._monitor)
        

    # evento disparado quando está na fase de negociação com o switch, duas fases
    # de negociação são observadas (MAIN_DISPATCHER, DEAD_DISPATCHER).
    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        self.logger.info('--------------monitor----------------')
        self.logger.info("log state_change_handler_monitor")
        datapath = ev.datapath
        #se a fase de negociacao é MAIN_DISPATCHER:
        if ev.state == MAIN_DISPATCHER:
            # verifica se o switch não está na lista de datapaths
            if datapath.id not in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                # em caso positivo, adiciona-o
                self.datapaths[datapath.id] = datapath
        #se a fase de negociação é DEAD_DISPATCHER:
        elif ev.state == DEAD_DISPATCHER:
            # verifica se o switch está na lista de datapaths
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                # em caso positivo, remove-o
                del self.datapaths[datapath.id]

    def _monitor(self):
        while True:
            for dp in self.datapaths.values():
                self._request_stats(dp)
            hub.sleep(5)

    def _request_stats(self, datapath):
        self.logger.debug('send stats request: %016x', datapath.id)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    def salvar_estatistica(self, dict_estatistica, key, value):
        # se a chave do fluxo não existe, cria uma lista vazia
        if key not in dict_estatistica:
            dict_estatistica[key] = []

        # adiciona as estatisticas(value) na lista de fluxos do switch, 
        # na chave criada, ou que já existe    
        dict_estatistica[key].append(value)

        # se o tamanho da lista de estatísticas medidas do fluxo
        # for maior que 5, remove a mais antiga
        if len(dict_estatistica[key]) > 5:
            dict_estatistica[key].pop(0)

    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        self.logger.info('--------------monitor----------------')
        self.logger.info('log flow_stats_reply_handler')
        
        body = ev.msg.body
        dpid = ev.msg.datapath.id
        
        #self.logger.info(json.dumps(ev.msg.to_jsondict(),ensure_ascii=True,indent=3,sort_keys=True))



        self.flow_stats.setdefault(dpid, {})
        self.flow_speed.setdefault(dpid, {})

        

        # percorrendo lista de statisticas dos flows
        for stat in body:
            # se a prioridade do flow é 1
            if stat.priority:
                # a chave do flow é uma tupla(porta de entrada, ip destino, porta destino*)
                key = (stat.match['in_port'],  stat.match.get('eth_dst'),
                    stat.instructions[0].actions[0].port)
                # valor relacionado a chave 
                value = {
                    "packet_count": stat.packet_count, 
                    "byte_count": stat.byte_count,
                    "duration_sec": stat.duration_sec, 
                    "duration_nsec": stat.duration_nsec
                }

                # salva a estatísitca de fluxo
                self.salvar_estatistica(self.flow_stats[dpid], key, value)

                self.logger.info('adicionando {} -> {}'.format(key, value))


                # calcular estatísticas de velocidade
                tmp = self.flow_stats[dpid][key]
                if len(tmp) > 1:
                    pre_byte_count = tmp[-2]["byte_count"]
                    curr_byte_count = tmp[-1]["byte_count"]
                    period = (tmp[-1]["duration_sec"] + tmp[-1]["duration_nsec"] / (10 ** 9)) - (tmp[-2]["duration_sec"] + tmp[-2]["duration_nsec"] / (10 ** 9))

                    speed = 0
                    if period != 0:
                        speed = (curr_byte_count - pre_byte_count) / period

                    # salva a estatística de velocidade
                    self.salvar_estatistica(self.flow_speed[dpid], key, speed)

                    self.logger.info(">>>> SPEED: {}".format(speed))


        '''self.logger.info('datapath         '
                         'in-port  eth-dst           '
                         'out-port packets  bytes')
        self.logger.info('---------------- '
                         '-------- ----------------- '
                         '-------- -------- --------')
        for stat in sorted([flow for flow in body if flow.priority == 1],
                           key=lambda flow: (flow.match['in_port'],
                                             flow.match['eth_dst'])):
            self.logger.info('%016x %8x %17s %8x %8d %8d',
                             ev.msg.datapath.id,
                             stat.match['in_port'], stat.match['eth_dst'],
                             stat.instructions[0].actions[0].port,
                             stat.packet_count, stat.byte_count)'''

    @set_ev_cls(ofp_event.EventOFPPortStatsReply, MAIN_DISPATCHER)
    def _port_stats_reply_handler(self, ev):
        self.logger.info('--------------monitor---------')
        self.logger.info('log  port_stats_reply_handler')
        body = ev.msg.body

        '''self.logger.info('datapath         port     '
                         'rx-pkts  rx-bytes rx-error '
                         'tx-pkts  tx-bytes tx-error')
        self.logger.info('---------------- -------- '
                         '-------- -------- -------- '
                         '-------- -------- --------')
        for stat in sorted(body, key=attrgetter('port_no')):
            self.logger.info('%016x %8x %8d %8d %8d %8d %8d %8d',
                             ev.msg.datapath.id, stat.port_no,
                             stat.rx_packets, stat.rx_bytes, stat.rx_errors,
                             stat.tx_packets, stat.tx_bytes, stat.tx_errors)'''