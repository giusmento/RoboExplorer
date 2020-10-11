import React from "react";
import { WebSocketContext } from "../Context/WebSocketContext";

class WebSocketClient extends React.Component {
  constructor(props) {
    super(props);
    console.log(props);
    this.state = {
      ws: new WebSocket("ws://localhost/"),
      websocket_message: null,
    };
    console.log("WebSocket constructor");
  }

  // single websocket instance for the own application and constantly trying to reconnect.
  async componentDidMount() {
    this.connect();
  }

  webServerHost = "192.168.1.190";
  webServerPort = "6790";

  timeout = 250; // Initial timeout duration as a class variable
  /**
   * @function connect
   * This function establishes the connect with the websocket and also ensures constant reconnection if connection closes
   */
  connect = () => {
    var ws = new WebSocket(
      "ws://" + this.webServerHost + ":" + this.webServerPort + "/"
    );
    // console.log(this);
    // this.props.setWs(ws);
    var connectInterval;

    // websocket onopen event listener
    ws.onopen = () => {
      console.log("connected websocket main component");

      this.setState({ ws: ws });
      ws.send("Hello");
      this.timeout = 250; // reset timer to 250 on open of websocket connection
      clearTimeout(connectInterval); // clear Interval on on open of websocket connection
    };

    ws.onmessage = (message) => {
      //console.log(message.data);
      // this.setState(
      //   {websocket_message: message}
      // )
      //this.dispatch({ message: message.data });
    };

    // websocket onclose event listener
    ws.onclose = (e) => {
      console.log(
        `Socket is closed. Reconnect will be attempted in ${Math.min(
          10000 / 1000,
          (this.timeout + this.timeout) / 1000
        )} second.`,
        e.reason
      );

      this.timeout = this.timeout + this.timeout; //increment retry interval
      connectInterval = setTimeout(this.check, Math.min(10000, this.timeout)); //call check function after timeout
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
  };

  /**
   * utilited by the @function connect to check if the connection is close, if so attempts to reconnect
   */
  check = () => {
    const { ws } = this.state;
    if (!ws || ws.readyState === WebSocket.CLOSED) this.connect(); //check if websocket instance is closed, if so call `connect` function.
  };

  render() {
    // return <ChildComponent websocket={this.state.ws} />;
    return (
      <div>
        <WebSocketContext.Provider value={{ ws: this.state.ws }}>
          {this.props.children}
        </WebSocketContext.Provider>
      </div>
    );
  }
}

export default WebSocketClient;
