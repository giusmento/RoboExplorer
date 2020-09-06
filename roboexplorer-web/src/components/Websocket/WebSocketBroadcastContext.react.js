import React, { useState } from "react";
// import WebSocketClient from "./WebSocketClient";

const WebSocketBroadcastContext = React.createContext();
const WebSocketBroadcastDispatchContext = React.createContext();
// const [ws, setWs] = useState(0);

function webSockerBroadcastReducer(state, action) {
  console.log(action);
  return { count: state.count + 1 };
}

function WebSocketBroadcastProvider({ children }) {
  const [state, dispatch] = React.useReducer(webSockerBroadcastReducer, {
    count: 0,
  });
  console.log("--");
  return (
    <WebSocketBroadcastContext.Provider value={state}>
      <WebSocketBroadcastDispatchContext.Provider value={dispatch}>
        {children}
      </WebSocketBroadcastDispatchContext.Provider>
    </WebSocketBroadcastContext.Provider>
  );
}

function useWebSocketBroadcastContext() {
  const context = React.useContext(WebSocketBroadcastContext);
  if (context === undefined) {
    throw new Error("useWebSocketContext must be used within a React Context");
  }
  return context;
}

function useWebSocketBroadcastDispatchContext() {
  const context = React.useContext(WebSocketBroadcastDispatchContext);
  if (context === undefined) {
    throw new Error(
      "useWebSocketDispatchContext must be used within a React Context"
    );
  }
  return context;
}

export {
  WebSocketBroadcastProvider,
  useWebSocketBroadcastContext,
  useWebSocketBroadcastDispatchContext,
};
