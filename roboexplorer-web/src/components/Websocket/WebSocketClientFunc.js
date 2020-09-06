import React from "react";
import { useWebSocketBroadcastDispatchContext } from "./WebSocketBroadcastContext.react";
import { useWebSocketConnectionDispatchContext } from "./WebSocketConnectionContext.react";

function WebSocketClientFunc() {
  // constructor(props) {
  //   super(props);
  //   console.log(props);
  //   this.state = {
  //     ws: null,
  //   };
  //   console.log("WebSocket constructor");
  // }

  // single websocket instance for the own application and constantly trying to reconnect.
  // async componentDidMount() {
  //   this.connect();
  // }

  var timeout = 250; // Initial timeout duration as a class variable
  var broadcastDispatch = useWebSocketBroadcastDispatchContext();
  var connectionDispatch = useWebSocketConnectionDispatchContext();
  var ws = new WebSocket("ws://localhost:6789/");
  connect();
  /**
   * @function connect
   * This function establishes the connect with the websocket and also ensures constant reconnection if connection closes
   */
  function connect() {
    //connectionDispatch({ type: "connect", ws: ws });
    // console.log(this);
    // this.props.setWs(ws);
    var connectInterval;

    // websocket onopen event listener
    ws.onopen = () => {
      console.log("connected websocket main component");

      //this.setState({ ws: ws });

      timeout = 250; // reset timer to 250 on open of websocket connection
      clearTimeout(connectInterval); // clear Interval on on open of websocket connection
    };

    ws.onmessage = (message) => {
      //console.log(message.data);
      //broadcastDispatch({ message: message.data });
    };

    // websocket onclose event listener
    ws.onclose = (e) => {
      console.log(
        `Socket is closed. Reconnect will be attempted in ${Math.min(
          10000 / 1000,
          (timeout + timeout) / 1000
        )} second.`,
        e.reason
      );

      timeout = timeout + timeout; //increment retry interval
      connectInterval = setTimeout(check, Math.min(10000, timeout)); //call check function after timeout
    };

    // websocket onerror event listener
    ws.onerror = (err) => {
      console.error(
        "Socket encountered error: ",
        err.message,
        "Closing socket"
      );

      ws.close();
    };
  }
  var send = ws.send.bind(ws);
  /**
   * utilited by the @function connect to check if the connection is close, if so attempts to reconnect
   */
  var check = () => {
    //const { ws } = this.state;
    if (!ws || ws.readyState === WebSocket.CLOSED) connect(); //check if websocket instance is closed, if so call `connect` function.
  };

  return null;
}

export default WebSocketClientFunc;
