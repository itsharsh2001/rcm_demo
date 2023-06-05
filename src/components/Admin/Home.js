import React, { useState } from "react";

import classes from "./Home.module.css";

export const Home = () => {
  let styling1 = {
    opacity:'1'
  }
  let styling0 = {
    opacity:'0'
  }
  const [entity, setEntity] = useState(false)
  const [tan, setTan] = useState(false)

  const entityToggler = () => {
    setEntity((prevState)=>{return !prevState})
  }

  const tanToggler = () => {
    setTan((prevState)=>{return !prevState})
  }
  return (
    <div className={classes.home}>
      {/* <h1>Dashboard</h1> */}
      <span className={classes.headingdiv}>
        <h1>Dashboard</h1>
      </span>

      <section className={classes.attributes}>
        <span>
          <select name="" id="">
            <option value="">Choose Group</option>
            <option value="">Value 1</option>
            <option value="">Value 2</option>
            <option value="">Value 3</option>
          </select>
          <label onClick={entityToggler} className={classes.whitelabel} htmlFor="">Choose Entity</label>
          <label onClick={tanToggler} className={classes.whitelabel} htmlFor="">Choose TAN</label>
          <select name="" id="">
            <option value="">Financial Year</option>
            <option value="">Value 1</option>
            <option value="">Value 2</option>
          </select>
        </span>
         <span>
          {/* <label htmlFor=""></label> */}
          <p></p>
          {(entity||tan) && <div  style={tan?styling0:styling1}>
            <span>
              <label htmlFor="">Entity 1</label>
              <input type="checkbox" name="" id="" />
            </span>
            <span>
              <label htmlFor="">Entity 2</label>
              <input type="checkbox" name="" id="" />
            </span>
            <span>
              <label htmlFor="">Entity 3</label>
              <input type="checkbox" name="" id="" />
            </span>
          </div>}

          {(entity||tan) && <div style={entity?styling0:styling1}>
            <span>
              <label htmlFor="">TAN 1</label>
              <input type="checkbox" name="" id="" />
            </span>
            <span>
              <label htmlFor="">TAN 2</label>
              <input type="checkbox" name="" id="" />
            </span>
            <span>
              <label htmlFor="">TAN 3</label>
              <input type="checkbox" name="" id="" />
            </span>
          </div>}
          <p></p>

          {/* <label htmlFor=""></label> */}
        </span>
      </section>

      {/* <main>
        <section>
          <img src="/MonthlyTDS.jpg" alt="" />
          <img src="/Top10Vendors.jpg" alt="" />
        </section>
        <div>
          <span>
            <img src="/PANGood.jpg" alt="" />
            <img src="/TDSDistribution.jpg" alt="" />
            
          </span>
          <img src="/MonthlyChallan.jpg" alt="" />
        </div>
      </main>
      <div className={classes.topdiv}>
        <img src="/VarianceTDS.jpg" alt="" />
        <img src="/Top10.jpg" alt="" />
      </div> */}

      <div className={classes.topdiv}>
        <img src="/TDSDistribution.jpg" alt="" />
        <img src="/MonthlyTDS.jpg" alt="" />
      </div>
      <div style={{ flexDirection: "row-reverse" }} className={classes.topdiv}>
        <img src="/PANGood.jpg" alt="" />
        <img src="/VarianceTDS.jpg" alt="" />
      </div>
      <img className={classes.bigimg} src="/MonthlyChallan.jpg" alt="" />
      <div className={classes.topdiv}>
        <img src="/Top10Vendors.jpg" alt="" />
        <img src="/Top10.jpg" alt="" />
      </div>
    </div>
  );
};
