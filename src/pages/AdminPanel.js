import React, { useState } from 'react'
import classes from './AdminPanel.module.css'
import { Home } from '../components/Admin/Home'

import { Sidebar } from '../components/UI/Sidebar'
import RCMAnalysis from '../components/Admin/RCMAnalysis'

export const AdminPanel = () => {
    const [home, setHome] = useState(true)
    const [rcmanalysis, setRcmanalysis] = useState(false)

    const pageHandler = (page) => {
        let flag1 = page==='home';
        let flag2 = page==='rcmanalysis'
        setHome(flag1);
        setRcmanalysis(flag2);
    }
  return (
    <div className={classes.admin}>
        {/* <Navbar navigation={pageHandler}/> */}
        <Sidebar navigation={pageHandler}/>
        {home && <Home/>}
        {rcmanalysis && <RCMAnalysis/>}
    </div>
  )
}
