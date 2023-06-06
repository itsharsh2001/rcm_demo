import React, { useState } from "react";
import CloseIcon from "@mui/icons-material/Close";
import MenuIcon from "@mui/icons-material/Menu";

import HomeIcon from "@mui/icons-material/Home";
import DashboardIcon from "@mui/icons-material/Dashboard";
import SpaIcon from "@mui/icons-material/Spa";
import VerifiedUserIcon from "@mui/icons-material/VerifiedUser";
import PaidIcon from "@mui/icons-material/Paid";
import AccountBalanceIcon from "@mui/icons-material/AccountBalance";
import AltRouteIcon from "@mui/icons-material/AltRoute";
import InfoIcon from "@mui/icons-material/Info";

import classes from "./Sidebar.module.css";

export const Sidebar = ({ navigation }) => {
  const [sidebar, setSidebar] = useState(true);

  const sidebarToggler = () => {
    setSidebar((prevState) => {
      return !prevState;
    });
  };
  return (
    <>
      {sidebar && (
        <div className={classes.sidebar}>
          <span>
          <img src="/GTLogoWhite.png" alt="logoimage" />
            ITD Analytics
            <CloseIcon
              onClick={sidebarToggler}
              style={{
                cursor: "pointer",
                position: "relative",
                top: "1px",
                left: "0%",
                fontSize: "3rem",
                color: "white",
                zIndex: "101",
              }}
            />
          </span>
          {/* <img src="/GTLogoWhite.png" alt="logoimage" /> */}
          <ul>
            <li
              onClick={() => {
                return navigation("home");
              }}
            >
              <HomeIcon className={classes.listicon} />
              Home
            </li>
            <li
              onClick={() => {
                return navigation("rcmanalysis");
              }}
            >
              <SpaIcon className={classes.listicon} />
              RCM Analysis
            </li>
          </ul>

          <div className={classes.user}>
            <div>
              Harsh
              <br />
              <p>Developer</p>
            </div>
            <img src="/sampleuser.png" alt="profileimg" />
          </div>
        </div>
      )}
      {!sidebar && (
        <div className={classes.sidebar2}>
          {/* <CloseIcon style={{cursor: 'pointer',position:'relative', top:'25px', left:'85%', fontSize:'3rem', color:'black', zIndex:'101'}}/> */}
          <MenuIcon
            onClick={sidebarToggler}
            style={{
              cursor: "pointer",
              fontSize: "3rem",
              color: "white",
              position: "relative",
              top: "2.5rem",
              left: "25%",
            }}
          />
          <span>
            {/* <img src="/GTLogo2.jpg" alt="logoimage" /> */}
            {/* TDS Returns */}
          </span>
          <ul>
            <li
              onClick={() => {
                return navigation("home");
              }}
            >
              <HomeIcon className={classes.listicon2} />
            </li>
            
            <li
              onClick={() => {
                return navigation("home");
              }}
            >
              <SpaIcon className={classes.listicon2} />
            </li>
          </ul>
          {/* <div className={classes.expire}>
        Your session will <br/> expire in: 14 : 53
      </div> */}
          <div className={classes.user2}>
            <div>
              Harsh
              <br />
              <p>Developer</p>
            </div>
            <img src="/sampleuser.png" alt="profileimg" />
          </div>
        </div>
      )}
    </>
  );
};
