import React from "react";
import { WebSocketContext } from "../../components/Context/WebSocketContext";

export function WithWebSocket(Component) {
  return function WebSocketComponent(props) {
    return (
      <WebSocketContext.Consumer>
        {(contexts) => <Component {...props} {...contexts} />}
      </WebSocketContext.Consumer>
    );
  };
}
