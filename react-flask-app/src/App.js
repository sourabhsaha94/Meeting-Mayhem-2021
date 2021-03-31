import React, { useState, useEffect } from 'react';

import { BrowserRouter as Router, Switch, Route} from "react-router-dom";

import Login from "./Login";
//import SignUp from "./Components/signup.component";
import Main from "./Main";

import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './App.css';


function App() {

const [currentTime, setCurrentTime] = useState(0);

  // useEffect(() => {
  //   setInterval(async () => {
  //     fetch('/time').then(res => res.json()).then(data => {
  //       setCurrentTime(data.time);
  //     });
  //   }, 2000);
  // }, []);

  return (<Router>
    <div className="App">
      
    {/* <p>The current time iss {currentTime}.</p> */}
      <div>
        <div>
          
          <Switch>
            <Route exact path='/' component={Login} />
            {/* <Route path="/sign-up" component={SignUp} /> */}
            <Route path="/home" component={Main} />
          </Switch>
          
        </div>
      </div>
    </div></Router>
  );
}

export default App;