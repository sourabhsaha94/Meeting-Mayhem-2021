import React, { useState } from "react";
import { Redirect } from 'react-router-dom'

export default function Login() {
        const [emailAddress, setEmailAddress] = useState('');
        const [userName, setUserName] = useState('');
        const [password, setPassword] = useState('');
      
    function validateForm() {
        return userName.length > 0 && password.length > 0;
    }

    function onSubmit(e) {
        e.preventDefault();
        const requestOptions = {
            method: 'POST',
            headers: { 'Access-Control-Request-Method': 'POST'
            , 'Access-Control-Request-Headers': '*'},
            body: JSON.stringify({ 
                'email': userName,
                'password': password
              })
        };

        fetch('https://2nahcals15.execute-api.us-east-2.amazonaws.com/default/login', requestOptions)
        .then(response => {

            // check for error response
            if (!response.ok) {
                // get error message from body or default to response statusText
                const error = "There was some problem in the request. Please try again."
                return Promise.reject(error);
            }
            return response.json()
        })
        .then(data => {

            if(data.body!==undefined)
            {
                var body = JSON.parse(data.body);
                setEmailAddress(body.emailAddress);
            }
            else
            {
               throw "Login failed";
            }
        })
        .catch(error => {
            console.error('There was an error!', error);
            alert(error)
        });
    
    }

    function handleuserNameChange(e) {
            setUserName(e.target.value);           
    }

    function handlePasswordChange(e) {
        setPassword(e.target.value);
    }
    
    if (emailAddress!=="") {
        return (
            <Redirect to={{pathname: "/home", state: { uname: userName, uid: emailAddress}} }/>
        )     
    }
    return (
        
        <div className="row" style={{paddingTop:100}}>
            <div className="col-md-4"></div>
            <div className="col-md-4">
            <div className="col-md-1"></div>
                <div className="col-md-8">
            
            <form>
            <h3>Sign In</h3>

            <div className="form-group">
                <input type="text" className="form-control" placeholder="Enter email*" onChange={handleuserNameChange} />
            </div>

            <div className="form-group">
                <input type="password" className="form-control" placeholder="Enter password*" onChange={handlePasswordChange}/>
            </div>

            <div className="row">
                
            </div>

            <button type="button" className="btn btn-primary btn-block" disabled={!validateForm()} onClick={onSubmit}>Login</button>
            <p className="forgot-password text-right">
                New user ? <a href="/sign-up">Register here</a>
            </p>
        </form>
        </div>
        
        </div><div className="col-md-4"></div>
        </div>
    );
}