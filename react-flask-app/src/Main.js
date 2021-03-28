import React from "react";
import { Navbar,Nav} from 'react-bootstrap'
export default function Main() {
    return(
        <div>
            <div className="row">
                <div className="col-md-12">
                        <Navbar bg="dark" variant="dark" expand="lg" sticky="top">
                            <Navbar.Brand href="/home">Caption It !</Navbar.Brand>
                            <Navbar.Toggle aria-controls="basic-navbar-nav" />
                            <Navbar.Collapse id="basic-navbar-nav">
                                <Nav className="mr-auto">
                                <Nav.Link>Upload an image</Nav.Link>
                                
                                <Nav.Link>My usage</Nav.Link>
                                </Nav>
                                <Nav>
                                <Nav class="navbar-brand pull-right">Hi player</Nav></Nav>
                                <Nav>
                                <Nav.Link class="navbar-brand pull-right" href="/logout">Logout</Nav.Link></Nav>
                            </Navbar.Collapse>
                        </Navbar> 
                </div>
            </div>
        </div>
    ); 
}