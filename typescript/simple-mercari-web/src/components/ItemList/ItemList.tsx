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
  const [itemCopy, setItemCopy] = useState<Item[]>([])
  const [group, setGroup] = useState("Id")

  const GroupById = () =>{
    fetchItems();
    setGroup("Id");
  }
  const GroupByDiscount = async () =>{
    await setItemCopy((itemCopy.filter(item => Number(item.discount)>0)).sort(function (a,b){return Number(b.discount) - Number(a.discount)}));
    setGroup("Discount");
  }
  const GroupByCategory = async () =>{
    await setItemCopy(itemCopy.sort(function (a,b){
      var categoryA = a.category.toUpperCase(); // ignore upper and lowercase
      var categoryB = b.category.toUpperCase(); // ignore upper and lowercase
      if (categoryA < categoryB) return -1;
      if (categoryA > categoryB) return 1;
      return 0;}));
    setGroup("Category");
  }
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
        setItemCopy(data.items);
      })
      .catch(error => {
        console.error('GET error:',error)
      })
  }
  useEffect(()=>{
  },[group])
  useEffect(() => {
    fetchItems();
  }, []);

  
  return (
    <div style={{ backgroundColor: '#222427' }} className="block">
      <h3>All items</h3> 
      <p>
      <button onClick={()=>{GroupByDiscount();console.log(group)}}>discount list</button> 
      <button onClick={()=>{GroupByCategory();console.log(group)}}>similar item</button> 
      <button onClick={()=>{GroupById();console.log(group)}}>index list</button>
      </p>
      {console.log(items)}

      {itemCopy.map((item) => {
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
