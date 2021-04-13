
import React from "react";
import BootstrapTable from 'react-bootstrap-table-next';

export default function ReceivedMessages() {



    const columns = [{
        dataField: 'id',
        text: 'Product ID'
      }, {
        dataField: 'name',
        text: 'Product Name'
      }, {
        dataField: 'price',
        text: 'Product Price'
      }];

      var products = [{
        id: 1,
        name: "Product1",
        price: 120
    }, {
        id: 2,
        name: "Product2",
        price: 80
    }];


    return(
        <BootstrapTable keyField='id' data={ products } columns={ columns } />
    ); 
}






