import React from 'react';

import { BrowserRouter as Router, Switch, Route} from "react-router-dom";

import Login from "./Login";
//import SignUp from "./Components/signup.component";
import Main from "./Main";

import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './App.css';


function App() {

  return (<Router>
    <div className="App">
      <div>
        <div>
          
          <Switch>
            <Route exact path='/' component={Login} />
            <Route path="/home" component={Main} />
          </Switch>
          
        </div>
      </div>
    </div></Router>
  );
}

export default App;