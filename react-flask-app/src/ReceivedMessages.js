
import React from "react";
import BootstrapTable from 'react-bootstrap-table-next';
import { useState } from "react";


export default function ReceivedMessages(props) {

  const [receivedMessages, setreceivedMessages] = useState([]);
  const [receiver] = useState(props.emailAddress);

  const requestOptions = {
    method: 'GET',
    headers: { 'Access-Control-Request-Method': 'GET'
    , 'Access-Control-Request-Headers': '*'}
};

  handleReceiveMessages()
  setInterval(() => handleReceiveMessages(), 5000);

  function handleReceiveMessages() {
    //console.log("fetching");
    fetch('https://k44erekqxe.execute-api.us-east-2.amazonaws.com/default/getMessages?receiver='+receiver, requestOptions)
    .then(response => {
    if (!response.ok) {
        const error = "There was some problem in the request. Please try again."
        return Promise.reject(error);
    }
  return response.json()
})
.then(data => {
  var m = JSON.parse(data.body);
  setreceivedMessages(m)
})
.catch(error => {
    console.error('There was an error!', error);
    alert(error)
});
  }

    const columns = [{
        dataField: 'sender',
        text: 'Sender'
      }, {
        dataField: 'message',
        text: 'Message',
        headerStyle: (colum, colIndex) => {
          return { 'whiteSppace' : 'nowrap' };
      }
      }];

    // const CaptionElement = () => <h3 style={{ borderRadius: '0.25em', textAlign: 'center', color: 'purple', border: '1px solid purple', padding: '0.5em' }}>Received Messages</h3>;


    return(
      <>
        <BootstrapTable 
        // caption={<CaptionElement />}
        keyField='messageId' 
        data={receivedMessages} 
        columns={ columns }
        striped
        hover
        condensed />
        </>
    ); 
}






