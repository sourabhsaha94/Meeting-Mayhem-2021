
import React from "react";
import BootstrapTable from 'react-bootstrap-table-next';

export default function ReceivedMessages() {



    const columns = [{
        dataField: 'sender',
        text: 'Sender'
      }, {
        dataField: 'message',
        text: 'Message'
      }];

      var products = [{
        sender: "Sudha",
        message: "Hi Akriti"
    }, {
      sender: "Ryan",
      message: "Hey There!"
    }];


    return(
      <>
      <div>Received Messages</div>
        <BootstrapTable keyField='id' data={ products } columns={ columns } />
        </>
    ); 
}






