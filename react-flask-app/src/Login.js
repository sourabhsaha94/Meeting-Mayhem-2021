import React, { useState } from "react";
import "./Login.css";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [login, setLogin] = useState("Unsuccessfull");

  function validateForm() {
    return email.length > 0 && password.length > 0;
  }

  function handleSubmit(event) {
    fetch('/login').then(res => res.json()).then(data => {
      setLogin("Successful");
    });
    event.preventDefault();

    fetch('/login', {
        method: 'POST',
        body: JSON.stringify({"userName":email,"password":password}),
        headers: {
          'Content-Type':'text/plain'
        }
      }).then(function(response) {
        console.log(response)
        setLogin("Successful");
      });

  }

  return (
    <div className="Login">
       

        <form
                    id="main-login"
                    onSubmit = {handleSubmit}>
                    <h2>
                        Enter your Email Id and password to Login
                    </h2>
                    <label>
                        <span className="text">User Name:</span>
                        <input type="text" name="message" onChange={(e) => setEmail(e.target.value)}/><br/>
                    </label>
                    <br/>
                    <label>
                        <span className="text">Password:</span>
                        <input type="text" name="message"onChange={(e) => setPassword(e.target.value)}/><br/>
                    </label>
                    <br/>
          
                    <div className="align-right">
                        <button type="submit" disabled={!validateForm()}>Login</button>
                    </div>

                    <div>
                      <span className="text">{login}</span>
                    </div>
                </form>
    </div>
  );
}