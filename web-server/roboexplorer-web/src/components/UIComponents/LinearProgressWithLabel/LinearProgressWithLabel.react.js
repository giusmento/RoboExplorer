import React from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import LinearProgress from "@material-ui/core/LinearProgress";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";

function LinearProgressWithLabel(props) {
  return (
    <Box display="flex" alignItems="center">
      <Box width="100%" mr={1}>
        <LinearProgress
          variant="determinate"
          {...props}
          className={props.className.root}
        />
      </Box>
      <Box minWidth={35}>
        <Typography variant="body2" color="textSecondary">{`${Math.round(
          props.value
        )}%`}</Typography>
      </Box>
    </Box>
  );
}

LinearProgressWithLabel.propTypes = {
  /**
   * The value of the progress indicator for the determinate and buffer variants.
   * Value between 0 and 100.
   */
  value: PropTypes.number.isRequired,
};

const useStyles = makeStyles({
  divRoot: {
    width: "100%",
  },
  root: {
    height: "25px",
    padding: "10px 10px",
    margin: "0px 0px",
  },
});

export default function LinearWithValueLabel(props) {
  const classes = useStyles();
  const [progress, setProgress] = React.useState(10);

  //   React.useEffect(() => {
  //     const timer = setInterval(() => {
  //       setProgress((prevProgress) =>
  //         prevProgress >= 100 ? 10 : prevProgress + 10
  //       );
  //     }, 800);
  //     return () => {
  //       clearInterval(timer);
  //     };
  //   }, []);

  return (
    <div className={classes.divRoot}>
      <LinearProgressWithLabel value={props.value} className={classes} />
    </div>
  );
}
