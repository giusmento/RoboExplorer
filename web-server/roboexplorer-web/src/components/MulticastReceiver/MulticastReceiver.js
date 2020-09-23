import React from "react";
var dgram = require('dgram');


function MulticastReceiver() {
      
    //Multicast Client receiving sent messages
    var PORT = 41848;
    var MCAST_ADDR = "230.185.192.108"; //same mcast address as Server
    var HOST = '192.168.1.9'; //this is your own IP
    
    console.log(dgram)
    var client =  dgram.createSocket('udp4');
    
    connect();

    function connect() {
        //var client = dgram.createSocket('udp4');
        this.state.client.on('listening', function () {
            var address = client.address();
            console.log('UDP Client listening on ' + address.address + ":" + address.port);
            client.setBroadcast(true)
            client.setMulticastTTL(128); 
            client.addMembership(MCAST_ADDR);
        });
        
        this.state.client.on('message', function (message, remote) {   
            console.log('MCast Msg: From: ' + remote.address + ':' + remote.port +' - ' + message);
        });
        
        this.state.client.bind(PORT, HOST)
    }

}
export default MulticastReceiver;
