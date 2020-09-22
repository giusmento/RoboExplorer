import React, { useState } from "react";

const WebSocketConnectionContext = React.createContext();
const WebSocketConnectionDispatchContext = React.createContext();

//websocket initialization
//var ws = new WebSocket("ws://localhost:1111/");
var state = 0;
setTimeout(check, 5000);
function check() {
  console.log("check- ", state);
  state = state + 1;
}
// function webSockerConnectionReducer(state, action) {
//   console.log("websocket connection Reducer");
//   if (action.type == "connect") {
//     return { ws: action.ws };
//   } else {
//     return { ws: state.ws };
//   }
// }

function WebSocketConnectionProvider({ children }) {
  // const [state, dispatch] = React.useReducer(webSockerConnectionReducer, {
  //   ws: ws,
  // });
  state = state + 1;
  return (
    <WebSocketConnectionContext.Provider value={state}>
      {/* <WebSocketConnectionDispatchContext.Provider value={dispatch}> */}
      {children}
      {/* </WebSocketConnectionDispatchContext.Provider> */}
    </WebSocketConnectionContext.Provider>
  );
}

function useWebSocketConnectionContext() {
  const context = React.useContext(WebSocketConnectionContext);
  if (context === undefined) {
    throw new Error("useWebSocketContext must be used within a React Context");
  }
  return context;
}

function useWebSocketConnectionDispatchContext() {
  // const context = React.useContext(WebSocketConnectionDispatchContext);
  // if (context === undefined) {
  //   throw new Error(
  //     "useWebSocketDispatchContext must be used within a React Context"
  //   );
  // }
  // return context;
}

export {
  WebSocketConnectionProvider,
  useWebSocketConnectionContext,
  useWebSocketConnectionDispatchContext,
};
