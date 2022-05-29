import React, { useEffect, useState } from 'react';
import internal from 'stream';

interface Item {
  id: number;
  name: string;
  category: string;
  price: string;
  discount: string;
  image: string | File;
};

const server = process.env.API_URL || 'http://127.0.0.1:9000';

const placeholderImage = process.env.PUBLIC_URL + '/logo192.png';

export const ItemList: React.FC<{}> = () => {
  const [items, setItems] = useState<Item[]>([])
  const fetchItems = () => {
    fetch(server.concat('/items'),
    {
      method: 'GET',
      mode: 'cors',
      headers : {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
    })
      .then(response => response.json())
      .then(data => {
        console.log('GET success:',data.items);
        setItems(data.items);
      })
      .catch(error => {
        console.error('GET error:',error)
      })
  }

  useEffect(() => {
    fetchItems();
  }, []);
  
  return (
    <div style={{ backgroundColor: '#222427' }} className="block">
      <h3>All items</h3>
      { items.map((item) => {
        return (
          <div key={item.id} className='ItemList' >
            <div className='container'>
            <img  style={{ width: '50%' }} src={server.concat(`/image/${item.image}`)} alt={item.name} />
            {Number(item.discount)>0? <div className='image'>{item.discount}%off</div> : <div/>}
            </div>
            <p>
            <span >Name: {item.name}</span>
            <br/>
            <span>Category: {item.category}</span>
            <br />
            <span>price: {item.price} ¥</span>
            <br />
            {Number(item.discount)>0? <span>discount: {item.discount} % off</span> : <br/>}
            </p>
          </div>
        )
      })}
    </div>
  )
};
