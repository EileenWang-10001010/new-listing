import React, { useEffect, useState } from 'react';

interface Item {
  id: number;
  name: string;
  category: string;
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
        console.log(process.env);
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
    <div style={{ backgroundColor: '#222427' }}>
      { items.map((item) => {
        return (
          <div key={item.id} className='ItemList' >
            {/* TODO: Task 1: Replace the placeholder image with the item image */}
            <img  style={{ width: '50%' }} src={server.concat(`/image/${item.image}`)} alt={item.name} />
            <p>
            <span >Name: {item.name}</span>
            <br/>
            <span>Category: {item.category}</span>
            </p>
          </div>
        )
      })}
    </div>
  )
};
