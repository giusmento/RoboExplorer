import React, { useState } from "react";
import { Route, Switch, Redirect, withRouter } from "react-router-dom";
import classnames from "classnames";

// styles
import useStyles from "./styles";

// components
import Header from "../Header";
import Sidebar from "../Sidebar";

// pages
import Dashboard from "../../pages/dashboard";
import Typography from "../../pages/typography";
import Notifications from "../../pages/notifications";
import Maps from "../../pages/maps";
import Tables from "../../pages/tables";
import Icons from "../../pages/icons";
import Charts from "../../pages/charts";

// context
import { useLayoutState } from "../../context/LayoutContext";

// import { WebSocketBroadcastProvider } from "../Websocket/WebSocketBroadcastContext.react";
// import { WebSocketConnectionProvider } from "../Websocket/WebSocketConnectionContext.react";
// import WebSocketClientFunc from "../../components/Websocket/WebSocketClientFunc";
import WebSocketClient from "../../components/Websocket/WebSocketClient";

function Layout(props) {
  var classes = useStyles();

  //CAMERA HOOK
  var [isCameraActive, setCameraActive] = useState(false);
  var [isControlRobotActive, setControlRobotActive] = useState(false);

  var toggleCameraActive = (status) => {
    setCameraActive(status);
  };

  var toggleControlRobotActive = (status) => {
    setControlRobotActive(status);
  };

  // global
  var layoutState = useLayoutState();

  return (
    <div className={classes.root}>
      <>
        <Header
          history={props.history}
          toggleCameraActive={(status) => toggleCameraActive(status)}
          toggleControlRobotActive={(status) =>
            toggleControlRobotActive(status)
          }
        />
        <Sidebar />
        <div
          className={classnames(classes.content, {
            [classes.contentShift]: layoutState.isSidebarOpened,
          })}
        >
          <div className={classes.fakeToolbar} />
          {/* <WebSocketConnectionProvider>
            <WebSocketBroadcastProvider> */}
          <WebSocketClient>
            <Switch>
              <Route
                path="/app/dashboard"
                render={(routeProps) => (
                  <Dashboard
                    {...routeProps}
                    {...props}
                    {...(isCameraActive = { isCameraActive })}
                    {...(isControlRobotActive = { isControlRobotActive })}
                  />
                )}
              />
              <Route path="/app/typography" component={Typography} />
              <Route path="/app/tables" component={Tables} />
              <Route path="/app/notifications" component={Notifications} />
              <Route
                exact
                path="/app/ui"
                render={() => <Redirect to="/app/ui/icons" />}
              />
              <Route path="/app/ui/maps" component={Maps} />
              <Route path="/app/ui/icons" component={Icons} />
              <Route path="/app/ui/charts" component={Charts} />
            </Switch>
          </WebSocketClient>
          {/* </WebSocketBroadcastProvider>
          </WebSocketConnectionProvider> */}
        </div>
      </>
    </div>
  );
}

export default withRouter(Layout);
