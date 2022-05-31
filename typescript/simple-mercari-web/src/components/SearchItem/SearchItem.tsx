import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import Input from '@mui/material/Input';
import SearchIcon from '@mui/icons-material/Search';

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

export const SearchItem: React.FC<{}> = () => {
  const [items, setItems] = useState<Item[]>([])
  const [keyword, setKeyword] = useState("")
  
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setKeyword(event.target.value);
};
  const onSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    let url = server.concat('/search') + "?keyword="+keyword;
    fetch(url,
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
  
  return (
    <div style={{ backgroundColor: "Cornsilk" }} >
        <h3>Search items</h3>
        <form onSubmit={onSubmit}>
        
        <div>
            <SearchIcon />
            <Input type='text' name='keyword' id='keyword' placeholder='search with item name or category keyword' onChange={onChange} required/> 
            <Button  type='submit'>search</Button>
        </div>
      </form>
      { items.map((item) => {
        return (
          <div key={item.id} className='Search' >
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
