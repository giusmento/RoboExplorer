import React, { useState } from "react";
import {
  Grid,
  LinearProgress,
  Select,
  OutlinedInput,
  MenuItem,
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

const mainChartData = getMainChartData();
const PieChartData = [
  { name: "Group A", value: 400, color: "primary" },
  { name: "Group B", value: 300, color: "secondary" },
  { name: "Group C", value: 300, color: "warning" },
  { name: "Group D", value: 200, color: "success" },
];

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
        setDistanceSensorChart(DistanceSensorData.arr);
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
            <Grid
              container
              direction="row"
              justify="space-between"
              alignItems="center"
            >
              <Grid item>
                <div style={{ position: "relative", width: "225px" }}>
                  <ResponsiveContainer height={150} width="99%">
                    <AreaChart data={distanceSensorChart.slice()}>
                      <Area
                        type="natural"
                        dataKey="value"
                        stroke={theme.palette.secondary.main}
                        fill={theme.palette.secondary.light}
                        strokeWidth={2}
                        fillOpacity="0.25"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </div>
              </Grid>
            </Grid>
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
                    Motor back
                  </Typography>
                  <LinearProgressWithLabel value={10} />
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
                    Motor front
                  </Typography>
                  <LinearProgressWithLabel value={30} />
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
                    Servo 0:
                  </Typography>
                  <Typography
                    size="xl"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                  >
                    &nbsp;&nbsp;15 &ordm;
                  </Typography>
                </div>
                <div className={classes.visitsNumberContainer}>
                  <Typography
                    size="l"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                  >
                    Servo 1:
                  </Typography>
                  <Typography
                    size="xl"
                    weight="medium"
                    color="text"
                    colorBrightness="secondary"
                  >
                    &nbsp;&nbsp;20 &ordm;
                  </Typography>
                </div>
              </Grid>
            </Grid>
          </Widget>
        </Grid>
        <Grid item lg={3} md={4} sm={6} xs={12}>
          <Widget title="Configuration" upperTitle className={classes.card}>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <ResponsiveContainer width="100%" height={144}>
                  <PieChart margin={{ left: theme.spacing(2) }}>
                    <Pie
                      data={PieChartData}
                      innerRadius={45}
                      outerRadius={60}
                      dataKey="value"
                    >
                      {PieChartData.map((entry, index) => (
                        <Cell
                          key={`cell-${index}`}
                          fill={theme.palette[entry.color].main}
                        />
                      ))}
                    </Pie>
                  </PieChart>
                </ResponsiveContainer>
              </Grid>
              <Grid item xs={6}>
                <div className={classes.pieChartLegendWrapper}>
                  {PieChartData.map(({ name, value, color }, index) => (
                    <div key={color} className={classes.legendItemContainer}>
                      <Dot color={color} />
                      <Typography style={{ whiteSpace: "nowrap" }}>
                        &nbsp;{name}&nbsp;
                      </Typography>
                      <Typography color="text" colorBrightness="secondary">
                        &nbsp;{value}
                      </Typography>
                    </div>
                  ))}
                </div>
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
                  Daily Line Chart
                </Typography>
                <div className={classes.mainChartHeaderLabels}>
                  <div className={classes.mainChartHeaderLabel}>
                    <Dot color="warning" />
                    <Typography className={classes.mainChartLegentElement}>
                      Tablet
                    </Typography>
                  </div>
                  <div className={classes.mainChartHeaderLabel}>
                    <Dot color="primary" />
                    <Typography className={classes.mainChartLegentElement}>
                      Mobile
                    </Typography>
                  </div>
                  <div className={classes.mainChartHeaderLabel}>
                    <Dot color="primary" />
                    <Typography className={classes.mainChartLegentElement}>
                      Desktop
                    </Typography>
                  </div>
                </div>
                <Select
                  value={mainChartState}
                  onChange={(e) => setMainChartState(e.target.value)}
                  input={
                    <OutlinedInput
                      labelWidth={0}
                      classes={{
                        notchedOutline: classes.mainChartSelectRoot,
                        input: classes.mainChartSelect,
                      }}
                    />
                  }
                  autoWidth
                >
                  <MenuItem value="daily">Daily</MenuItem>
                  <MenuItem value="weekly">Weekly</MenuItem>
                  <MenuItem value="monthly">Monthly</MenuItem>
                </Select>
              </div>
            }
          >
            <ResponsiveContainer width="100%" minWidth={500} height={350}>
              <ComposedChart
                margin={{ top: 0, right: -15, left: -15, bottom: 0 }}
                data={mainChartData}
              >
                <YAxis
                  ticks={[0, 2500, 5000, 7500]}
                  tick={{
                    fill: theme.palette.text.hint + "80",
                    fontSize: 14,
                  }}
                  stroke={theme.palette.text.hint + "80"}
                  tickLine={false}
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
                  type="natural"
                  dataKey="desktop"
                  fill={theme.palette.background.light}
                  strokeWidth={0}
                  activeDot={false}
                />
                <Line
                  type="natural"
                  dataKey="mobile"
                  stroke={theme.palette.primary.main}
                  strokeWidth={2}
                  dot={false}
                  activeDot={false}
                />
                <Line
                  type="linear"
                  dataKey="tablet"
                  stroke={theme.palette.warning.main}
                  strokeWidth={2}
                  dot={{
                    stroke: theme.palette.warning.dark,
                    strokeWidth: 2,
                    fill: theme.palette.warning.main,
                  }}
                />
              </ComposedChart>
            </ResponsiveContainer>
          </Widget>
        </Grid>
        {mock.bigStat.map((stat) => (
          <Grid item md={4} sm={6} xs={12} key={stat.product}>
            <BigStat {...stat} />
          </Grid>
        ))}
        <Grid item xs={12}>
          <Widget
            title="Support Requests"
            upperTitle
            noBodyPadding
            bodyClass={classes.tableWidget}
          >
            <Table data={mock.table} />
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
  var tablet = getRandomData(31, 3500, 6500, 7500, 1000);
  var desktop = getRandomData(31, 1500, 7500, 7500, 1500);
  var mobile = getRandomData(31, 1500, 7500, 7500, 1500);

  for (let i = 0; i < tablet.length; i++) {
    resultArray.push({
      tablet: tablet[i].value,
      desktop: desktop[i].value,
      mobile: mobile[i].value,
    });
  }

  return resultArray;
}
