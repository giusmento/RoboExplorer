import React, { useState } from "react";
import {
  Grid,
  LinearProgress,
  Select,
  OutlinedInput,
  MenuItem,
  FormControlLabel,
  Checkbox,
} from "@material-ui/core";
import WarningRoundedIcon from "@material-ui/icons/WarningRounded";
import { Alert } from "@material-ui/lab";
import { useTheme } from "@material-ui/styles";
import LinearProgressWithLabel from "../../components/UIComponents/LinearProgressWithLabel/LinearProgressWithLabel.react";
import {
  ResponsiveContainer,
  ComposedChart,
  AreaChart,
  LineChart,
  Line,
  Area,
  PieChart,
  Pie,
  Cell,
  YAxis,
  XAxis,
} from "recharts";

// styles
import useStyles from "./styles";

// components
import mock from "./mock";
import Widget from "../../components/Widget";
import PageTitle from "../../components/PageTitle";
import { Typography } from "../../components/Wrappers";
import Dot from "../../components/Sidebar/components/Dot";
import Table from "./components/Table/Table";
import BigStat from "./components/BigStat/BigStat";

import { WithWebSocket } from "../../components/Websocket/WithWebSocket";
import { FixedLengthArray } from "../../utils/FixedLengthArray";
import { ParseMessage } from "../../utils/ParseMessage";
//import WebSocketContext from "../../components/Context/WebSocketContext";

//const mainChartData = getMainChartData();
const mainChartData = new FixedLengthArray(100);

const DistanceSensorData = new FixedLengthArray(50);
DistanceSensorData.push({ value: 0 });

function Dashboard(props) {
  var classes = useStyles();
  var theme = useTheme();
  var ws: WebSocket = props.ws;
  const [lastDistance, setLastDistance] = useState({
    value: 0,
    timestamp: "",
  });
  const [distanceSensorChart, setDistanceSensorChart] = useState(
    DistanceSensorData.arr
  );
  const [lastMessage, setLastMessage] = useState("");
  const [distanceAlert, setDistanceAlert] = useState({ visible: false });
  const [motors, setMotors] = useState([]);
  const [servos, setServos] = useState([]);
  const [settings, setSettings] = useState([]);
  const [mainChart, setMainChart] = useState(mainChartData.arr);

  console.log(mainChart);

  ws.onmessage = (message) => {
    //parse message
    //console.log("dash:", message.data);
    var msg = new ParseMessage(message.data);
    //console.log("parsed:", msg);
    setLastMessage(msg.timestamp);
    switch (msg.type) {
      case "Summary":
        var last_distance = Math.round(msg.payload.last_distance * 100);
        var timestamp = msg.timestamp;
        DistanceSensorData.push({
          value: last_distance,
        });
        mainChartData.push({
          power_0: motors[0] && motors[0].speed ? motors[0].speed : 0,
          distance_0: last_distance ? last_distance : 0,
        });
        setMotors(msg.payload.motors);
        setServos(msg.payload.servos);
        setSettings(msg.payload.settings);
        setDistanceSensorChart(DistanceSensorData.arr);
        setMainChart(mainChartData.arr);
        setLastDistance({ value: last_distance, timestamp: timestamp });
        if (last_distance > 20) {
          setDistanceAlert({ visble: false });
        }
        break;
      case "Alert":
        setDistanceAlert({
          visible: true,
          message: msg.payload.message,
          distance: msg.payload.distance,
        });
    }
  };
  //console.log("ws", props);

  // local
  var [mainChartState, setMainChartState] = useState("monthly");

  function SendWSMessage() {
    return (
      <button
        onClick={() => props.ws.send(JSON.stringify({ type: "new message" }))}
      >
        Send message
      </button>
    );
    return null;
  }

  return (
    <>
      <PageTitle title="Dashboard" label={"Last update: " + lastMessage} />
      <Grid container spacing={4}>
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget
            title="Distance Sensor"
            upperTitle
            bodyClass={classes.fullHeightBody}
            className={classes.card}
          >
            <div className={classes.visitsNumberContainer}>
              <Typography
                size="l"
                weight="medium"
                color="text"
                colorBrightness="secondary"
              >
                Last distance
              </Typography>
              <Typography
                size="xl"
                weight="medium"
                color="text"
                colorBrightness="secondary"
              >
                &nbsp;&nbsp;{lastDistance.value} cm
              </Typography>
            </div>
            <div
              style={{
                position: "relative",
                top: "-17px",
                minHeight: "30px",
              }}
            >
              {distanceAlert.visible && <WarningRoundedIcon color="error" />}
            </div>
          </Widget>
        </Grid>
        <Grid item lg={3} md={8} sm={6} xs={12}>
          <Widget
            title="Motor Power"
            upperTitle
            className={classes.card}
            bodyClass={classes.fullHeightBody}
          >
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <div
                  style={{ position: "relative", top: "30px", width: "224px" }}
                >
                  <Typography
                    size="l"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                    className={classes.progressSectionTitle}
                  >
                    {motors[0] && motors[0].name ? motors[0].name : "loading.."}
                  </Typography>
                  <LinearProgressWithLabel
                    value={motors[0] && motors[0].speed ? motors[0].speed : 0}
                  />
                </div>
                <div
                  style={{ position: "relative", top: "30px", width: "224px" }}
                >
                  <Typography
                    size="l"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                    className={classes.progressSectionTitle}
                  >
                    {motors[1] && motors[1].name ? motors[1].name : "loading.."}
                  </Typography>
                  <LinearProgressWithLabel
                    value={motors[1] && motors[1].speed ? motors[1].speed : 0}
                  />
                </div>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
        <Grid item lg={3} md={8} sm={6} xs={12}>
          <Widget
            title="Servo Motors"
            upperTitle
            className={classes.card}
            bodyClass={classes.fullHeightBody}
          >
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <div className={classes.visitsNumberContainer}>
                  <Typography
                    size="l"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                  >
                    {servos[0] && servos[0].name ? servos[0].name : "loading.."}
                  </Typography>
                  <Typography
                    size="xl"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                  >
                    &nbsp;&nbsp;
                    {servos[0] && servos[0].name ? servos[0].value : "..."}
                    &ordm;
                  </Typography>
                </div>
                <div className={classes.visitsNumberContainer}>
                  <Typography
                    size="l"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                  >
                    {servos[1] && servos[1].name ? servos[1].name : "loading.."}
                  </Typography>
                  <Typography
                    size="xl"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                  >
                    &nbsp;&nbsp;
                    {servos[1] && servos[1].name ? servos[1].value : "..."}
                    &ordm;
                  </Typography>
                </div>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget title="Controls" upperTitle className={classes.card}>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <ResponsiveContainer width="100%" height={144}>
                  <div>
                    <div className={classes.visitsNumberContainer}>
                      <Checkbox
                        checked={
                          settings && settings.anti_collision
                            ? settings.anti_collision
                            : false
                        }
                        // onChange={handleChange}
                        name="checkedB"
                        color="primary"
                      />

                      <Typography
                        size="l"
                        weight="medium"
                        color="text"
                        colorBrightness="secondary"
                      >
                        Anti-collision {settings.anti_collision}
                      </Typography>
                    </div>
                    <div className={classes.visitsNumberContainer}>
                      <Checkbox
                        checked={
                          settings && settings.camera ? settings.camera : false
                        }
                        // onChange={handleChange}
                        name="checkedB"
                        color="primary"
                      />

                      <Typography
                        size="l"
                        weight="medium"
                        color="text"
                        colorBrightness="secondary"
                      >
                        Camera
                      </Typography>
                    </div>
                  </div>
                </ResponsiveContainer>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
        <Grid item xs={12}>
          <Widget
            bodyClass={classes.mainChartBody}
            header={
              <div className={classes.mainChartHeader}>
                <Typography
                  variant="h5"
                  color="text"
                  colorBrightness="secondary"
                >
                  Motor Power Chart
                </Typography>
                <div className={classes.mainChartHeaderLabels}>
                  <div className={classes.mainChartHeaderLabel}>
                    <Dot color="primary" />
                    <Typography
                      size="l"
                      weight="medium"
                      color="text"
                      colorBrightness="secondary"
                    >
                      &nbsp;Power 0
                    </Typography>
                  </div>
                  <div className={classes.mainChartHeaderLabel}>
                    <Dot color={theme.palette.background.light} />
                    <Typography
                      size="l"
                      weight="medium"
                      color="text"
                      colorBrightness="secondary"
                    >
                      Distance Sensor 0
                    </Typography>
                  </div>
                </div>
              </div>
            }
          >
            <ResponsiveContainer width="100%" minWidth={500} height={200}>
              <ComposedChart
                margin={{ top: 0, right: -15, left: -15, bottom: 0 }}
                data={mainChart.slice()}
              >
                <YAxis
                  yAxisId="left"
                  tick={{
                    fill: theme.palette.text.hint + "80",
                    fontSize: 14,
                  }}
                  stroke={theme.palette.text.hint + "80"}
                />
                <YAxis
                  yAxisId="right"
                  tick={{
                    fill: theme.palette.text.hint + "80",
                    fontSize: 14,
                  }}
                  stroke={"red"}
                  orientation="right"
                />
                <XAxis
                  tickFormatter={(i) => i + 1}
                  tick={{
                    fill: theme.palette.text.hint + "80",
                    fontSize: 14,
                  }}
                  stroke={theme.palette.text.hint + "80"}
                  tickLine={false}
                />
                <Area
                  yAxisId="right"
                  type="natural"
                  dataKey="distance_0"
                  fill={theme.palette.background.light}
                  strokeWidth={0}
                  activeDot={false}
                />
                <Line
                  yAxisId="left"
                  type="natural"
                  dataKey="power_0"
                  stroke={theme.palette.primary.main}
                  strokeWidth={2}
                  dot={false}
                  activeDot={false}
                />
              </ComposedChart>
            </ResponsiveContainer>
          </Widget>
        </Grid>
      </Grid>
    </>
  );
}

export default WithWebSocket(Dashboard);

// #######################################################################
function getRandomData(length, min, max, multiplier = 10, maxDiff = 10) {
  var array = new Array(length).fill();
  let lastValue;

  return array.map((item, index) => {
    let randomValue = Math.floor(Math.random() * multiplier + 1);

    while (
      randomValue <= min ||
      randomValue >= max ||
      (lastValue && randomValue - lastValue > maxDiff)
    ) {
      randomValue = Math.floor(Math.random() * multiplier + 1);
    }

    lastValue = randomValue;

    return { value: randomValue };
  });
}

function getMainChartData() {
  var resultArray = [];
  var power = getRandomData(100, 0, 100, 500);

  for (let i = 0; i < power.length; i++) {
    resultArray.push({
      power: power[i].value,
    });
  }

  return resultArray;
}
