import React from "react";
import { Button } from "@material-ui/core";

// styles
import useStyles from "./styles";

// components
import { Typography } from "../Wrappers";

export default function PageTitle(props) {
  var classes = useStyles();

  return (
    <div className={classes.pageTitleContainer}>
      <Typography className={classes.typo} variant="h1" size="sm">
        {props.title}
      </Typography>
      {props.label && (
        <div style={{ position: "relative", bottom: "-29px" }}>
          <Typography className={classes.typo} variant="body1" size="sm">
            {props.label}
          </Typography>
        </div>
      )}
    </div>
  );
}
