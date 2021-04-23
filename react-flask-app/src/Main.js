import React from "react";
import { Navbar,Nav} from 'react-bootstrap'
import SentMessages from './SentMessages'
import ReceivedMessages from './ReceivedMessages'
import Home from './home'
import {useState, useEffect} from "react";


export default function Main(props) {


    const [showHomeScreen, setShowHomeScreen] = useState(false);
    const [showSentMessagesScreen, setShowSentMessagesScreen] = useState(false);
    const [showReceivedMessagesScreen, setShowReceivedMessagesScreen] = useState(false); 
    const [emailAddress, setEmailAddress] = useState('');
    const [userName, setUserName] = useState('');

    useEffect(() => {
        setEmailAddress(props.location.state.emailAddress);
        setUserName(props.location.state.userName);
        setShowHomeScreen(true);

    }, []);


    function sentMessagesClicked() {

        setShowHomeScreen(false);
        setShowSentMessagesScreen(true);
        setShowReceivedMessagesScreen(false);


    }

    function homeClicked() {

        setShowHomeScreen(true);
        setShowSentMessagesScreen(false);
        setShowReceivedMessagesScreen(false);


    }

    function receivedMessagesClicked() {

        setShowHomeScreen(false);
        setShowSentMessagesScreen(false);
        setShowReceivedMessagesScreen(true);


    }


    return(
        <div>
            <div className="row">
                <div className="col-md-12">
                        <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
                            <Nav.Link onClick={homeClicked}><Navbar.Brand>Home </Navbar.Brand></Nav.Link>
                            <Navbar.Toggle aria-controls="basic-navbar-nav" />
                            <Navbar.Collapse id="basic-navbar-nav">
                                <Nav className="mr-auto">
                                    <Nav.Link onClick={sentMessagesClicked}>Sent Messages</Nav.Link>
                                
                                    <Nav.Link onClick={receivedMessagesClicked}>Received Messages</Nav.Link>
                                </Nav>
                                <Nav>
                                    <Nav className="navbar-brand pull-right">Hi {userName} !</Nav></Nav>
                                <Nav>
                                    <Nav.Link className="navbar-brand pull-right" href="/">Logout</Nav.Link></Nav>
                            </Navbar.Collapse>
                        </Navbar> 

                    {showSentMessagesScreen && <SentMessages/>}
                    {showReceivedMessagesScreen && <ReceivedMessages emailAddress={emailAddress} userName={userName}/>}
                    {showHomeScreen && <Home emailAddress={emailAddress} userName={userName}/>}

                </div>
            </div>
        </div>
    ); 
}